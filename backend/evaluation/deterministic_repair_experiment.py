"""
Legacy deterministic repair smoke test for the deterministic CURE repair scope.

This script is retained for helper functions and backward-compatible local
checks. It does not provide the main paper evidence for the current revision.
Use `shared_benchmark_deterministic_experiment.py` and
`shared_benchmark_llm_experiment.py` for the shared S01-S50 repair benchmark.
"""

from __future__ import annotations

import csv
import json
import math
import platform
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
SRC_ROOT = BACKEND_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from ocl_engine.error_handler import plantuml_syntax_kontrol  # noqa: E402
from ocl_engine.ocl_validator import validate_ocl  # noqa: E402


MAX_ITERATIONS = 3


@dataclass(frozen=True)
class RepairCase:
    case_id: str
    category: str
    description: str
    initial_plantuml: str
    expected_final_success: bool


def compile_check(plantuml_code: str) -> dict:
    syntax = plantuml_syntax_kontrol(plantuml_code)
    ocl = validate_ocl(plantuml_code)
    errors = syntax["hatalar"] + ocl["hatalar"]
    warnings = ocl["uyarilar"]
    return {
        "successful": syntax["gecerli"] and ocl["gecerli_mi"],
        "syntax_valid": syntax["gecerli"],
        "ocl_valid": ocl["gecerli_mi"],
        "score": ocl["skor"],
        "percent": ocl["yuzde"],
        "errors": errors,
        "warnings": warnings,
        "class_count": ocl["sinif_sayisi"],
        "relationship_count": ocl["iliski_sayisi"],
    }


def deterministic_backend_repair(plantuml_code: str) -> tuple[str, list[str]]:
    """
    Mirrors the local backend's simple repair capability:
    add missing PlantUML boundaries and synthesize one class for empty diagrams.
    More semantic/OCL-like repairs, such as duplicate-class resolution, are left
    unfixed so the log records realistic unsupported cases.
    """
    actions: list[str] = []
    code = plantuml_code.strip()

    if "@startuml" not in code:
        code = "@startuml\n" + code
        actions.append("added_missing_startuml")

    if "@enduml" not in code:
        code = code + "\n@enduml"
        actions.append("added_missing_enduml")

    if "class " not in code:
        code = code.replace("@enduml", "class GeneratedDiagram {}\n@enduml")
        actions.append("inserted_generated_class_for_empty_diagram")

    if not actions:
        actions.append("no_supported_repair_action")

    return code, actions


def wilson_interval(successes: int, total: int, z: float = 1.96) -> dict:
    if total <= 0:
        raise ValueError("total must be positive")
    phat = successes / total
    denominator = 1 + z**2 / total
    center = (phat + z**2 / (2 * total)) / denominator
    margin = z * math.sqrt((phat * (1 - phat) + z**2 / (4 * total)) / total) / denominator
    return {
        "successes": successes,
        "total": total,
        "rate": phat,
        "lower": center - margin,
        "upper": center + margin,
        "z": z,
    }


def repair_cases() -> list[RepairCase]:
    success_cases = [
        ("R01", "missing_startuml", "Missing @startuml around one class", "class UserManager {}\n@enduml"),
        ("R02", "missing_enduml", "Missing @enduml around one class", "@startuml\nclass UserManager {}"),
        ("R03", "missing_both_boundaries", "Missing both PlantUML boundaries", "class DiagramService {}"),
        ("R04", "empty_diagram", "Empty PlantUML diagram", "@startuml\n@enduml"),
        ("R05", "plain_empty_input", "Plain empty input", ""),
        ("R06", "missing_startuml_with_relation", "Missing @startuml with two related classes", "class UserManager {}\nclass DiagramService {}\nUserManager --> DiagramService\n@enduml"),
        ("R07", "missing_enduml_with_relation", "Missing @enduml with two related classes", "@startuml\nclass ParserService {}\nclass ReportService {}\nParserService --> ReportService"),
        ("R08", "missing_both_with_relation", "Missing both boundaries with relation", "class AuthService {}\nclass UserRepository {}\nAuthService --> UserRepository"),
        ("R09", "only_start_token", "Only @startuml token", "@startuml"),
        ("R10", "only_end_token", "Only @enduml token", "@enduml"),
        ("R11", "comment_only", "Comment-only diagram body", "@startuml\n' comment\n@enduml"),
        ("R12", "missing_startuml_pascal_warning", "Missing start with lowercase warning only", "class userManager {}\n@enduml"),
        ("R13", "missing_enduml_isolated_warning", "Missing end with isolated-class warning only", "@startuml\nclass UserManager {}\nclass DiagramService {}"),
        ("R14", "missing_both_god_class_warning", "Missing boundaries with God Class warning", "class HugeService {\n  +m1()\n  +m2()\n  +m3()\n  +m4()\n  +m5()\n  +m6()\n  +m7()\n  +m8()\n  +m9()\n  +m10()\n  +m11()\n}"),
        ("R15", "whitespace_empty", "Whitespace-only input", "   \n   "),
    ]

    fail_cases = [
        ("R16", "duplicate_class", "Duplicate class remains unsupported", "@startuml\nclass UserManager {}\nclass UserManager {}\n@enduml"),
        ("R17", "duplicate_class_missing_start", "Duplicate class with missing start remains unsupported", "class UserManager {}\nclass UserManager {}\n@enduml"),
        ("R18", "duplicate_class_missing_end", "Duplicate class with missing end remains unsupported", "@startuml\nclass DiagramService {}\nclass DiagramService {}"),
        ("R19", "duplicate_lowercase", "Duplicate lowercase class remains unsupported", "@startuml\nclass userManager {}\nclass userManager {}\n@enduml"),
        ("R20", "duplicate_with_relation", "Duplicate class with relation remains unsupported", "@startuml\nclass AuthService {}\nclass AuthService {}\nclass UserRepository {}\nAuthService --> UserRepository\n@enduml"),
    ]

    return [
        RepairCase(case_id, category, description, plantuml, True)
        for case_id, category, description, plantuml in success_cases
    ] + [
        RepairCase(case_id, category, description, plantuml, False)
        for case_id, category, description, plantuml in fail_cases
    ]


