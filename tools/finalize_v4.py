"""Derive and audit a complete frozen matrix. No model/API calls or Git mutations."""

from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.evaluation.analyze_v4 import main as analyze
from backend.evaluation.run_matrix import JAR_SHA, dump, load_cases
from backend.evaluation.validator_audit import measured_cache, run as audit
from tools.check_numbers import check


def coverage(rows, cases, conditions, repetitions):
    expected = {
        (condition, case["case_id"], rep)
        for condition in conditions
        for case in cases
        for rep in range(1, 2 if condition in {"C0", "C1", "C2"} else repetitions + 1)
    }
    actual = [(r["condition"], r["case_id"], r["rep"]) for r in rows]
    missing = sorted(expected - set(actual))
    unexpected = sorted(set(actual) - expected)
    duplicates = sorted(k for k, n in Counter(actual).items() if n != 1)
    incomplete = [k for k, r in zip(actual, rows) if r.get("run_status", "completed") != "completed"]
    if missing or unexpected or duplicates or incomplete:
        raise ValueError(
            json.dumps(
                {
                    "missing": missing,
                    "unexpected": unexpected,
                    "duplicates": duplicates,
                    "incomplete": incomplete,
                }
            )
        )
    return {
        "status": "passed",
        "expected_case_runs": len(expected),
        "observed_unique_case_runs": len(actual),
        "complete_registered_matrix": True,
    }


def finalize(directory, audit_directory):
    protected_root = ROOT / "backend/evaluation/results_v4"
    for path in [directory, audit_directory]:
        if not path.resolve().is_relative_to(protected_root.resolve()):
            raise ValueError("Outputs must remain inside results_v4")
    if audit_directory.exists():
        raise ValueError("Choose a new audit directory; existing evidence is preserved")
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "completed":
        raise ValueError("Main matrix is not completed; do not finalize partial evidence")
    raw = directory / "results.json"
    for name, checksum in manifest["output_hashes"].items():
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != checksum:
            raise ValueError("Raw run manifest mismatch: " + name)
    rows = json.loads(raw.read_text(encoding="utf-8"))
    config = manifest["config"]
    cases = load_cases(config["split"], config["datasets"])
    if hashlib.sha256(json.dumps(cases, sort_keys=True).encode()).hexdigest() != manifest["input_sha256"]:
        raise ValueError("Input dataset changed after the registered run")
    proof = coverage(rows, cases, config["conditions"], config["reps"])
    generation_paths = [
        "ai_core/prompts",
        "ai_core/rules",
        "ai_core/src/ai/repair_agent.py",
        "ai_core/src/ai/plantuml_normalizer.py",
        "ai_core/src/rag/local_rules.py",
        "backend/src/ocl_engine",
        "backend/src/utils",
        "backend/src/repair",
        "backend/src/plantuml_runtime.py",
        "backend/evaluation/reference_metrics.py",
        "backend/evaluation/shared_repair_benchmark_cases.py",
        "backend/evaluation/pure_external_repair_cases.py",
        "backend/evaluation/semantic_benchmark",
    ]
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", manifest["git_commit"], "--", *generation_paths], cwd=ROOT, text=True
    )
    if changed.strip():
        raise ValueError("Generation/validator sources changed after freeze: " + changed)
    analyze(["--run-dir", str(directory)])
    proof["derived_numbers"] = check(directory)
    audit_directory.mkdir(parents=True)
    sources = sorted(
        p.parent
        for p in protected_root.glob("*/results.json")
        if (p.parent / "cases").is_dir() and (p.parent / "manifest.json").exists()
    )
    cache, provenance = measured_cache(sources)
    earlier = protected_root / "validator-audit-20261022/audit.json"
    old = json.loads(earlier.read_text(encoding="utf-8"))
    if old["plantuml_jar_sha256"] != JAR_SHA:
        raise ValueError("Earlier audit compiler mismatch")
    for row in old["diagrams"]:
        digest = row["diagram_sha256"]
        if digest not in provenance["conflicting_hashes_requiring_recheck"]:
            if digest in cache and cache[digest]["compiler_valid"] != row["compiler_valid"]:
                cache.pop(digest)
                provenance["conflicting_hashes_requiring_recheck"].append(digest)
            else:
                cache.setdefault(digest, row)
    paths = [p / "results.json" for p in sources]
    paths += sorted((ROOT / "backend/evaluation/results").rglob("*.json"))
    result = audit(paths, cached=cache)
    # Publish portable source identifiers rather than local absolute paths.
    for occurrence in result["occurrences"]:
        occurrence["file"] = str(Path(occurrence["file"]).relative_to(ROOT)).replace("\\", "/")
    result["plantuml_jar_sha256"] = JAR_SHA
    result["reuse_provenance"] = provenance
    result["source_results_sha256"] = {
        str(p.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths
    }
    dump(audit_directory / "audit.json", result)
    proof["audit_unique_diagrams"] = len(result["diagrams"])
    proof["audit_confusion"] = result["confusion"]
    proof["source_generation_commit"] = manifest["git_commit"]
    proof["generation_sources_unchanged"] = True
    proof["all_measured_run_ids"] = [p.name for p in sources]
    proof["audit_sha256"] = hashlib.sha256((audit_directory / "audit.json").read_bytes()).hexdigest()
    archives = [
        json.loads(p.read_text(encoding="utf-8")) for p in (directory / "incomplete_attempts").glob("*.json")
    ]
    attempts = [t for r in archives for t in r.get("trace", [])]
    known = [t for t in attempts if t.get("tokens_in") is not None and t.get("tokens_out") is not None]
    proof["archived_incomplete_attempt_usage"] = {
        "archived_case_attempts": len(archives),
        "model_attempts": len(attempts),
        "unknown_usage_attempts": len(attempts) - len(known),
        "known_usage_subtotal_usd": sum(
            (t["tokens_in"] * 0.15 + t["tokens_out"] * 0.60) / 1e6 for t in known
        ),
    }
    dump(audit_directory / "finalization.json", proof)
    return proof


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--audit-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(finalize(args.run_dir.resolve(), args.audit_dir.resolve())), flush=True)
