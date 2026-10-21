"""Recompute all derived v4 numbers from retained raw cases and verify hashes."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.evaluation.analyze_v4 import compute


def check(directory):
    raw = directory / "results.json"
    recorded = json.loads((directory / "paper_inputs/numbers.json").read_text(encoding="utf-8"))
    expected = compute(json.loads(raw.read_text(encoding="utf-8")))
    expected["source_results_sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
    if recorded != expected:
        raise AssertionError("Derived numbers differ from raw case recomputation")
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    for name, checksum in manifest.get("output_hashes", {}).items():
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != checksum:
            raise AssertionError("Manifest output mismatch: " + name)
    per_case = [
        json.loads(p.read_text(encoding="utf-8")) for p in sorted((directory / "cases").glob("*.json"))
    ]
    if per_case != json.loads(raw.read_text(encoding="utf-8")):
        raise AssertionError("Aggregate result file differs from per-case records")
    return {"status": "passed", "raw_case_runs": len(per_case), "all_derived_numbers_recomputed": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.run_dir)))
