"""Read-only source/evidence inventory and descriptive semantic failure audit."""

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.finalize_v4 import GENERATION_PATHS, verify_generation_freeze

OUT = ROOT / "docs/closure_audit"
BASE = "249d0a14cc6bd2f3c449d21b87c1daa3124a8c2a"
FREEZE = "1ead72ff7071e1f6de5867aaa250b0483d91431f"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, allow_nan=False), encoding="utf-8")


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, timeout=30).strip()


def main():
    snapshot = json.loads((ROOT.parent / "closure-original-hashes.json").read_text(encoding="utf-8"))
    changed = [name for name, expected in snapshot.items() if not (ROOT / name).is_file() or sha(ROOT / name) != expected]
    write("EVIDENCE_SNAPSHOT.json", snapshot)
    inventory = []
    for name in git("ls-files", "-z").split("\0"):
        path = ROOT / name
        if name and path.is_file() and not name.startswith("docs/closure_audit/"):
            inventory.append({"path": name, "bytes": path.stat().st_size, "sha256": sha(path)})
    write("FILE_INVENTORY.json", {"scope": "Tracked working bytes except closure directory to avoid self-hash recursion; external runtimes are separately identified", "files": inventory, "total_bytes": sum(r["bytes"] for r in inventory)})
    ancestry = {}
    for commit in ["e506110e3893af73378e74aa7dcfc922bbf9eaf3", "f2689cc2407c0d6f17eaee272f93cd233063cfc7", FREEZE, "a4454a9b518f0148409934a9da6be4a0c09f604a"]:
        code = subprocess.run(["git", "merge-base", "--is-ancestor", commit, BASE], cwd=ROOT, timeout=30).returncode
        ancestry[commit] = {"exit_code": code, "is_ancestor": code == 0}
    verify_generation_freeze(FREEZE)
    refs = {name: {"object": git("rev-parse", name), "commit": git("rev-parse", name + "^{}")}
            for name in ["paper-submission-v1", "paper-submission-v2", "paper-submission-v3"]}
    provenance = {
        "checkout": "genuine Git checkout; not reconstructed from ZIP",
        "base_commit": BASE, "audit_branch": git("branch", "--show-current"),
        "source_freeze": FREEZE, "expanded_generation_guard": "PASS",
        "expanded_generation_paths": GENERATION_PATHS, "ancestry": ancestry, "existing_tags": refs,
        "chronology": [{"commit": c, "recorded_git_dates": git("show", "-s", "--format=%aI|%cI", c)} for c in [FREEZE, "a4454a9b518f0148409934a9da6be4a0c09f604a", BASE]],
        "chronology_limit": "Git ancestry/order verified; author/committer clocks and provider execution dates are not independently time-attested",
        "from_anonymous_zip": "UNVERIFIABLE_FROM_ZIP: no .git history is exported",
        "original_evidence": {"files_checked": len(snapshot), "changed": changed, "status": "PASS" if not changed else "FAIL"},
    }
    write("GIT_AND_IMMUTABILITY.json", provenance)
    rows = json.loads((ROOT / "backend/evaluation/results_v4/test-frozen-20261022/results.json").read_text(encoding="utf-8"))
    groups = defaultdict(list)
    failures = []
    for row in rows:
        if not row.get("metrics"):
            continue
        groups[row["dataset"], row["condition"]].append(row)
        metrics = row["metrics"]
        cl, rel = metrics["reference_class"], metrics["reference_rel_typed"]
        if cl["f1"] < 1 or rel["f1"] < 1:
            failures.append({
                "dataset": row["dataset"], "condition": row["condition"], "case_id": row["case_id"], "rep": row["rep"],
                "class_f1": cl["f1"], "typed_rel_f1": rel["f1"], "critic_valid": row["critic_valid"],
                "compiler_valid": row["compiler_valid"], "project_valid": row["project_valid"], "terminated_by": row["terminated_by"],
                "missing_classes": json.dumps(cl["missing"]), "spurious_classes": json.dumps(cl["spurious"]),
                "missing_typed_edges": json.dumps(rel["missing"]), "spurious_typed_edges": json.dumps(rel["spurious"]),
                "case_file": f"backend/evaluation/results_v4/test-frozen-20261022/cases/{row['condition']}_{row['case_id']}_{row['rep']}.json",
            })
    with (OUT / "SEMANTIC_DEVIATIONS.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(failures[0]))
        writer.writeheader()
        writer.writerows(failures)
    summaries = []
    for (dataset, condition), group in sorted(groups.items()):
        counts = Counter()
        for row in group:
            match = all(row["metrics"][m]["f1"] == 1 for m in ["reference_class", "reference_rel_typed"])
            critic = row["critic_valid"]
            counts["structural_exact" if match else "structural_deviation"] += 1
            if critic is True:
                counts["critic_true_exact" if match else "critic_true_deviation"] += 1
            elif critic is False:
                counts["critic_false_exact" if match else "critic_false_deviation"] += 1
            else:
                counts["critic_not_run_or_null"] += 1
            if row["terminated_by"] == "accepted":
                counts["accepted_exact" if match else "accepted_deviation"] += 1
        summaries.append({"dataset": dataset, "condition": condition, "case_runs": len(group), "independent_cases": len({r['case_id'] for r in group}), "counts": dict(counts), "C2_status": "exploratory post-test source fix" if condition == "C2" else "frozen main observation"})
    write("SEMANTIC_CATEGORIES.json", {"definition": "Exact means class and directed typed-edge F1 both 1.0; excludes multiplicity/attributes/NL semantics. Not an independently adjudicated semantic confusion matrix.", "groups": summaries, "deviation_rows": len(failures)})
    tools = {}
    for program, args in [("java", ["-version"]), ("node", ["--version"]), ("npm", ["--version"]), ("docker", ["--version"]), ("dot", ["-V"])]:
        executable = shutil.which(program)
        if not executable:
            tools[program] = {"status": "BULUNAMADI on PATH"}
        else:
            # Windows npm.cmd cannot be launched without cmd, so use node inventory only here.
            if program == "npm":
                tools[program] = {"status": "present; lint/build exit 0 recorded separately"}
            else:
                try:
                    result = subprocess.run([executable, *args], capture_output=True, text=True, timeout=20)
                    tools[program] = {"exit_code": result.returncode, "version": (result.stdout + result.stderr).strip()}
                except (OSError, subprocess.TimeoutExpired) as exc:
                    tools[program] = {"status": "INCONCLUSIVE", "error_type": type(exc).__name__, "limitation": "Not counted as pass; see separate authorized live-runtime check"}
    write("RUNTIME_INVENTORY.json", {"python": sys.version.split()[0], "tools": tools,
          "locks": {name: sha(ROOT / name) for name in ["requirements.lock.txt", "requirements-dev.txt", "requirements-index.lock.txt", "frontend/package-lock.json"]},
          "container": "backend/Dockerfile exists; Docker absent, build NOT TESTABLE", "jar": "External pinned binary, not bundled; SHA/live tests in LIVE_RUNTIME_CHECKS.json"})
    print(json.dumps({"protected_files": len(snapshot), "changed": len(changed), "inventory_files": len(inventory), "semantic_deviations": len(failures), "ancestry": all(r["is_ancestor"] for r in ancestry.values())}))
    if changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
