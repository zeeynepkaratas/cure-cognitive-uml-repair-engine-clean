"""Verify existing v4 evidence with all new outputs isolated from frozen files.

No LLM client is called. This invokes the original independent checker with
only its output directory redirected, plus read-only original verification.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def safe_output(path):
    path = path.resolve()
    if path.is_relative_to(ROOT) and not path.is_relative_to(ROOT / "docs/final_closure"):
        raise ValueError("Outputs inside this checkout must be under docs/final_closure")
    if path.exists() and any(path.iterdir()):
        raise FileExistsError("Choose a new empty verification directory; do not overwrite evidence")
    return path


def verify(output):
    output = safe_output(output)
    output.mkdir(parents=True, exist_ok=True)
    from tools import closure_audit_v4 as independent
    from tools.check_numbers import check
    from tools.verify_retained_evidence import verify as retained
    from tools.finalize_v4 import verify_generation_freeze

    # No metric, parser, prompt, generation or statistic implementation changes.
    independent.OUT = output
    independent.main()
    numbers = check(ROOT / "backend/evaluation/results_v4/test-frozen-20261022")
    retained_result = retained()
    snapshot = json.loads((ROOT / "docs/closure_audit/EVIDENCE_SNAPSHOT.json").read_text(encoding="utf-8"))
    differences = [p for p, h in snapshot.items() if not (ROOT / p).is_file() or hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h]
    verify_generation_freeze("1ead72ff7071e1f6de5867aaa250b0483d91431f")
    old = json.loads((ROOT / "docs/closure_audit/GIT_AND_IMMUTABILITY.json").read_text(encoding="utf-8"))
    for tag, ref in old["existing_tags"].items():
        actual = subprocess.check_output(["git", "rev-parse", tag], cwd=ROOT, text=True).strip()
        if actual != ref["object"]:
            raise ValueError("Historical tag changed: " + tag)
    report = {"status": "PASS" if not differences else "BLOCKING_INTEGRITY_FAILURE", "protected_files": len(snapshot), "changed": differences, "read_only_numbers": numbers, "retained": retained_result, "generation_freeze": "PASS", "model_calls": 0}
    (output / "READ_ONLY_VERIFICATION.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "retained"}))
    if differences:
        raise SystemExit(1)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    verify(args.output)
