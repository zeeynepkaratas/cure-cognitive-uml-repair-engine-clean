"""Budgeted, resumable evaluation matrix; never writes retained results/."""

from __future__ import annotations
import argparse
import csv
from dataclasses import asdict
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from ai_core.src.ai.repair_agent import RepairConfig, UMLRepairAgent
from backend.evaluation.shared_repair_benchmark_cases import SHARED_REPAIR_BENCHMARK_CASES
from backend.evaluation.pure_external_repair_cases import PURE_EXTERNAL_REPAIR_CASES
from backend.evaluation.reference_metrics import reference_metrics
from backend.src.repair.deterministic import deterministic_minimal, deterministic_extended
from backend.src.repair.validation import check_diagram

CONDITIONS = {
    "C0": "none",
    "C1": "deterministic_minimal",
    "C2": "deterministic_extended",
    "C3": "single_pass",
    "C4": "healer_only_compiler_feedback",
    "C5": "legacy_critic_healer",
    "C6": "critic_healer_norules",
    "C7": "improved_critic_healer",
}
JAR_SHA = "89948f14c93756c7a3fb7b69078ff37e8489fd79dd430c582b931e2f65358690"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    temporary.replace(path)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load_cases(split="test", datasets=("shared", "pure", "semantic")):
    cases = []
    if "shared" in datasets:
        cases.extend(
            {
                "case_id": c["case_id"],
                "dataset": "shared",
                "srs": c["srs_metni"],
                "input_plantuml": c["plantuml_kodu"],
                "gold": None,
                "defect_ids": [c["category"]],
            }
            for c in SHARED_REPAIR_BENCHMARK_CASES
            if split == "test"
        )
    if "pure" in datasets:
        cases.extend(
            {
                "case_id": c["case_id"],
                "dataset": "pure",
                "srs": c["srs_metni"],
                "input_plantuml": c["plantuml_kodu"],
                "gold": c["reference_plantuml"],
                "defect_ids": [c["category"]],
            }
            for c in PURE_EXTERNAL_REPAIR_CASES
            if split == "test"
        )
    if "semantic" in datasets:
        data = json.loads(
            (ROOT / "backend/evaluation/semantic_benchmark/cases.json").read_text(encoding="utf-8")
        )
        cases.extend(
            {**c, "dataset": "semantic", "input_plantuml": c["defective"]}
            for c in data
            if c["split"] == split
        )
    return cases


class BudgetExceeded(RuntimeError):
    budget_exceeded = True


class Budget:
    """Reserve conservative upper-bound USD before every attempted API request.

    Count UTF-8 bytes as an upper bound on input tokens, plus 4096 schema/framing
    tokens. Reservations are never refunded, including timeouts. The bound is
    specific to configured gpt-4o-mini pricing and completion-token limits.
    Persist before dispatch so resume cannot reset the allowance after a crash.
    """

    def __init__(self, path, max_calls, max_cost, input_price=0.15, output_price=0.60):
        self.path = path
        self.max_calls = max_calls
        self.max_cost = max_cost
        self.input_price = input_price
        self.output_price = output_price
        self.state = (
            json.loads(path.read_text()) if path.exists() else {"calls_reserved": 0, "usd_reserved": 0.0}
        )

    def reserve(self, role, prompt, config):
        cost = (
            (len(prompt.encode("utf-8")) + 4096) * self.input_price + config.max_tokens * self.output_price
        ) / 1e6
        if (
            self.state["calls_reserved"] + 1 > self.max_calls
            or self.state["usd_reserved"] + cost > self.max_cost
        ):
            raise BudgetExceeded("Call/cost reservation limit reached before dispatch")
        self.state["calls_reserved"] += 1
        self.state["usd_reserved"] += cost
        dump(self.path, self.state)


def plan(cases, conditions, reps, retries=2):
    per = {"C0": 0, "C1": 0, "C2": 0, "C3": 1, "C4": 3, "C5": 7, "C6": 7, "C7": 7}
    return {
        "case_count": len(cases),
        "conditions": conditions,
        "llm_repetitions": reps,
        "planned_case_runs": len(cases) * sum(1 if c in {"C0", "C1", "C2"} else reps for c in conditions),
        "upper_bound_api_attempts": len(cases) * reps * sum(per[c] for c in conditions) * (retries + 1),
        "includes_retries": True,
        "no_embedding_api_calls": True,
    }


