"""Measure the deterministic /api/analyze workload without any LLM calls.

This script intentionally measures the same local function chain used by
`backend/src/api/endpoints.py::tam_analiz_yap`:

    srs_to_plantuml -> validate_ocl -> calculate_semantic_fidelity

It does not call OpenAI, ChatOpenAI, UMLGenerator, or UMLMultiAgentSystem.
The purpose is to document the latency scope of Table IV separately from the
shared LLM repair benchmark in `shared_benchmark_llm_experiment.py`.
"""

from __future__ import annotations

import csv
import json
import statistics
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKEND_SRC = ROOT / "backend" / "src"
RESULTS = ROOT / "backend" / "evaluation" / "results"

sys.path.insert(0, str(BACKEND_SRC))

from evaluators.semantic_eval import calculate_semantic_fidelity  # noqa: E402
from ocl_engine.ocl_validator import validate_ocl  # noqa: E402
from parsers.srs_parser import srs_to_plantuml  # noqa: E402


REQUEST_COUNT = 50
SLA_LIMIT_SECONDS = 15.0
SRS_TEXT = (
    "The UserManager handles user authentication. "
    "The DiagramService generates PlantUML diagrams. "
    "The UserManager uses the DiagramService."
)


def percentile(values: list[float], p: float) -> float:
    """Match backend/src/api/performance.py percentile indexing."""
    if not values:
        return 0.0
    ordered = sorted(values)
    index = int(len(ordered) * p / 100)
    return ordered[min(index, len(ordered) - 1)]


def run_once() -> dict:
    start = time.perf_counter()
    parse_result = srs_to_plantuml(SRS_TEXT)
    uml = parse_result["plantuml_kodu"]
    ocl_result = validate_ocl(uml)
    semantic_result = calculate_semantic_fidelity(SRS_TEXT, uml)
    elapsed_seconds = time.perf_counter() - start

    return {
        "successful": True,
        "duration_seconds": elapsed_seconds,
        "duration_ms": elapsed_seconds * 1000,
        "class_count": parse_result["sinif_sayisi"],
        "relationship_count": len(parse_result["iliskiler"]),
        "ocl_valid": ocl_result["gecerli_mi"],
        "semantic_passed": semantic_result["gecti_mi"],
        "semantic_score": semantic_result["genel_skor"],
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    run_id = str(uuid.uuid4())
    generated_at = datetime.now(timezone.utc).isoformat()

    rows = []
    for request_id in range(1, REQUEST_COUNT + 1):
        try:
            result = run_once()
            error = ""
        except Exception as exc:  # pragma: no cover - kept for experiment logging
            elapsed_seconds = 0.0
            result = {
                "successful": False,
                "duration_seconds": elapsed_seconds,
                "duration_ms": elapsed_seconds,
                "class_count": 0,
                "relationship_count": 0,
                "ocl_valid": False,
                "semantic_passed": False,
                "semantic_score": 0.0,
            }
            error = str(exc)

        rows.append(
            {
                "run_id": run_id,
                "request_id": request_id,
                "measurement_scope": "deterministic_analyze_pipeline_no_llm",
                "successful": result["successful"],
                "duration_ms": round(result["duration_ms"], 3),
                "duration_seconds": round(result["duration_seconds"], 6),
                "sla_passed": result["duration_seconds"] < SLA_LIMIT_SECONDS,
                "class_count": result["class_count"],
                "relationship_count": result["relationship_count"],
                "ocl_valid": result["ocl_valid"],
                "semantic_passed": result["semantic_passed"],
                "semantic_score": result["semantic_score"],
                "error": error,
            }
        )

    successful_rows = [row for row in rows if row["successful"]]
    durations_ms = [float(row["duration_ms"]) for row in successful_rows]
    summary = {
        "run_id": run_id,
        "generated_at": generated_at,
        "measurement_scope": "deterministic_analyze_pipeline_no_llm",
        "request_count": len(rows),
        "successful_count": len(successful_rows),
        "average_ms": round(statistics.mean(durations_ms), 3),
        "min_ms": round(min(durations_ms), 3),
        "max_ms": round(max(durations_ms), 3),
        "p50_ms": round(percentile(durations_ms, 50), 3),
        "p95_ms": round(percentile(durations_ms, 95), 3),
        "p99_ms": round(percentile(durations_ms, 99), 3),
        "sla_limit_seconds": SLA_LIMIT_SECONDS,
        "sla_pass_rate": round(
            sum(1 for row in successful_rows if row["sla_passed"]) / len(rows), 4
        ),
        "llm_calls": 0,
        "notes": [
            "This experiment measures the deterministic workload used by /api/analyze.",
            "It does not measure /api/autonomous-repair or any ChatOpenAI call.",
        ],
    }

    csv_path = RESULTS / "deterministic_analysis_latency_experiment.csv"
    json_path = RESULTS / "deterministic_analysis_latency_experiment.json"
    md_path = RESULTS / "deterministic_analysis_latency_experiment.md"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump({"summary": summary, "rows": rows}, json_file, indent=2)

    md_lines = [
        "# Deterministic /api/analyze Latency Experiment",
        "",
        "This is a reproducible latency check for the non-LLM analyze workload.",
        "It should not be interpreted as LLM repair latency.",
        "",
        "## Summary",
        "",
        f"- Run id: `{summary['run_id']}`",
        f"- Generated at: `{summary['generated_at']}`",
        f"- Measurement scope: `{summary['measurement_scope']}`",
        f"- Request count: {summary['request_count']}",
        f"- Successful count: {summary['successful_count']}",
        f"- Average latency: {summary['average_ms']} ms",
        f"- Min latency: {summary['min_ms']} ms",
        f"- Max latency: {summary['max_ms']} ms",
        f"- P50 latency: {summary['p50_ms']} ms",
        f"- P95 latency: {summary['p95_ms']} ms",
        f"- P99 latency: {summary['p99_ms']} ms",
        f"- SLA pass rate: {summary['sla_pass_rate'] * 100:.1f}%",
        "- LLM calls: 0",
        "",
        "## Scope Note",
        "",
        "The measured chain is:",
        "",
        "```text",
        "srs_to_plantuml -> validate_ocl -> calculate_semantic_fidelity",
        "```",
        "",
        "Real LLM repair evidence is measured separately by",
        "`backend/evaluation/shared_benchmark_llm_experiment.py`.",
    ]
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")
    print(f"MD: {md_path}")
    print(
        "SUMMARY: "
        f"n={summary['request_count']}, "
        f"avg={summary['average_ms']}ms, "
        f"p95={summary['p95_ms']}ms, "
        f"llm_calls={summary['llm_calls']}"
    )


if __name__ == "__main__":
    main()