def run_case(case: RepairCase) -> dict:
    start = time.perf_counter()
    current = case.initial_plantuml
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

        if after["successful"]:
            break

        if actions == ["no_supported_repair_action"]:
            break

    final_compile = compile_check(current)
    elapsed = round(time.perf_counter() - start, 6)
    passed_expectation = final_compile["successful"] == case.expected_final_success

    return {
        "case_id": case.case_id,
        "category": case.category,
        "description": case.description,
        "expected_final_success": case.expected_final_success,
        "final_success": final_compile["successful"],
        "expectation_matched": passed_expectation,
        "iteration_count": len(iterations),
        "elapsed_seconds": elapsed,
        "initial_plantuml": case.initial_plantuml,
        "final_plantuml": current,
        "final_compile": final_compile,
        "iterations": iterations,
    }


def write_csv(path: Path, cases: list[dict]) -> None:
    fieldnames = [
        "case_id",
        "category",
        "description",
        "expected_final_success",
        "final_success",
        "expectation_matched",
        "iteration_count",
        "elapsed_seconds",
        "final_errors",
        "final_warnings",
        "final_percent",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for case in cases:
            writer.writerow(
                {
                    "case_id": case["case_id"],
                    "category": case["category"],
                    "description": case["description"],
                    "expected_final_success": case["expected_final_success"],
                    "final_success": case["final_success"],
                    "expectation_matched": case["expectation_matched"],
                    "iteration_count": case["iteration_count"],
                    "elapsed_seconds": case["elapsed_seconds"],
                    "final_errors": "; ".join(case["final_compile"]["errors"]),
                    "final_warnings": "; ".join(case["final_compile"]["warnings"]),
                    "final_percent": case["final_compile"]["percent"],
                }
            )


def write_markdown(path: Path, report: dict) -> None:
    interval = report["wilson_95_ci"]
    lines = [
        "# Legacy Deterministic Backend Repair Smoke Test",
        "",
        "This legacy 20-case smoke test is retained for development checks.",
        "It is not the main repair evidence for the current paper revision.",
        "Use the shared S01-S50 benchmark results for reported repair rates.",
        "",
        "## Summary",
        "",
        f"- Run id: `{report['metadata']['run_id']}`",
        f"- Generated at: `{report['metadata']['generated_at_utc']}`",
        f"- Scope: {report['metadata']['scope']}",
        f"- Repair engine: {report['metadata']['repair_engine']}",
        f"- Total cases: {report['summary']['total_cases']}",
        f"- Successful repairs: {report['summary']['successful_repairs']}",
        f"- Success rate: {report['summary']['success_rate_percent']}%",
        f"- Wilson 95% CI: {interval['lower_percent']}% - {interval['upper_percent']}%",
        f"- Expectation checks passed: {report['summary']['expectation_matches']}/{report['summary']['total_cases']}",
        "",
        "## Case Results",
        "",
        "| Case | Category | Final success | Iterations | Final errors |",
        "|---|---|---:|---:|---|",
    ]

    for case in report["cases"]:
        errors = "; ".join(case["final_compile"]["errors"]) or "-"
        lines.append(
            f"| {case['case_id']} | {case['category']} | {case['final_success']} | "
            f"{case['iteration_count']} | {errors} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This legacy result should not be reported as the current paper's main repair result.",
            "The current revision reports the shared S01-S50 benchmark instead:",
            "deterministic repair 31/50 (62.0%) and LLM autonomous repair 47/50 (94.0%).",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_report() -> dict:
    cases = [run_case(case) for case in repair_cases()]
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
            "scope": "backend/src/ocl_engine structural validation and deterministic local repair",
            "repair_engine": "deterministic_backend_repair; no LLM or external API calls",
            "max_iterations": MAX_ITERATIONS,
        },
        "summary": {
            "total_cases": total,
            "successful_repairs": successes,
            "failed_repairs": total - successes,
            "success_rate": round(successes / total, 4),
            "success_rate_percent": round(successes / total * 100, 1),
            "expectation_matches": sum(1 for case in cases if case["expectation_matched"]),
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


def main() -> None:
    report = build_report()
    output_dir = BACKEND_ROOT / "evaluation" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "deterministic_repair_experiment.json"
    csv_path = output_dir / "deterministic_repair_experiment.csv"
    md_path = output_dir / "deterministic_repair_experiment.md"

    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(csv_path, report["cases"])
    write_markdown(md_path, report)

    print(f"JSON: {json_path}")
    print(f"CSV: {csv_path}")
    print(f"MD: {md_path}")
    print(
        f"SUMMARY: {report['summary']['successful_repairs']}/"
        f"{report['summary']['total_cases']} "
        f"({report['summary']['success_rate_percent']}%)"
    )


if __name__ == "__main__":
    main()
