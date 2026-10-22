"""Audit project-validator agreement with compilation (not semantic correctness)."""

from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from backend.src.repair.validation import check_diagram
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    paths = [
        q
        for p in args.paths
        for q in (sorted(p.glob("*.json")) if p.is_dir() else [p])
        if q.name not in {"manifest.json", "validator_audit.json"}
    ]
    result = run(paths)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result["confusion"]))


if __name__ == "__main__":
    main()
