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
    project_defined_final_success = final_compile["project_defined_success"]
    plantuml_validated_final_success = final_compile["plantuml_validated_success"]
    return {
        "case_id": case["case_id"],
        "pure_row": case["pure_row"],
        "category": case["category"],
        "description": case["description"],
        "final_success": plantuml_validated_final_success,
        "project_defined_final_success": project_defined_final_success,
        "plantuml_validated_final_success": plantuml_validated_final_success,
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
    project_successes = sum(1 for row in rows if row["project_defined_final_success"])
    plantuml_runtime_available = any(row["plantuml_validated_final_success"] is not None for row in rows)
    plantuml_successes = (
        sum(1 for row in rows if row["plantuml_validated_final_success"])
        if plantuml_runtime_available
        else None
    )
    project_interval = wilson_interval(project_successes, total)
    plantuml_interval = wilson_interval(plantuml_successes, total) if plantuml_successes is not None else None
    return {
        "metadata": execution_metadata(
            benchmark="PURE-derived repair pilot",
            scope=(
                "Preliminary pilot using selected PURE requirement excerpts, "
                "curated reference UML, and controlled injected PlantUML defects. "
                "Project-defined fallback success is reported separately from real PlantUML-runtime success."
            ),
            max_iterations=MAX_ITERATIONS,
            model="none",
            temperature="none",
            run_id=str(uuid.uuid4()),
            case_count=total,
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
            "plantuml_validated_failed_repairs": (total - plantuml_successes) if plantuml_successes is not None else None,
            "plantuml_validated_success_rate": round(plantuml_successes / total, 4) if plantuml_successes is not None else None,
            "plantuml_validated_success_rate_percent": round(plantuml_successes / total * 100, 1) if plantuml_successes is not None else None,
            "mean_class_f1": round(sum(row["reference_metrics"]["class_f1"] for row in rows) / total, 3),
            "mean_relationship_f1": round(sum(row["reference_metrics"]["relationship_f1"] for row in rows) / total, 3),
            "relationship_metric_definition": "source-target endpoint-pair F1; relation type, multiplicity, and labels are not scored",
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
        "cases": rows,
    }


def write_outputs(report: dict) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    fieldnames = [
        "commit_sha",
        "generated_at_utc",
        "python",
        "platform",
        "model",
        "temperature",
        "max_iterations",
        "case_id",
        "pure_row",
        "category",
        "project_defined_final_success",
        "plantuml_validated_final_success",
        "plantuml_runtime_available",
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
                    "commit_sha": report["metadata"]["commit_sha"],
                    "generated_at_utc": report["metadata"]["generated_at_utc"],
                    "python": report["metadata"]["python"],
                    "platform": report["metadata"]["platform"],
                    "model": report["metadata"]["model"],
                    "temperature": report["metadata"]["temperature"],
                    "max_iterations": report["metadata"]["max_iterations"],
                    "case_id": row["case_id"],
                    "pure_row": row["pure_row"],
                    "category": row["category"],
                    "project_defined_final_success": row["project_defined_final_success"],
                    "plantuml_validated_final_success": row["plantuml_validated_final_success"],
                    "plantuml_runtime_available": row["final_compile"].get("plantuml_runtime_available"),
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
        f"- Project-defined fallback repairs: {report['summary']['project_defined_successful_repairs']}/{report['summary']['total_cases']}",
        f"- Project-defined fallback success rate: {report['summary']['project_defined_success_rate_percent']}%",
        f"- Project-defined Wilson 95% CI: {report['project_defined_wilson_95_ci']['lower_percent']}%-{report['project_defined_wilson_95_ci']['upper_percent']}%",
        f"- PlantUML runtime available: {report['summary']['plantuml_runtime_available']}",
        f"- PlantUML-validated repairs: {report['summary']['plantuml_validated_successful_repairs']}",
        f"- PlantUML-validated Wilson 95% CI: {report['plantuml_validated_wilson_95_ci'] if report['plantuml_validated_wilson_95_ci'] is not None else 'not run'}",
        f"- Mean class F1 against reference UML: {report['summary']['mean_class_f1']}",
        f"- Mean relationship F1 against reference UML: {report['summary']['mean_relationship_f1']}",
        "- Relationship metric: source-target endpoint-pair F1; relation type, multiplicity, and labels are not scored.",
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
        "## Case Results",
        "",
        "| Case | PURE row | Category | Project-defined success | PlantUML-validated success | Runtime available | Class F1 | Relationship F1 |",
        "|---|---:|---|---:|---:|---:|---:|---:|",
    ]
    for row in report["cases"]:
        metrics = row["reference_metrics"]
        lines.append(
            f"| {row['case_id']} | {row['pure_row']} | {row['category']} | "
            f"{row['project_defined_final_success']} | {row['plantuml_validated_final_success']} | "
            f"{row['final_compile'].get('plantuml_runtime_available')} | {metrics['class_f1']} | {metrics['relationship_f1']} |"
        )
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    report = build_report()
    write_outputs(report)
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
    print(f"MEAN_CLASS_F1: {report['summary']['mean_class_f1']}")
    print(f"MEAN_RELATIONSHIP_F1: {report['summary']['mean_relationship_f1']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
