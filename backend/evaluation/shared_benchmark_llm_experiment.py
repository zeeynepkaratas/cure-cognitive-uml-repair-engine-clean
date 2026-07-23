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
import platform
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

EVALUATION_ROOT = Path(__file__).resolve().parent
if str(EVALUATION_ROOT) not in sys.path:
    sys.path.insert(0, str(EVALUATION_ROOT))

from deterministic_repair_experiment import wilson_interval
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
    agent_count = response.get("agent_iteration_count")
    if agent_count is not None:
        return max(int(agent_count) - 1, 0)
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
    final_compile_success = bool(final_compile.get("basarili"))
    return {
        "case_id": case["case_id"],
        "category": case["category"],
        "description": case["description"],
        "srs_metni": case["srs_metni"],
        "initial_plantuml": case["plantuml_kodu"],
        "basarili": final_compile_success,
        "api_basarili": response["basarili"],
        "sure_saniye": response.get("sure_saniye", elapsed),
        "wall_time_saniye": elapsed,
        "iterasyon_sayisi": repair_attempt_count(response),
        "agent_iteration_count": response.get("agent_iteration_count"),
        "agent_is_valid": response.get("agent_is_valid"),
        "agent_llm_call_count": response.get("agent_llm_call_count"),
        "final_plantuml": response.get("final_plantuml"),
        "final_compile_success": final_compile_success,
        "final_compile": final_compile,
        "raw_response": response,
    }


def write_partial(rows: list[dict], max_iterations: int) -> None:
    total = len(rows)
    successes = sum(1 for row in rows if row["basarili"])
    partial = {
        "metadata": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "benchmark": "shared S01-S50 invalid PlantUML benchmark",
            "scope": "partial interrupted/ongoing LLM benchmark output; do not report as final paper result",
            "max_iterations": max_iterations,
            "completed_cases": total,
            "openai_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        },
        "summary": {
            "completed_cases": total,
            "successful_repairs_so_far": successes,
            "failed_repairs_so_far": total - successes,
        },
        "cases": rows,
    }
    PARTIAL_JSON.write_text(json.dumps(partial, ensure_ascii=False, indent=2), encoding="utf-8")

    fieldnames = [
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
            f"{row['case_id']} basarili={row['basarili']} "
            f"final_compile={row['final_compile_success']} "
            f"sure_saniye={row['sure_saniye']} "
            f"iterasyon_sayisi={row['iterasyon_sayisi']}"
        )

    total = len(rows)
    successes = sum(1 for row in rows if row["basarili"])
    interval = wilson_interval(successes, total)
    return {
        "metadata": {
            "run_id": str(uuid.uuid4()),
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "repository_path": str(ROOT),
            "python": sys.version,
            "platform": platform.platform(),
            "benchmark": "shared S01-S50 invalid PlantUML benchmark",
            "scope": "real LLM-based /api/autonomous-repair endpoint",
            "max_iterations": max_iterations,
            "openai_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            "total_wall_time_saniye": round(time.perf_counter() - started, 3),
            "protocol_note": "Run once and report the obtained result; do not repeat runs to select a preferred outcome.",
        },
        "summary": {
            "total_cases": total,
            "successful_repairs": successes,
            "failed_repairs": total - successes,
            "success_rate": round(successes / total, 4),
            "success_rate_percent": round(successes / total * 100, 1),
        },
        "wilson_95_ci": {
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
    fieldnames = [
        "case_id",
        "category",
        "description",
        "basarili",
        "sure_saniye",
        "wall_time_saniye",
        "iterasyon_sayisi",
        "agent_iteration_count",
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
                    "case_id": row["case_id"],
                    "category": row["category"],
                    "description": row["description"],
                    "basarili": row["basarili"],
                    "sure_saniye": row["sure_saniye"],
                    "wall_time_saniye": row["wall_time_saniye"],
                    "iterasyon_sayisi": row["iterasyon_sayisi"],
                    "agent_iteration_count": row["agent_iteration_count"],
                    "agent_is_valid": row["agent_is_valid"],
                    "agent_llm_call_count": row["agent_llm_call_count"],
                    "final_errors": format_messages(compile_result.get("normalize_hatalar", [])),
                    "final_warnings": "; ".join((compile_result.get("ocl") or {}).get("uyarilar", [])),
                }
            )


def write_markdown(report: dict) -> None:
    interval = report["wilson_95_ci"]
    lines = [
        "# Shared Benchmark LLM Repair Experiment",
        "",
        "This report evaluates the real LLM-based /api/autonomous-repair endpoint",
        "on the shared S01-S50 invalid PlantUML benchmark.",
        "",
        "## Summary",
        "",
        f"- Total cases: {report['summary']['total_cases']}",
        f"- Successful repairs: {report['summary']['successful_repairs']}",
        f"- Failed repairs: {report['summary']['failed_repairs']}",
        f"- Success rate: {report['summary']['success_rate_percent']}%",
        f"- Wilson 95% CI: {interval['lower_percent']}% - {interval['upper_percent']}%",
        f"- Model: {report['metadata']['openai_model']}",
        f"- Max iterations: {report['metadata']['max_iterations']}",
        "",
        "## Case Results",
        "",
        "| Case | Category | Success | Time (s) | Repair attempts | LLM calls |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in report["cases"]:
        lines.append(
            f"| {row['case_id']} | {row['category']} | {row['basarili']} | "
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
        f"SUMMARY: {report['summary']['successful_repairs']}/"
        f"{report['summary']['total_cases']} "
        f"({report['summary']['success_rate_percent']}%)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
