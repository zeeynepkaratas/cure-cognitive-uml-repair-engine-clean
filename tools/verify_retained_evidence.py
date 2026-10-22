"""Read-only verification against the v3 evidence baseline."""

import argparse
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.sanitize_artifact import numeric_values

BASE = "b9bee1d78bbdda14d9a1b07585f865b18aa5ef0d"


def numeric_csv(data):
    rows = list(csv.reader(io.StringIO(data)))
    numbers = []
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            try:
                number = Decimal(value)
            except InvalidOperation:
                continue
            numbers.append((i, j, str(number)))
    return numbers


def verify(base=BASE):
    paths = subprocess.check_output(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            base,
            "--",
            "backend/evaluation/results",
            "docs/submission-audit-2026-10-20",
        ],
        cwd=ROOT,
        text=True,
    ).splitlines()
    checks = []
    for name in paths:
        before = subprocess.check_output(["git", "show", f"{base}:{name}"], cwd=ROOT)
        path = ROOT / name
        if not path.exists():
            raise AssertionError("Retained evidence missing: " + name)
        after = path.read_bytes()
        before_text = before.decode("utf-8-sig")
        after_text = after.decode("utf-8-sig")
        if path.suffix == ".json":
            assert numeric_values(json.loads(before_text)) == numeric_values(json.loads(after_text)), name
            proof = "all numeric/boolean/null values and their JSON paths identical"
        elif path.suffix == ".csv":
            assert numeric_csv(before_text) == numeric_csv(after_text), name
            proof = "all numeric CSV cells and row/column positions identical"
        else:
            proof = (
                "retained; review string/path changes separately (no generic numeric claim for code or prose)"
            )
        checks.append(
            {
                "file": name,
                "sha256_v3_git_blob": hashlib.sha256(before).hexdigest(),
                "sha256_current_worktree": hashlib.sha256(after).hexdigest(),
                "proof": proof,
            }
        )
    original = "data_pipeline/datasets/pure_dataset.csv"
    old = subprocess.check_output(["git", "show", f"{base}:{original}"], cwd=ROOT)
    current = (ROOT / original).read_bytes()
    assert old.replace(b"\r\n", b"\n") == current.replace(b"\r\n", b"\n"), "Original PURE CSV content changed"
    return {
        "base_commit": base,
        "status": "passed",
        "protected_file_count": len(checks),
        "original_pure_csv": "identical content; line-ending normalisation allowed",
        "checks": checks,
        "clarification": "The A1 report is the historical sanitization log; its after-hashes describe that stage. This report verifies the current state independently against v3.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = verify()
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "checks"}))