def metadata(args, cases):
    protocol = ROOT / "docs/evaluation-protocol-v4.md"
    if not protocol.exists():
        raise RuntimeError("Protocol is missing; commit it before running evaluation")
    protocol_commit = git("log", "-1", "--format=%H", "--", "docs/evaluation-protocol-v4.md")
    if not protocol_commit or git("diff", "HEAD", "--", "docs/evaluation-protocol-v4.md").strip():
        raise RuntimeError("Protocol must be committed and unchanged")
    jar = Path(os.environ.get("PLANTUML_JAR", ""))
    if not jar.is_file() or sha(jar.read_bytes()) != JAR_SHA:
        raise RuntimeError("Pinned PlantUML JAR unavailable or SHA-256 mismatch")
    version = subprocess.check_output(["java", "-jar", str(jar), "-version"], text=True).splitlines()[0]
    if "1.2026.6" not in version:
        raise RuntimeError("Unexpected PlantUML version")
    prompts = {
        str(p.relative_to(ROOT)).replace("\\", "/"): sha(p.read_bytes())
        for p in sorted((ROOT / "ai_core/prompts").rglob("*.txt"))
    }
    return {
        "schema_version": 4,
        "git_commit": git("rev-parse", "HEAD"),
        "protocol_commit": protocol_commit,
        "protocol_sha256": sha(protocol.read_bytes()),
        "python": platform.python_version(),
        "platform": platform.system(),
        "packages": {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},
        "plantuml_version": version,
        "plantuml_jar_sha256": JAR_SHA,
        "prompt_hashes": prompts,
        "model_critic": args.model_critic,
        "model_healer": args.model_healer,
        "seed": args.seed,
        "input_sha256": sha(json.dumps(cases, sort_keys=True).encode()),
        "config": {k: v for k, v in vars(args).items() if k not in {"run_dir", "resume"}},
        "compiler_cache": "per-process diagram SHA; measurements reused, repair timing separate from validation",
        "extended_baseline_version": "v4.1-truncated-source-fix; post-test exploratory revision",
        "runtime_source_sha256": {
            str(p.relative_to(ROOT)).replace(chr(92), "/"): sha(p.read_bytes())
            for folder in ["backend/src", "ai_core/src"]
            for p in sorted((ROOT / folder).rglob("*.py"))
        },
        "C5_caveat": "Original prompts and loop; local lexical selection of original four rules replaces historical OpenAI embedding ranking. Not a bit-identical full v2 replication.",
        "pricing_usd_per_million": {
            "input": 0.15,
            "output": 0.60,
            "reference": "https://developers.openai.com/api/docs/models/gpt-4o-mini",
            "verified_date": "2026-10-22",
        },
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
    }


@lru_cache(maxsize=None)
def cached_check(code):
    return check_diagram(code)


def evaluate(case, condition, rep, args, budget):
    original = case["input_plantuml"]
    initial = cached_check(original)
    started = time.perf_counter()
    state = {}
    actions = []
    if condition == "C0":
        output = original
    elif condition in {"C1", "C2"}:
        output, actions = (deterministic_minimal if condition == "C1" else deterministic_extended)(original)
    else:
        config = RepairConfig(
            mode=CONDITIONS[condition],
            use_rules=condition not in {"C3", "C4", "C6"},
            compiler_feedback=condition in {"C4", "C7"},
            healer_sees_srs=condition not in {"C5", "C6"},
            seed=args.seed + rep,
            model_critic=args.model_critic,
            model_healer=args.model_healer,
        )
        agent = UMLRepairAgent(config, validator=cached_check, before_call=budget.reserve)
        state = agent.run(case["srs"], original, True, force_repair=True)
        output = state["current_uml"]
        state["config"] = asdict(config)
    repair_seconds = time.perf_counter() - started
    final = cached_check(output)
    regression = initial["compiler_valid"] is True and final["compiler_valid"] is False
    safe = original if regression else output
    row = {
        **case,
        "condition": condition,
        "condition_name": CONDITIONS[condition],
        "rep": rep,
        "output_plantuml": output,
        "output_sha256": sha(output.encode()),
        "input_sha256": sha(original.encode()),
        "project_valid": final["project_valid"],
        "compiler_valid": final["compiler_valid"],
        "critic_valid": state.get("critic_valid"),
        "agent_status": state.get("agent_status", "not_applicable"),
        "agent_error": state.get("agent_error"),
        "run_status": "budget_stopped" if state.get("budget_stopped") else "completed",
        "terminated_by": state.get("terminated_by", "not_applicable"),
        "repair_attempt_count": state.get("repair_attempt_count", 0),
        "trace": state.get("trace", []),
        "llm_call_count": state.get("llm_call_count", 0),
        "tokens_in": state.get("tokens_in", 0),
        "tokens_out": state.get("tokens_out", 0),
        "first_compiler_valid_iteration": state.get(
            "first_compiler_valid_iteration", 0 if final["compiler_valid"] else None
        ),
        "first_project_valid_iteration": state.get(
            "first_project_valid_iteration", 0 if final["project_valid"] else None
        ),
        "input_validation": initial,
        "output_validation": final,
        "regression": regression,
        "output_if_reverted": safe,
        "compiler_valid_if_reverted": initial["compiler_valid"] if regression else final["compiler_valid"],
        "project_valid_if_reverted": initial["project_valid"] if regression else final["project_valid"],
        "warnings_added": len(set(final["warnings"]) - set(initial["warnings"])),
        "warnings_removed": len(set(initial["warnings"]) - set(final["warnings"])),
        "elapsed_seconds": repair_seconds,
        "elapsed_scope": "repair loop; includes LLM-loop checks but excludes final independent validation; cached checks may be reused",
        "actions": actions,
        "metrics": reference_metrics(case["gold"], output, original) if case["gold"] else None,
        "metrics_if_reverted": reference_metrics(case["gold"], safe, original) if case["gold"] else None,
    }
    return row


