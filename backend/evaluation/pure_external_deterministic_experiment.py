"""Run deterministic repair on the preliminary PURE-derived pilot benchmark."""

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

from pure_external_metrics import compare_to_reference
from pure_external_repair_cases import PURE_EXTERNAL_REPAIR_CASES
from repair_benchmark_utils import (
    MAX_ITERATIONS,
    compile_check,
    deterministic_backend_repair,
    execution_metadata,
    wilson_interval,
)


BACKEND_ROOT = Path(__file__).resolve().parents[1]
RESULTS = BACKEND_ROOT / "evaluation" / "results"
OUTPUT_JSON = RESULTS / "pure_external_deterministic_experiment.json"
OUTPUT_CSV = RESULTS / "pure_external_deterministic_experiment.csv"
OUTPUT_MD = RESULTS / "pure_external_deterministic_experiment.md"


def run_case(case: dict) -> dict:
    started = time.perf_counter()
    current = case["plantuml_kodu"]
    iterations = []

    for iteration_no in range(1, MAX_ITERATIONS + 1):
        before = compile_check(current)
        if before["successful"]:
            break
        repaired, actions = deterministic_backend_repair(current)
        after = compile_check(repaired)
        iterations.append(
            {
                "iteration_no": iteration_no,
                "actions": actions,
                "compile_before_success": before["successful"],
                "compile_after_success": after["successful"],
            }
        )
        current = repaired
        if after["successful"] or actions == ["no_supported_repair_action"]:
            break

    final_compile = compile_check(current)
    reference_metrics = compare_to_reference(case["reference_plantuml"], current)
    return {
        "case_id": case["case_id"],
        "pure_row": case["pure_row"],
        "category": case["category"],
        "description": case["description"],
        "final_success": final_compile["successful"],
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "iteration_count": len(iterations),
        "initial_plantuml": case["plantuml_kodu"],
        "reference_plantuml": case["reference_plantuml"],
        "final_plantuml": current,
        "final_errors": final_compile["errors"],
        "final_warnings": final_compile["warnings"],
        "reference_metrics": reference_metrics,
        "iterations": iterations,
    }


def build_report() -> dict:
    rows = [run_case(case) for case in PURE_EXTERNAL_REPAIR_CASES]
    total = len(rows)
    successes = sum(1 for row in rows if row["final_success"])
    interval = wilson_interval(successes, total)
    return {
        "metadata": execution_metadata(
            benchmark="PURE-derived repair pilot",
            scope=(
                "Preliminary pilot using selected PURE requirement excerpts, "
                "curated reference UML, and controlled injected PlantUML defects."
            ),
            max_iterations=MAX_ITERATIONS,
            model="none",
            temperature="none",
            run_id=str(uuid.uuid4()),
            case_count=total,
        ),
        "summary": {
            "total_cases": total,
            "successful_repairs": successes,
            "failed_repairs": total - successes,
            "success_rate": round(successes / total, 4),
            "success_rate_percent": round(successes / total * 100, 1),
            "mean_class_f1": round(sum(row["reference_metrics"]["class_f1"] for row in rows) / total, 3),
            "mean_relationship_f1": round(sum(row["reference_metrics"]["relationship_f1"] for row in rows) / total, 3),
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


def write_outputs(report: dict) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    fieldnames = [
        "case_id",
        "pure_row",
        "category",
        "final_success",
        "iteration_count",
        "elapsed_seconds",
        "class_f1",
        "relationship_f1",
        "missing_classes",
        "extra_classes",
        "missing_relationships",
        "extra_relationships",
        "final_errors",
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in report["cases"]:
            metrics = row["reference_metrics"]
            writer.writerow(
                {
                    "case_id": row["case_id"],
                    "pure_row": row["pure_row"],
                    "category": row["category"],
                    "final_success": row["final_success"],
                    "iteration_count": row["iteration_count"],
                    "elapsed_seconds": row["elapsed_seconds"],
                    "class_f1": metrics["class_f1"],
                    "relationship_f1": metrics["relationship_f1"],
                    "missing_classes": "; ".join(metrics["missing_classes"]),
                    "extra_classes": "; ".join(metrics["extra_classes"]),
                    "missing_relationships": "; ".join(f"{a}->{b}" for a, b in metrics["missing_relationships"]),
                    "extra_relationships": "; ".join(f"{a}->{b}" for a, b in metrics["extra_relationships"]),
                    "final_errors": "; ".join(row["final_errors"]),
                }
            )

    lines = [
        "# PURE-Derived Deterministic Repair Pilot",
        "",
        "This preliminary pilot does not replace the shared S01-S50 benchmark.",
        "It uses selected PURE requirement excerpts, curated reference UML models, and controlled injected PlantUML defects.",
        "",
        "## Summary",
        "",
        f"- Total cases: {report['summary']['total_cases']}",
        f"- Successful repairs: {report['summary']['successful_repairs']}",
        f"- Failed repairs: {report['summary']['failed_repairs']}",
        f"- Success rate: {report['summary']['success_rate_percent']}%",
        f"- Wilson 95% CI: {report['wilson_95_ci']['lower_percent']}%-{report['wilson_95_ci']['upper_percent']}%",
        f"- Mean class F1 against reference UML: {report['summary']['mean_class_f1']}",
        f"- Mean relationship F1 against reference UML: {report['summary']['mean_relationship_f1']}",
        "",
        "## Case Results",
        "",
        "| Case | PURE row | Category | Final success | Class F1 | Relationship F1 |",
        "|---|---:|---|---:|---:|---:|",
    ]
    for row in report["cases"]:
        metrics = row["reference_metrics"]
        lines.append(
            f"| {row['case_id']} | {row['pure_row']} | {row['category']} | "
            f"{row['final_success']} | {metrics['class_f1']} | {metrics['relationship_f1']} |"
        )
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    report = build_report()
    write_outputs(report)
    print(f"JSON: {OUTPUT_JSON}")
    print(f"CSV: {OUTPUT_CSV}")
    print(f"MD: {OUTPUT_MD}")
    print(
        f"SUMMARY: {report['summary']['successful_repairs']}/"
        f"{report['summary']['total_cases']} "
        f"({report['summary']['success_rate_percent']}%)"
    )
    print(f"MEAN_CLASS_F1: {report['summary']['mean_class_f1']}")
    print(f"MEAN_RELATIONSHIP_F1: {report['summary']['mean_relationship_f1']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
