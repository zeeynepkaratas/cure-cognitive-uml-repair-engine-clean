"""Run deterministic repair on the shared S01-S50 benchmark.

This script is LLM-free and reproducible. It uses the same benchmark cases as
the LLM script, which makes the deterministic and LLM repair layers directly
comparable when both result files are available.
"""

from __future__ import annotations

import csv
import json
import platform
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

EVALUATION_ROOT = Path(__file__).resolve().parent
if str(EVALUATION_ROOT) not in sys.path:
    sys.path.insert(0, str(EVALUATION_ROOT))

from deterministic_repair_experiment import (
    MAX_ITERATIONS,
    compile_check,
    deterministic_backend_repair,
    wilson_interval,
)
from shared_repair_benchmark_cases import SHARED_REPAIR_BENCHMARK_CASES


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
RESULTS = BACKEND_ROOT / "evaluation" / "results"
OUTPUT_JSON = RESULTS / "shared_benchmark_deterministic_experiment.json"
OUTPUT_CSV = RESULTS / "shared_benchmark_deterministic_experiment.csv"
OUTPUT_MD = RESULTS / "shared_benchmark_deterministic_experiment.md"


def run_case(case: dict) -> dict:
    started = time.perf_counter()
    current = case["plantuml_kodu"]
    initial_compile = compile_check(current)
    iterations = []

    for iteration_no in range(1, MAX_ITERATIONS + 1):
        before = compile_check(current)
        row = {
            "iteration_no": iteration_no,
            "input_plantuml": current,
            "compile_before": before,
            "repair_actions": [],
            "output_plantuml": current,
            "compile_after": before,
        }

        if before["successful"]:
            iterations.append(row)
            break

        repaired, actions = deterministic_backend_repair(current)
        after = compile_check(repaired)
        row["repair_actions"] = actions
        row["output_plantuml"] = repaired
        row["compile_after"] = after
        iterations.append(row)
        current = repaired

        if after["successful"] or actions == ["no_supported_repair_action"]:
            break

    final_compile = compile_check(current)
    return {
        "case_id": case["case_id"],
        "category": case["category"],
        "description": case["description"],
        "srs_metni": case["srs_metni"],
        "initial_plantuml": case["plantuml_kodu"],
        "final_plantuml": current,
        "initial_success": initial_compile["successful"],
        "final_success": final_compile["successful"],
        "iteration_count": len(iterations),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "final_compile": final_compile,
        "initial_compile": initial_compile,
        "iterations": iterations,
    }


def build_report() -> dict:
    cases = [run_case(case) for case in SHARED_REPAIR_BENCHMARK_CASES]
    successes = sum(1 for case in cases if case["final_success"])
    total = len(cases)
    interval = wilson_interval(successes, total)
    return {
        "metadata": {
            "run_id": str(uuid.uuid4()),
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "repository_path": str(REPO_ROOT),
            "python": sys.version,
            "platform": platform.platform(),
            "benchmark": "shared S01-S50 invalid PlantUML benchmark",
            "scope": "deterministic backend repair; no LLM or external API calls",
            "max_iterations": MAX_ITERATIONS,
            "total_cases": total,
        },
        "summary": {
            "total_cases": total,
            "initially_invalid_cases": sum(1 for case in cases if not case["initial_success"]),
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
        "cases": cases,
    }


def write_csv(report: dict) -> None:
    fieldnames = [
        "case_id",
        "category",
        "description",
        "final_success",
        "initial_success",
        "iteration_count",
        "elapsed_seconds",
        "final_errors",
        "final_warnings",
        "final_percent",
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for case in report["cases"]:
            writer.writerow(
                {
                    "case_id": case["case_id"],
                    "category": case["category"],
                    "description": case["description"],
                    "final_success": case["final_success"],
                    "initial_success": case["initial_success"],
                    "iteration_count": case["iteration_count"],
                    "elapsed_seconds": case["elapsed_seconds"],
                    "final_errors": "; ".join(case["final_compile"]["errors"]),
                    "final_warnings": "; ".join(case["final_compile"]["warnings"]),
                    "final_percent": case["final_compile"]["percent"],
                }
            )


def write_markdown(report: dict) -> None:
    interval = report["wilson_95_ci"]
    lines = [
        "# Shared Benchmark Deterministic Repair Experiment",
        "",
        "This report evaluates the deterministic backend repair layer on the",
        "shared S01-S50 invalid PlantUML benchmark. The same benchmark is used",
        "by `shared_benchmark_llm_experiment.py` for the LLM-based endpoint.",
        "",
        "## Summary",
        "",
        f"- Total cases: {report['summary']['total_cases']}",
        f"- Initially invalid cases: {report['summary']['initially_invalid_cases']}",
        f"- Successful repairs: {report['summary']['successful_repairs']}",
        f"- Failed repairs: {report['summary']['failed_repairs']}",
        f"- Success rate: {report['summary']['success_rate_percent']}%",
        f"- Wilson 95% CI: {interval['lower_percent']}% - {interval['upper_percent']}%",
        "",
        "## Case Results",
        "",
        "| Case | Category | Initially invalid | Success | Iterations | Final errors |",
        "|---|---|---:|---:|---:|---|",
    ]
    for case in report["cases"]:
        errors = "; ".join(case["final_compile"]["errors"]) or "-"
        lines.append(
            f"| {case['case_id']} | {case['category']} | {not case['initial_success']} | "
            f"{case['final_success']} | {case['iteration_count']} | {errors} |"
        )
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    report = build_report()
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