def write_outputs(directory, manifest):
    files = sorted((directory / "cases").glob("*.json"))
    rows = [json.loads(p.read_text(encoding="utf-8")) for p in files]
    dump(directory / "results.json", rows)
    columns = [
        "case_id",
        "dataset",
        "condition",
        "rep",
        "project_valid",
        "compiler_valid",
        "critic_valid",
        "agent_status",
        "terminated_by",
        "repair_attempt_count",
        "llm_call_count",
        "elapsed_seconds",
        "tokens_in",
        "tokens_out",
        "regression",
        "compiler_valid_if_reverted",
    ]
    with (directory / "cases.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    manifest["output_hashes"] = {
        str(p.relative_to(directory)).replace("\\", "/"): sha(p.read_bytes())
        for p in directory.rglob("*")
        if p.is_file() and p.name != "manifest.json" and p.suffix != ".tmp"
    }
    dump(directory / "manifest.json", manifest)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conditions", nargs="+", choices=CONDITIONS, default=list(CONDITIONS))
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=["shared", "pure", "semantic"],
        default=["shared", "pure", "semantic"],
    )
    parser.add_argument("--split", choices=["dev", "test"], default="test")
    parser.add_argument("--reps", type=int, default=5)
    parser.add_argument("--seed", type=int, default=1729)
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=ROOT
        / "backend/evaluation/results_v4"
        / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-calls", type=int, default=0)
    parser.add_argument("--max-cost-usd", type=float, default=0)
    parser.add_argument("--model-critic", default="gpt-4o-mini-2024-07-18")
    parser.add_argument("--model-healer", default="gpt-4o-mini-2024-07-18")
    args = parser.parse_args(argv)
    if args.reps < 1 or args.max_calls < 0 or args.max_cost_usd < 0:
        parser.error("Repetitions and budget limits must be non-negative (reps >= 1)")
    cases = load_cases(args.split, args.datasets)
    planned = plan(cases, args.conditions, args.reps)
    print(json.dumps(planned), flush=True)
    if args.dry_run:
        return planned
    paid = any(c not in {"C0", "C1", "C2"} for c in args.conditions)
    if paid and (not os.environ.get("OPENAI_API_KEY") or not args.max_calls or not args.max_cost_usd):
        parser.error("Paid runs require OPENAI_API_KEY and explicit positive --max-calls / --max-cost-usd")
    if paid and any(not m.startswith("gpt-4o-mini") for m in [args.model_critic, args.model_healer]):
        parser.error(
            "This cost bound is only configured for gpt-4o-mini; other models require reviewed pricing bounds"
        )
    directory = args.run_dir.resolve()
    if (directory / "manifest.json").exists() and not args.resume:
        parser.error("Run already exists; use --resume or a new run directory")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "cases").mkdir(exist_ok=True)
    manifest = metadata(args, cases)
    if args.resume and (directory / "manifest.json").exists():
        old = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
        for key in [
            "git_commit",
            "protocol_commit",
            "prompt_hashes",
            "input_sha256",
            "model_critic",
            "model_healer",
            "seed",
        ]:
            if old[key] != manifest[key]:
                raise ValueError("Resume configuration mismatch: " + key)
        manifest = old
    dump(directory / "manifest.json", manifest)
    budget = Budget(directory / "budget.json", args.max_calls, args.max_cost_usd)
    try:
        for condition in args.conditions:
            for rep in range(1, 2 if condition in {"C0", "C1", "C2"} else args.reps + 1):
                for case in cases:
                    path = directory / "cases" / f"{condition}_{case['case_id']}_{rep}.json"
                    if args.resume and path.exists():
                        continue
                    try:
                        row = evaluate(case, condition, rep, args, budget)
                    except BudgetExceeded:
                        manifest["status"] = "budget_stopped"
                        raise
                    dump(path, row)
                    if row["run_status"] == "budget_stopped":
                        manifest["status"] = "budget_stopped"
                        raise BudgetExceeded(
                            "Case interrupted; partial trace saved and excluded from completed-case denominator"
                        )
                    print(
                        f"{condition} {case['case_id']} rep={rep} compiler={row['compiler_valid']} status={row['agent_status']}",
                        flush=True,
                    )
        manifest["status"] = "completed"
    except BudgetExceeded as exc:
        print(str(exc), flush=True)
    finally:
        write_outputs(directory, manifest)
    return manifest


if __name__ == "__main__":
    main()
