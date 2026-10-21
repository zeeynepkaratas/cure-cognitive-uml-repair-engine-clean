"""Run deterministic repair on the shared S01-S50 benchmark.

This script is LLM-free and reproducible. It uses the same benchmark cases as
the LLM script, which makes the deterministic and LLM repair layers directly
comparable when both result files are available.
"""

from __future__ import annotations

import csv
import json
import sys
import time
import uuid
from pathlib import Path

EVALUATION_ROOT = Path(__file__).resolve().parent
if str(EVALUATION_ROOT) not in sys.path:
    sys.path.insert(0, str(EVALUATION_ROOT))

from repair_benchmark_utils import (
    MAX_ITERATIONS,
    compile_check,
    deterministic_backend_repair,
    execution_metadata,
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
    initial_project_success = initial_compile["project_defined_success"]
    final_project_success = final_compile["project_defined_success"]
    final_plantuml_success = final_compile["plantuml_validated_success"]
    return {
        "case_id": case["case_id"],
        "category": case["category"],
        "description": case["description"],
        "srs_metni": case["srs_metni"],
        "initial_plantuml": case["plantuml_kodu"],
        "final_plantuml": current,
        "initial_success": initial_project_success,
        "final_success": final_plantuml_success,
        "project_defined_initial_success": initial_project_success,
        "project_defined_final_success": final_project_success,
        "plantuml_validated_final_success": final_plantuml_success,
        "iteration_count": len(iterations),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "final_compile": final_compile,
        "initial_compile": initial_compile,
        "iterations": iterations,
    }


def build_report() -> dict:
    cases = [run_case(case) for case in SHARED_REPAIR_BENCHMARK_CASES]
    total = len(cases)
    project_successes = sum(1 for case in cases if case["project_defined_final_success"])
    plantuml_runtime_available = any(case["final_compile"]["plantuml_runtime_available"] for case in cases)
    plantuml_successes = (
        sum(1 for case in cases if case["plantuml_validated_final_success"])
        if plantuml_runtime_available
        else None
    )
    project_interval = wilson_interval(project_successes, total)
    plantuml_interval = wilson_interval(plantuml_successes, total) if plantuml_successes is not None else None
    return {
        "metadata": execution_metadata(
            benchmark="shared S01-S50 invalid PlantUML benchmark",
            scope="deterministic backend repair; no LLM calls; reports project-defined fallback success separately from real PlantUML-runtime success",
            max_iterations=MAX_ITERATIONS,
            model="none",
            temperature="none",
            run_id=str(uuid.uuid4()),
            repository_path=str(REPO_ROOT),
            total_cases=total,
        ),
        "summary": {
            "total_cases": total,
            "initially_invalid_cases": sum(1 for case in cases if not case["initial_success"]),
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
        },
        "project_defined_wilson_95_ci": {
            "successes": project_interval["successes"],
            "total": project_interval["total"],
            "rate": round(project_interval["rate"], 4),
            "lower": round(project_interval["lower"], 4),
            "upper": round(project_interval["upper"], 4),
            "lower_percent": round(project_interval["lower"] * 100, 1),
            "upper_percent": round(project_interval["upper"] * 100, 1),
            "z": project_interval["z"],
        },
        "plantuml_validated_wilson_95_ci": None
        if plantuml_interval is None
        else {
            "successes": plantuml_interval["successes"],
            "total": plantuml_interval["total"],
            "rate": round(plantuml_interval["rate"], 4),
            "lower": round(plantuml_interval["lower"], 4),
            "upper": round(plantuml_interval["upper"], 4),
            "lower_percent": round(plantuml_interval["lower"] * 100, 1),
            "upper_percent": round(plantuml_interval["upper"] * 100, 1),
            "z": plantuml_interval["z"],
        },
        "cases": cases,
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
        "project_defined_final_success",
        "plantuml_validated_final_success",
        "project_defined_initial_success",
        "plantuml_runtime_available",
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
                    "commit_sha": metadata["commit_sha"],
                    "generated_at_utc": metadata["generated_at_utc"],
                    "python": metadata["python"],
                    "platform": metadata["platform"],
                    "model": metadata["model"],
                    "temperature": metadata["temperature"],
                    "max_iterations": metadata["max_iterations"],
                    "case_id": case["case_id"],
                    "category": case["category"],
                    "description": case["description"],
                    "project_defined_final_success": case["project_defined_final_success"],
                    "plantuml_validated_final_success": case["plantuml_validated_final_success"],
                    "project_defined_initial_success": case["project_defined_initial_success"],
                    "plantuml_runtime_available": case["final_compile"]["plantuml_runtime_available"],
                    "iteration_count": case["iteration_count"],
                    "elapsed_seconds": case["elapsed_seconds"],
                    "final_errors": "; ".join(case["final_compile"]["errors"]),
                    "final_warnings": "; ".join(case["final_compile"]["warnings"]),
                    "final_percent": case["final_compile"]["percent"],
                }
            )


def write_markdown(report: dict) -> None:
    interval = report["project_defined_wilson_95_ci"]
    metadata = report["metadata"]
    plantuml_ci = report["plantuml_validated_wilson_95_ci"]
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
        f"- Project-defined fallback repairs: {report['summary']['project_defined_successful_repairs']}/{report['summary']['total_cases']}",
        f"- Project-defined fallback success rate: {report['summary']['project_defined_success_rate_percent']}%",
        f"- Project-defined Wilson 95% CI: {interval['lower_percent']}% - {interval['upper_percent']}%",
        f"- PlantUML runtime available: {report['summary']['plantuml_runtime_available']}",
        f"- PlantUML-validated repairs: {report['summary']['plantuml_validated_successful_repairs']}",
        f"- PlantUML-validated Wilson 95% CI: {plantuml_ci if plantuml_ci is not None else 'not run'}",
        "",
        "The project-defined fallback result is based on the repository's lightweight syntax/OCL-like checks.",
        "It must not be reported as a real PlantUML-runtime-validated success rate.",
        "",
        "## Execution Metadata",
        "",
        f"- Commit SHA: `{metadata['commit_sha']}`",
        f"- Generated at UTC: `{metadata['generated_at_utc']}`",
        f"- Python: `{metadata['python']}`",
        f"- Platform: `{metadata['platform']}`",
        f"- Model: `{metadata['model']}`",
        f"- Temperature: `{metadata['temperature']}`",
        f"- Max iterations: `{metadata['max_iterations']}`",
        "",
        "## Case Results",
        "",
        "| Case | Category | Initially invalid | Project-defined success | PlantUML-validated success | Runtime available | Iterations | Final errors |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for case in report["cases"]:
        errors = "; ".join(case["final_compile"]["errors"]) or "-"
        lines.append(
            f"| {case['case_id']} | {case['category']} | {not case['initial_success']} | "
            f"{case['project_defined_final_success']} | {case['plantuml_validated_final_success']} | "
            f"{case['final_compile']['plantuml_runtime_available']} | {case['iteration_count']} | {errors} |"
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
        f"SUMMARY_PROJECT_DEFINED: {report['summary']['project_defined_successful_repairs']}/"
        f"{report['summary']['total_cases']} "
        f"({report['summary']['project_defined_success_rate_percent']}%)"
    )
    if report["summary"]["plantuml_validated_successful_repairs"] is None:
        print("SUMMARY_PLANTUML_VALIDATED: not run (PlantUML runtime unavailable)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
