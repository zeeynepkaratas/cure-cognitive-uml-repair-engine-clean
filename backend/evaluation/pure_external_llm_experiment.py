"""Run real LLM repair on the preliminary PURE-derived pilot benchmark."""

from __future__ import annotations

import argparse
import csv
import json
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

from pure_external_metrics import compare_to_reference
from pure_external_repair_cases import PURE_EXTERNAL_REPAIR_CASES
from repair_benchmark_utils import execution_metadata, wilson_interval


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
AI_CORE = ROOT / "ai_core" / "src"
RESULTS = BACKEND / "evaluation" / "results"
OUTPUT_JSON = RESULTS / "pure_external_llm_experiment.json"
OUTPUT_CSV = RESULTS / "pure_external_llm_experiment.csv"
OUTPUT_MD = RESULTS / "pure_external_llm_experiment.md"
PARTIAL_JSON = RESULTS / "pure_external_llm_experiment.partial.json"
PARTIAL_CSV = RESULTS / "pure_external_llm_experiment.partial.csv"


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
    final_plantuml = response.get("final_plantuml") or ""
    reference_metrics = compare_to_reference(case["reference_plantuml"], final_plantuml)
    final_compile_success = bool(final_compile.get("basarili"))
    return {
        "case_id": case["case_id"],
        "pure_row": case["pure_row"],
        "category": case["category"],
        "description": case["description"],
        "srs_metni": case["srs_metni"],
        "initial_plantuml": case["plantuml_kodu"],
        "reference_plantuml": case["reference_plantuml"],
        "final_plantuml": final_plantuml,
        "basarili": final_compile_success,
        "api_basarili": response.get("basarili"),
        "sure_saniye": response.get("sure_saniye", elapsed),
        "wall_time_saniye": elapsed,
        "iterasyon_sayisi": repair_attempt_count(response),
        "agent_iteration_count": response.get("agent_iteration_count"),
        "agent_is_valid": response.get("agent_is_valid"),
        "agent_llm_call_count": response.get("agent_llm_call_count"),
        "final_compile": final_compile,
        "reference_metrics": reference_metrics,
        "raw_response": response,
    }


def write_partial(rows: list[dict], max_iterations: int) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    partial_metadata = execution_metadata(
        benchmark="PURE-derived repair pilot",
        scope="partial interrupted/ongoing LLM pilot output; do not report as final paper result",
        max_iterations=max_iterations,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0")),
        completed_cases=len(rows),
    )
    partial = {
        "metadata": partial_metadata,
        "cases": rows,
    }
    PARTIAL_JSON.write_text(json.dumps(partial, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv_rows(PARTIAL_CSV, rows, partial_metadata)


def build_report(max_iterations: int) -> dict:
    rows = []
    started = time.perf_counter()
    for index, case in enumerate(PURE_EXTERNAL_REPAIR_CASES, start=1):
        row = run_case(case, max_iterations=max_iterations)
        rows.append(row)
        write_partial(rows, max_iterations=max_iterations)
        print(
            f"{index:02d}/{len(PURE_EXTERNAL_REPAIR_CASES)} "
            f"{row['case_id']} basarili={row['basarili']} "
            f"sure_saniye={row['sure_saniye']} "
            f"iterasyon_sayisi={row['iterasyon_sayisi']} "
            f"class_f1={row['reference_metrics']['class_f1']} "
            f"rel_f1={row['reference_metrics']['relationship_f1']}"
        )

    total = len(rows)
    successes = sum(1 for row in rows if row["basarili"])
    agent_terminal_valid = sum(1 for row in rows if row.get("agent_is_valid") is True)
    both_final_and_agent_valid = sum(
        1 for row in rows if row["basarili"] and row.get("agent_is_valid") is True
    )
    final_valid_agent_invalid = sum(
        1 for row in rows if row["basarili"] and row.get("agent_is_valid") is not True
    )
    interval = wilson_interval(successes, total)
    return {
        "metadata": execution_metadata(
            benchmark="PURE-derived repair pilot",
            scope="real LLM-based /api/autonomous-repair endpoint on selected PURE-derived pilot cases",
            max_iterations=max_iterations,
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0")),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            run_id=str(uuid.uuid4()),
            total_wall_time_saniye=round(time.perf_counter() - started, 3),
            protocol_note="Run once and report the obtained result; do not repeat runs to select a preferred outcome.",
        ),
        "summary": {
            "total_cases": total,
            "successful_repairs": successes,
            "failed_repairs": total - successes,
            "success_rate": round(successes / total, 4),
            "success_rate_percent": round(successes / total * 100, 1),
            "mean_class_f1": round(sum(row["reference_metrics"]["class_f1"] for row in rows) / total, 3),
            "mean_relationship_f1": round(sum(row["reference_metrics"]["relationship_f1"] for row in rows) / total, 3),
            "agent_terminal_valid": agent_terminal_valid,
            "both_final_compile_and_agent_terminal_valid": both_final_and_agent_valid,
            "final_compile_valid_but_agent_terminal_invalid": final_valid_agent_invalid,
            "success_definition": "final syntax/OCL validation after the autonomous repair endpoint returns",
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


def write_csv_rows(path: Path, rows: list[dict], metadata: dict) -> None:
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
        "basarili",
        "sure_saniye",
        "wall_time_saniye",
        "iterasyon_sayisi",
        "agent_llm_call_count",
        "class_f1",
        "relationship_f1",
        "missing_classes",
        "extra_classes",
        "missing_relationships",
        "extra_relationships",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            metrics = row["reference_metrics"]
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
                    "pure_row": row["pure_row"],
                    "category": row["category"],
                    "basarili": row["basarili"],
                    "sure_saniye": row["sure_saniye"],
                    "wall_time_saniye": row["wall_time_saniye"],
                    "iterasyon_sayisi": row["iterasyon_sayisi"],
                    "agent_llm_call_count": row["agent_llm_call_count"],
                    "class_f1": metrics["class_f1"],
                    "relationship_f1": metrics["relationship_f1"],
                    "missing_classes": "; ".join(metrics["missing_classes"]),
                    "extra_classes": "; ".join(metrics["extra_classes"]),
                    "missing_relationships": "; ".join(f"{a}->{b}" for a, b in metrics["missing_relationships"]),
                    "extra_relationships": "; ".join(f"{a}->{b}" for a, b in metrics["extra_relationships"]),
                }
            )


def write_markdown(report: dict) -> None:
    lines = [
        "# PURE-Derived LLM Repair Pilot",
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
        f"- Agent terminal-state valid: {report['summary']['agent_terminal_valid']}",
        f"- Final-valid and agent-terminal-valid: {report['summary']['both_final_compile_and_agent_terminal_valid']}",
        f"- Final-valid but agent-terminal-invalid: {report['summary']['final_compile_valid_but_agent_terminal_invalid']}",
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
        "| Case | PURE row | Category | Final success | Class F1 | Relationship F1 | LLM calls |",
        "|---|---:|---|---:|---:|---:|---:|",
    ]
    for row in report["cases"]:
        metrics = row["reference_metrics"]
        lines.append(
            f"| {row['case_id']} | {row['pure_row']} | {row['category']} | "
            f"{row['basarili']} | {metrics['class_f1']} | {metrics['relationship_f1']} | "
            f"{row['agent_llm_call_count']} |"
        )
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-iterations", type=int, default=3)
    args = parser.parse_args()

    configure_paths()
    require_openai_key()
    report = build_report(max_iterations=args.max_iterations)
    RESULTS.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv_rows(OUTPUT_CSV, report["cases"], report["metadata"])
    write_markdown(report)
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
