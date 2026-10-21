"""Run real LLM repair on the shared S01-S50 benchmark.

This script intentionally refuses to run without OPENAI_API_KEY. It should be
executed once for the reported benchmark protocol, and the raw CSV/JSON outputs
should be preserved with the paper artifact.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
import time
import uuid
from pathlib import Path

EVALUATION_ROOT = Path(__file__).resolve().parent
if str(EVALUATION_ROOT) not in sys.path:
    sys.path.insert(0, str(EVALUATION_ROOT))

from repair_benchmark_utils import execution_metadata, wilson_interval
from shared_repair_benchmark_cases import SHARED_REPAIR_BENCHMARK_CASES


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
AI_CORE = ROOT / "ai_core" / "src"
RESULTS = BACKEND / "evaluation" / "results"
OUTPUT_JSON = RESULTS / "shared_benchmark_llm_experiment.json"
OUTPUT_CSV = RESULTS / "shared_benchmark_llm_experiment.csv"
OUTPUT_MD = RESULTS / "shared_benchmark_llm_experiment.md"
PARTIAL_JSON = RESULTS / "shared_benchmark_llm_experiment.partial.json"
PARTIAL_CSV = RESULTS / "shared_benchmark_llm_experiment.partial.csv"


def configure_paths() -> None:
    sys.path.insert(0, str(EVALUATION_ROOT))
    sys.path.insert(0, str(BACKEND))
    sys.path.insert(0, str(AI_CORE))


def require_openai_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY bulunamadi. Bu script gercek /api/autonomous-repair "
            "LLM cagrilari icin API anahtari gerektirir; sonuc uretmedi."
        )


def repair_attempt_count(response: dict) -> int:
    explicit_count = response.get("agent_repair_attempt_count")
    if explicit_count is not None:
        return int(explicit_count)
    agent_count = response.get("agent_iteration_count")
    if agent_count is not None:
        return int(agent_count)
    return max(len(response.get("iterasyonlar", [])) - 1, 0)


def format_messages(items: list) -> str:
    messages = []
    for item in items:
        if isinstance(item, str):
            messages.append(item)
        elif isinstance(item, dict):
            messages.append(item.get("mesaj") or json.dumps(item, ensure_ascii=False))
        else:
            messages.append(str(item))
    return "; ".join(messages)


def run_case(case: dict, max_iterations: int) -> dict:
    from src.api.endpoints import AutonomousRepairRequest, autonomous_repair

    started = time.perf_counter()
    response = autonomous_repair(
        AutonomousRepairRequest(
            plantuml_kodu=case["plantuml_kodu"],
            srs_metni=case["srs_metni"],
            max_iterations=max_iterations,
        )
    )
    elapsed = round(time.perf_counter() - started, 3)
    final_compile = response.get("final_compile") or {}
    project_defined_success = bool(
        final_compile.get("project_defined_success", final_compile.get("basarili"))
    )
    plantuml_validated_success = final_compile.get("plantuml_validated_success")
    return {
        "case_id": case["case_id"],
        "category": case["category"],
        "description": case["description"],
        "srs_metni": case["srs_metni"],
        "initial_plantuml": case["plantuml_kodu"],
        "basarili": plantuml_validated_success,
        "project_defined_basarili": project_defined_success,
        "plantuml_validated_basarili": plantuml_validated_success,
        "api_basarili": response["basarili"],
        "sure_saniye": response.get("sure_saniye", elapsed),
        "wall_time_saniye": elapsed,
        "iterasyon_sayisi": repair_attempt_count(response),
        "agent_iteration_count": response.get("agent_iteration_count"),
        "agent_repair_attempt_count": response.get("agent_repair_attempt_count"),
        "agent_is_valid": response.get("agent_is_valid"),
        "agent_llm_call_count": response.get("agent_llm_call_count"),
        "final_plantuml": response.get("final_plantuml"),
        "final_compile_success": plantuml_validated_success,
        "project_defined_final_compile_success": project_defined_success,
        "plantuml_validated_final_compile_success": plantuml_validated_success,
        "final_compile": final_compile,
        "raw_response": response,
    }


def write_partial(rows: list[dict], max_iterations: int) -> None:
    total = len(rows)
    successes = sum(1 for row in rows if row["project_defined_basarili"])
    partial_metadata = execution_metadata(
        benchmark="shared S01-S50 invalid PlantUML benchmark",
        scope="partial interrupted/ongoing LLM benchmark output; do not report as final paper result",
        max_iterations=max_iterations,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0")),
        completed_cases=total,
    )
    partial = {
        "metadata": partial_metadata,
        "summary": {
            "completed_cases": total,
            "successful_repairs_so_far": successes,
            "failed_repairs_so_far": total - successes,
        },
        "cases": rows,
    }
    PARTIAL_JSON.write_text(json.dumps(partial, ensure_ascii=False, indent=2), encoding="utf-8")

    fieldnames = [
        "commit_sha",
        "generated_at_utc",
        "python",
        "platform",
        "model",
        "temperature",
        "max_iterations",
        "case_id",
        "category",
        "description",
        "basarili",
        "api_basarili",
        "final_compile_success",
        "sure_saniye",
        "wall_time_saniye",
        "iterasyon_sayisi",
        "agent_iteration_count",
        "agent_repair_attempt_count",
        "agent_is_valid",
        "agent_llm_call_count",
        "final_errors",
        "final_warnings",
    ]
    with PARTIAL_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            compile_result = row.get("final_compile") or {}
            row_for_csv = {field: row.get(field) for field in fieldnames}
            row_for_csv.update(
                {
                    "commit_sha": partial_metadata["commit_sha"],
                    "generated_at_utc": partial_metadata["generated_at_utc"],
                    "python": partial_metadata["python"],
                    "platform": partial_metadata["platform"],
                    "model": partial_metadata["model"],
                    "temperature": partial_metadata["temperature"],
                    "max_iterations": partial_metadata["max_iterations"],
                }
            )
            row_for_csv["final_errors"] = format_messages(compile_result.get("normalize_hatalar", []))
            row_for_csv["final_warnings"] = "; ".join((compile_result.get("ocl") or {}).get("uyarilar", []))
            writer.writerow(row_for_csv)


def build_report(max_iterations: int) -> dict:
    rows = []
    started = time.perf_counter()
    for index, case in enumerate(SHARED_REPAIR_BENCHMARK_CASES, start=1):
        row = run_case(case, max_iterations=max_iterations)
        rows.append(row)
        write_partial(rows, max_iterations=max_iterations)
        print(
            f"{index:02d}/{len(SHARED_REPAIR_BENCHMARK_CASES)} "
            f"{row['case_id']} project_defined_basarili={row['project_defined_basarili']} "
            f"plantuml_validated_basarili={row['plantuml_validated_basarili']} "
            f"sure_saniye={row['sure_saniye']} "
            f"iterasyon_sayisi={row['iterasyon_sayisi']}"
        )

    total = len(rows)
    project_successes = sum(1 for row in rows if row["project_defined_basarili"])
    plantuml_runtime_available = any(
        (row.get("final_compile") or {}).get("plantuml_runtime_available") for row in rows
    )
    plantuml_successes = (
        sum(1 for row in rows if row["plantuml_validated_basarili"]) if plantuml_runtime_available else None
    )
    agent_terminal_valid = sum(1 for row in rows if row.get("agent_is_valid") is True)
    both_final_and_agent_valid = sum(
        1 for row in rows if row["project_defined_basarili"] and row.get("agent_is_valid") is True
    )
    final_valid_agent_invalid = sum(
        1 for row in rows if row["project_defined_basarili"] and row.get("agent_is_valid") is not True
    )
    interval = wilson_interval(project_successes, total)
    return {
        "metadata": execution_metadata(
            benchmark="shared S01-S50 invalid PlantUML benchmark",
            scope="real LLM-based /api/autonomous-repair endpoint",
            max_iterations=max_iterations,
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0")),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            run_id=str(uuid.uuid4()),
            repository_path=str(ROOT),
            total_wall_time_saniye=round(time.perf_counter() - started, 3),
            protocol_note="Run once and report the obtained result; do not repeat runs to select a preferred outcome.",
        ),
        "summary": {
            "total_cases": total,
            "success_definition": "project-defined fallback validation is separate from real PlantUML-runtime validation",
            "plantuml_runtime_available": plantuml_runtime_available,
            "project_defined_successful_repairs": project_successes,
            "project_defined_failed_repairs": total - project_successes,
            "project_defined_success_rate": round(project_successes / total, 4),
            "project_defined_success_rate_percent": round(project_successes / total * 100, 1),
            "plantuml_validated_successful_repairs": plantuml_successes,
            "plantuml_validated_failed_repairs": (total - plantuml_successes)
            if plantuml_successes is not None
            else None,
            "plantuml_validated_success_rate": round(plantuml_successes / total, 4)
            if plantuml_successes is not None
            else None,
            "plantuml_validated_success_rate_percent": round(plantuml_successes / total * 100, 1)
            if plantuml_successes is not None
            else None,
            "agent_terminal_valid": agent_terminal_valid,
            "both_final_compile_and_agent_terminal_valid": both_final_and_agent_valid,
            "final_compile_valid_but_agent_terminal_invalid": final_valid_agent_invalid,
        },
        "project_defined_wilson_95_ci": {
            "successes": interval["successes"],
            "total": interval["total"],
            "rate": round(interval["rate"], 4),
            "lower": round(interval["lower"], 4),
            "upper": round(interval["upper"], 4),
            "lower_percent": round(interval["lower"] * 100, 1),
            "upper_percent": round(interval["upper"] * 100, 1),
            "z": interval["z"],
        },
        "cases": rows,
    }


def write_csv(report: dict) -> None:
    metadata = report["metadata"]
    fieldnames = [
        "commit_sha",
        "generated_at_utc",
        "python",
        "platform",
        "model",
        "temperature",
        "max_iterations",
        "case_id",
        "category",
        "description",
        "basarili",
        "project_defined_basarili",
        "plantuml_validated_basarili",
        "project_defined_final_compile_success",
        "plantuml_validated_final_compile_success",
        "sure_saniye",
        "wall_time_saniye",
        "iterasyon_sayisi",
        "agent_iteration_count",
        "agent_repair_attempt_count",
        "agent_is_valid",
        "agent_llm_call_count",
        "final_errors",
        "final_warnings",
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in report["cases"]:
            compile_result = row.get("final_compile") or {}
            writer.writerow(
                {
                    "commit_sha": metadata["commit_sha"],
                    "generated_at_utc": metadata["generated_at_utc"],
                    "python": metadata["python"],
                    "platform": metadata["platform"],
                    "model": metadata["model"],
                    "temperature": metadata["temperature"],
                    "max_iterations": metadata["max_iterations"],
                    "case_id": row["case_id"],
                    "category": row["category"],
                    "description": row["description"],
                    "basarili": row["basarili"],
                    "project_defined_basarili": row["project_defined_basarili"],
                    "plantuml_validated_basarili": row["plantuml_validated_basarili"],
                    "project_defined_final_compile_success": row["project_defined_final_compile_success"],
                    "plantuml_validated_final_compile_success": row[
                        "plantuml_validated_final_compile_success"
                    ],
                    "sure_saniye": row["sure_saniye"],
                    "wall_time_saniye": row["wall_time_saniye"],
                    "iterasyon_sayisi": row["iterasyon_sayisi"],
                    "agent_iteration_count": row["agent_iteration_count"],
                    "agent_repair_attempt_count": row["agent_repair_attempt_count"],
                    "agent_is_valid": row["agent_is_valid"],
                    "agent_llm_call_count": row["agent_llm_call_count"],
                    "final_errors": format_messages(compile_result.get("normalize_hatalar", [])),
                    "final_warnings": "; ".join((compile_result.get("ocl") or {}).get("uyarilar", [])),
                }
            )


def write_markdown(report: dict) -> None:
    interval = report["project_defined_wilson_95_ci"]
    lines = [
        "# Shared Benchmark LLM Repair Experiment",
        "",
        "This report evaluates the real LLM-based /api/autonomous-repair endpoint",
        "on the shared S01-S50 invalid PlantUML benchmark.",
        "",
        "## Summary",
        "",
        f"- Total cases: {report['summary']['total_cases']}",
        f"- Project-defined fallback repairs: {report['summary']['project_defined_successful_repairs']}/{report['summary']['total_cases']}",
        f"- Project-defined fallback success rate: {report['summary']['project_defined_success_rate_percent']}%",
        f"- Project-defined Wilson 95% CI: {interval['lower_percent']}% - {interval['upper_percent']}%",
        f"- PlantUML runtime available: {report['summary']['plantuml_runtime_available']}",
        f"- PlantUML-validated repairs: {report['summary']['plantuml_validated_successful_repairs']}",
        f"- Agent terminal-state valid: {report['summary']['agent_terminal_valid']}",
        f"- Final-valid and agent-terminal-valid: {report['summary']['both_final_compile_and_agent_terminal_valid']}",
        f"- Final-valid but agent-terminal-invalid: {report['summary']['final_compile_valid_but_agent_terminal_invalid']}",
        f"- Model: {report['metadata']['openai_model']}",
        f"- Max iterations: {report['metadata']['max_iterations']}",
        "",
        "## Execution Metadata",
        "",
        f"- Commit SHA: `{report['metadata']['commit_sha']}`",
        f"- Generated at UTC: `{report['metadata']['generated_at_utc']}`",
        f"- Python: `{report['metadata']['python']}`",
        f"- Platform: `{report['metadata']['platform']}`",
        f"- Model: `{report['metadata']['model']}`",
        f"- Temperature: `{report['metadata']['temperature']}`",
        f"- Max iterations: `{report['metadata']['max_iterations']}`",
        "",
        "Project-defined fallback success must not be reported as a real PlantUML-runtime-validated success rate.",
        "",
        "Success is defined by the endpoint's final syntax/OCL validation. The",
        "`agent_is_valid` field is a secondary LangGraph terminal-state diagnostic",
        "from the internal Critic-Healer loop and should not be interpreted as the",
        "primary repair-success criterion.",
        "Because the Critic receives a strict prompt and fixed curated OCL-rule",
        "retrieval context, this field may reflect retrieval-rule mismatch or",
        "over-strict Critic behavior rather than independent semantic correctness.",
        "",
        "## Case Results",
        "",
        "| Case | Category | Project-defined success | PlantUML-validated success | Time (s) | Repair attempts | LLM calls |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in report["cases"]:
        lines.append(
            f"| {row['case_id']} | {row['category']} | "
            f"{row['project_defined_basarili']} | {row['plantuml_validated_basarili']} | "
            f"{row['sure_saniye']} | {row['iterasyon_sayisi']} | "
            f"{row['agent_llm_call_count']} |"
        )
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-iterations", type=int, default=3, choices=range(1, 6))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_openai_key()
    configure_paths()
    logging.disable(logging.WARNING)
    RESULTS.mkdir(parents=True, exist_ok=True)
    report = build_report(max_iterations=args.max_iterations)
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(report)
    write_markdown(report)
    print(f"JSON: {OUTPUT_JSON}")
    print(f"CSV: {OUTPUT_CSV}")
    print(f"MD: {OUTPUT_MD}")
    print(
        f"SUMMARY_PROJECT_DEFINED: {report['summary']['project_defined_successful_repairs']}/"
        f"{report['summary']['total_cases']} "
        f"({report['summary']['project_defined_success_rate_percent']}%)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
