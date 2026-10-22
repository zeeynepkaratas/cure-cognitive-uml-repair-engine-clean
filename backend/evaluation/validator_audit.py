"""Audit project-validator agreement with compilation (not semantic correctness)."""

from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from backend.src.repair.validation import check_diagram
from backend.src.ocl_engine.error_handler import plantuml_syntax_kontrol
from backend.src.ocl_engine.ocl_validator import validate_ocl
from ai_core.src.rag.local_rules import rule_catalogue


def confusion(rows, predicted="project_valid", actual="compiler_valid"):
    counts = Counter()
    for row in rows:
        p, a = row.get(predicted), row.get(actual)
        if type(p) is not bool or type(a) is not bool:
            counts["unavailable"] += 1
        else:
            counts["TP" if p and a else "FP" if p else "FN" if a else "TN"] += 1
    tp, fp, fn, tn = (counts[k] for k in ("TP", "FP", "FN", "TN"))
    return {
        **{k: counts[k] for k in ("TP", "FP", "FN", "TN", "unavailable")},
        "sensitivity": tp / (tp + fn) if tp + fn else None,
        "specificity": tn / (tn + fp) if tn + fp else None,
    }


def extract_diagrams(value):
    """Only recognized diagram fields; source references are included and labelled."""
    fields = {
        "plantuml_kodu",
        "final_plantuml",
        "reference_plantuml",
        "input_plantuml",
        "output_plantuml",
        "gold",
        "defective",
        "raw_final_plantuml",
        "output_if_reverted",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            if key in fields and isinstance(item, str):
                yield key, item
            else:
                yield from extract_diagrams(item)
    elif isinstance(value, list):
        for item in value:
            yield from extract_diagrams(item)


def run(paths, checker=check_diagram, cached=None):
    unique = {}
    occurrences = []
    for path in paths:
        value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
        for field, diagram in extract_diagrams(value):
            sha = hashlib.sha256(diagram.encode()).hexdigest()
            occurrences.append({"file": str(path).replace("\\", "/"), "field": field, "diagram_sha256": sha})
            if sha not in unique:
                unique[sha] = (cached or {}).get(sha) or {"diagram_sha256": sha, **checker(diagram)}
    rows = list(unique.values())
    rules = [
        {
            "id": r["id"],
            "description": r["text"],
            "severity": r["severity"],
            "influences_verdict": r["severity"] == "error",
        }
        for r in rule_catalogue()
        if not r["domain_example"]
    ]
    return {
        "scope": "Compiler agreement only; not a semantic-validator accuracy estimate.",
        "unit": "unique diagram SHA-256, occurrence mapping retained",
        "confusion": confusion(rows),
        "rules": rules,
        "diagrams": rows,
        "occurrences": occurrences,
    }


def measured_cache(directories):
    """Reuse real checks by exact diagram hash; retain conflicts for fresh checking.

    Raw call traces contain measured compiler flags for intermediate Healer
    outputs. Project checks are inexpensive and recomputed locally. Unknown
    compiler outcomes are not promoted to passes or used as cache entries.
    """
    from backend.evaluation.run_matrix import JAR_SHA

    cache, conflicts, sources = {}, set(), []
    for directory in directories:
        manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
        if manifest["plantuml_jar_sha256"] != JAR_SHA:
            raise ValueError("Measured compiler cache uses a different JAR")
        raw = directory / "results.json"
        if (
            manifest.get("output_hashes", {}).get("results.json")
            != hashlib.sha256(raw.read_bytes()).hexdigest()
        ):
            raise ValueError("Measured results hash does not match its manifest")
        rows = json.loads(raw.read_text(encoding="utf-8"))
        sources.append(
            {
                "run_id": directory.name,
                "git_commit": manifest["git_commit"],
                "results_sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
            }
        )
        for row in rows:
            candidates = [
                (row["input_plantuml"], row["input_validation"]),
                (row["output_plantuml"], row["output_validation"]),
            ]
            candidates += [(t["output_plantuml"], t) for t in row.get("trace", []) if "output_plantuml" in t]
            for code, measured in candidates:
                if type(measured.get("compiler_valid")) is not bool:
                    continue
                digest = hashlib.sha256(code.encode()).hexdigest()
                if digest in cache and cache[digest]["compiler_valid"] != measured["compiler_valid"]:
                    conflicts.add(digest)
                elif digest in cache:
                    continue
                syntax, ocl = plantuml_syntax_kontrol(code), validate_ocl(code)
                cache[digest] = {
                    "diagram_sha256": digest,
                    "project_valid": syntax["gecerli"] and ocl["gecerli_mi"],
                    "compiler_valid": measured["compiler_valid"],
                    "compiler_available": True,
                    "compiler_errors": measured.get("compiler_errors", []),
                    "project_errors": syntax["hatalar"] + ocl["hatalar"],
                    "warnings": ocl["uyarilar"],
                    "rule_results": ocl["detaylar"],
                    "measurement_source": directory.name,
                }
    for digest in conflicts:
        cache.pop(digest, None)
    return cache, {
        "measured_runs": sources,
        "conflicting_hashes_requiring_recheck": sorted(conflicts),
        "measured_unique_hashes": len(cache),
        "reuse_scope": "Same pinned compiler, exact diagram SHA; project rules recomputed. Not an independent repeated compilation.",
    }


def main():
    from backend.evaluation.run_matrix import JAR_SHA

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--measured-runs", nargs="*", type=Path, default=[])
    parser.add_argument("--cached-audits", nargs="*", type=Path, default=[])
    args = parser.parse_args()
    paths = [
        q
        for p in args.paths
        for q in (sorted(p.glob("*.json")) if p.is_dir() else [p])
        if q.name not in {"manifest.json", "validator_audit.json"}
    ]
    cache = {}
    for path in args.cached_audits:
        previous = json.loads(path.read_text(encoding="utf-8"))
        if previous.get("plantuml_jar_sha256") != JAR_SHA:
            raise ValueError("Cached audit JAR SHA missing or different")
        cache.update({r["diagram_sha256"]: r for r in previous["diagrams"]})
    measured, provenance = measured_cache(args.measured_runs)
    conflicts = set(provenance["conflicting_hashes_requiring_recheck"])
    conflicts.update(
        k
        for k, value in measured.items()
        if k in cache and cache[k]["compiler_valid"] != value["compiler_valid"]
    )
    provenance["conflicting_hashes_requiring_recheck"] = sorted(conflicts)
    cache.update(measured)
    for digest in provenance["conflicting_hashes_requiring_recheck"]:
        cache.pop(digest, None)
    result = run(paths, cached=cache)
    result["reuse_provenance"] = provenance
    result["plantuml_jar_sha256"] = JAR_SHA
    result["source_results_sha256"] = {
        str(p).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result["confusion"]))


if __name__ == "__main__":
    main()
