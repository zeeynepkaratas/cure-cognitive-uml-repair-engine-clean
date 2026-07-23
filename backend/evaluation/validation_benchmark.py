"""
Backend validation benchmark.

This script produces reproducible evidence for the backend-owned validation
layer: `src/ocl_engine` and `src/evaluators`. It does not call LLM services and
does not claim to reproduce the paper's autonomous repair success experiment.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from src.evaluators.semantic_eval import calculate_semantic_fidelity
from src.ocl_engine.ocl_validator import validate_ocl


OCL_CASES = [
    {
        "id": "ocl_01_missing_start",
        "description": "Missing @startuml tag",
        "plantuml": "class UserManager {}\n@enduml",
        "expected_valid": False,
        "expected_error_contains": ["@startuml etiketi eksik"],
        "expected_warning_contains": [],
    },
    {
        "id": "ocl_02_missing_end",
        "description": "Missing @enduml tag",
        "plantuml": "@startuml\nclass UserManager {}",
        "expected_valid": False,
        "expected_error_contains": ["@enduml etiketi eksik"],
        "expected_warning_contains": [],
    },
    {
        "id": "ocl_03_empty_diagram",
        "description": "No class declaration",
        "plantuml": "@startuml\n@enduml",
        "expected_valid": False,
        "expected_error_contains": ["Hic sinif tanimlanmamis"],
        "expected_warning_contains": [],
    },
    {
        "id": "ocl_04_missing_both_tags",
        "description": "Class without PlantUML boundary tags",
        "plantuml": "class UserManager {}",
        "expected_valid": False,
        "expected_error_contains": ["@startuml etiketi eksik", "@enduml etiketi eksik"],
        "expected_warning_contains": [],
    },
    {
        "id": "ocl_05_pascal_case",
        "description": "Non-PascalCase class name",
        "plantuml": "@startuml\nclass userManager {}\n@enduml",
        "expected_valid": True,
        "expected_error_contains": [],
        "expected_warning_contains": ["Sinif isimlendirme kurali ihlali"],
    },
    {
        "id": "ocl_06_duplicate_class",
        "description": "Duplicate class declaration",
        "plantuml": "@startuml\nclass UserManager {}\nclass UserManager {}\n@enduml",
        "expected_valid": False,
        "expected_error_contains": ["Tekrar eden sinif ismi"],
        "expected_warning_contains": ["Izole sinif"],
    },
    {
        "id": "ocl_07_isolated_classes",
        "description": "Multiple classes without relation",
        "plantuml": "@startuml\nclass UserManager {}\nclass DiagramService {}\n@enduml",
        "expected_valid": True,
        "expected_error_contains": [],
        "expected_warning_contains": ["Izole sinif"],
    },
    {
        "id": "ocl_08_cycle",
        "description": "Cyclic dependency",
        "plantuml": (
            "@startuml\nclass Aaaa {}\nclass Bbbb {}\n"
            "Aaaa --> Bbbb\nBbbb --> Aaaa\n@enduml"
        ),
        "expected_valid": True,
        "expected_error_contains": [],
        "expected_warning_contains": ["Dongusel bagimlilik"],
    },
    {
        "id": "ocl_09_god_class",
        "description": "Class with more than ten methods",
        "plantuml": "@startuml\nclass HugeService {\n"
        + "\n".join(f"  +m{i}()" for i in range(11))
        + "\n}\n@enduml",
        "expected_valid": True,
        "expected_error_contains": [],
        "expected_warning_contains": ["God Class"],
    },
    {
        "id": "ocl_10_complexity",
        "description": "More than twenty classes",
        "plantuml": "@startuml\n"
        + "\n".join(f"class Class{i} {{}}" for i in range(21))
        + "\n@enduml",
        "expected_valid": True,
        "expected_error_contains": [],
        "expected_warning_contains": ["Cok fazla sinif"],
    },
    {
        "id": "ocl_11_mixed_missing_end",
        "description": "Missing end tag plus naming and isolation warnings",
        "plantuml": "@startuml\nclass badName {}\nclass OtherClass {}",
        "expected_valid": False,
        "expected_error_contains": ["@enduml etiketi eksik"],
        "expected_warning_contains": ["Sinif isimlendirme", "Izole sinif"],
    },
    {
        "id": "ocl_12_duplicate_cycle",
        "description": "Duplicate class and cyclic dependency",
        "plantuml": (
            "@startuml\nclass AlphaClass {}\nclass BetaClass {}\n"
            "class AlphaClass {}\nAlphaClass --> BetaClass\n"
            "BetaClass --> AlphaClass\n@enduml"
        ),
        "expected_valid": False,
        "expected_error_contains": ["Tekrar eden sinif ismi"],
        "expected_warning_contains": ["Dongusel bagimlilik"],
    },
    {
        "id": "ocl_13_valid_baseline",
        "description": "Valid two-class relation baseline",
        "plantuml": (
            "@startuml\nclass UserManager {}\nclass DiagramService {}\n"
            "UserManager --> DiagramService\n@enduml"
        ),
        "expected_valid": True,
        "expected_error_contains": [],
        "expected_warning_contains": [],
    },
]


SEMANTIC_CASES = [
    {
        "id": "sem_01_exact_classes_relation",
        "description": "SRS and UML contain the same classes and relation",
        "srs": (
            "The UserManager handles user authentication. "
            "The DiagramService generates diagrams. "
            "The UserManager uses the DiagramService."
        ),
        "plantuml": (
            "@startuml\nclass UserManager {}\nclass DiagramService {}\n"
            "UserManager --> DiagramService\n@enduml"
        ),
        "expected_pass": True,
    },
    {
        "id": "sem_02_hallucinated_class",
        "description": "UML contains a class absent from the SRS",
        "srs": "The UserManager handles user authentication.",
        "plantuml": "@startuml\nclass UserManager {}\nclass FakeBillingService {}\n@enduml",
        "expected_pass": True,
        "limitation_note": "Passes the current 0.75 threshold despite one hallucinated class.",
    },
    {
        "id": "sem_03_missing_class",
        "description": "SRS mentions two classes but UML contains one",
        "srs": (
            "The AuthenticationService handles login. "
            "The SessionManager manages active sessions."
        ),
        "plantuml": "@startuml\nclass AuthenticationService {}\n@enduml",
        "expected_pass": True,
        "limitation_note": "Passes the current 0.75 threshold despite one missing class.",
    },
    {
        "id": "sem_04_no_srs_entities",
        "description": "No recognized class suffix in SRS",
        "srs": "The system shall let a user reset a password.",
        "plantuml": "@startuml\nclass GeneratedDiagram {}\n@enduml",
        "expected_pass": False,
        "limitation_note": "Fails because no SRS-side class entity is extracted and UML has a hallucinated class.",
    },
    {
        "id": "sem_05_complex_match",
        "description": "Three extracted classes with two relations",
        "srs": (
            "The AuthenticationService uses the UserRepository. "
            "The AuthenticationService communicates with the SessionManager. "
            "The SessionManager manages active sessions."
        ),
        "plantuml": (
            "@startuml\nclass AuthenticationService {}\nclass UserRepository {}\n"
            "class SessionManager {}\nAuthenticationService --> UserRepository\n"
            "AuthenticationService --> SessionManager\n@enduml"
        ),
        "expected_pass": True,
        "limitation_note": "",
    },
]


def contains_all(values: list[str], expected: list[str]) -> bool:
    joined = "\n".join(values)
    return all(fragment in joined for fragment in expected)


def wilson_interval(successes: int, total: int, z: float = 1.96) -> dict:
    if total <= 0:
        raise ValueError("total must be positive")
    phat = successes / total
    denom = 1 + z * z / total
    center = (phat + z * z / (2 * total)) / denom
    half = z * math.sqrt((phat * (1 - phat) + z * z / (4 * total)) / total) / denom
    return {
        "successes": successes,
        "total": total,
        "rate": round(phat, 4),
        "lower": round(center - half, 4),
        "upper": round(center + half, 4),
        "lower_percent": round((center - half) * 100, 1),
        "upper_percent": round((center + half) * 100, 1),
    }


def run_ocl_cases() -> list[dict]:
    rows = []
    for case in OCL_CASES:
        result = validate_ocl(case["plantuml"])
        passed = (
            result["gecerli_mi"] == case["expected_valid"]
            and contains_all(result["hatalar"], case["expected_error_contains"])
            and contains_all(result["uyarilar"], case["expected_warning_contains"])
        )
        rows.append(
            {
                "id": case["id"],
                "description": case["description"],
                "expected_valid": case["expected_valid"],
                "actual_valid": result["gecerli_mi"],
                "score": result["skor"],
                "percent": result["yuzde"],
                "errors": result["hatalar"],
                "warnings": result["uyarilar"],
                "details": result["detaylar"],
                "passed": passed,
                "manual_review": "",
                "review_note": "",
            }
        )
    return rows


def run_semantic_cases() -> list[dict]:
    rows = []
    for case in SEMANTIC_CASES:
        result = calculate_semantic_fidelity(case["srs"], case["plantuml"])
        rows.append(
            {
                "id": case["id"],
                "description": case["description"],
                "expected_pass": case["expected_pass"],
                "actual_pass": result["gecti_mi"],
                "score": result["genel_skor"],
                "percent": result["yuzde"],
                "class_metrics": result["sinif_metrikleri"],
                "relation_metrics": result["iliski_metrikleri"],
                "hallucinations": result["halusinasyonlar"],
                "missing_classes": result["eksik_siniflar"],
                "criteria": result["ieee_kriterleri"],
                "passed": result["gecti_mi"] == case["expected_pass"],
                "limitation_note": case.get("limitation_note", ""),
                "manual_review": "",
                "review_note": "",
            }
        )
    return rows


def write_markdown_report(report: dict, output_path: Path) -> None:
    lines = [
        "# Backend Validation Evidence",
        "",
        "This report is generated by `backend/evaluation/validation_benchmark.py`.",
        "It covers only the backend-owned OCL-like structural validator and deterministic semantic evaluator.",
        "",
        "## Summary",
        "",
        f"- OCL cases: {report['summary']['ocl_passed']}/{report['summary']['ocl_total']} passed.",
        f"- Semantic cases: {report['summary']['semantic_passed']}/{report['summary']['semantic_total']} passed.",
        "- Autonomous repair success rate is not reproduced by this validation script.",
        "- The main repair evidence is the shared S01-S50 benchmark in `backend/evaluation/results/`.",
        "",
        "## Shared Repair Benchmark Note",
        "",
        "The current paper revision uses a shared benchmark of 50 invalid PlantUML scenarios.",
        "Both deterministic repair and the real LLM-based autonomous repair endpoint are evaluated",
        "on the same S01-S50 cases with `max_iterations=3`.",
        "",
        "Current repair results:",
        "- Deterministic repair: 31/50 successful repairs (62.0%; Wilson 95% CI: 48.2%-74.1%).",
        "- LLM autonomous repair: 47/50 successful repairs (94.0%; Wilson 95% CI: 83.8%-97.9%).",
        "",
        "Primary output files:",
        "- `backend/evaluation/results/shared_benchmark_deterministic_experiment.json`",
        "- `backend/evaluation/results/shared_benchmark_llm_experiment.json`",
        "",
        "## OCL-like Structural Validation Cases",
        "",
        "| ID | Valid? | Score | Errors | Warnings | Auto Check | Manual Review |",
        "|---|---:|---:|---|---|---|---|",
    ]
    for row in report["ocl_cases"]:
        errors = "<br>".join(row["errors"]) if row["errors"] else "-"
        warnings = "<br>".join(row["warnings"]) if row["warnings"] else "-"
        lines.append(
            f"| {row['id']} | {row['actual_valid']} | {row['percent']} | "
            f"{errors} | {warnings} | {row['passed']} |  |"
        )
    lines.extend(
        [
            "",
            "## Deterministic Semantic Evaluator Cases",
            "",
            "| ID | Expected Pass | Actual Pass | Score | Hallucinations | Missing Classes | Limitation Note | Auto Check | Manual Review |",
            "|---|---:|---:|---:|---|---|---|---|---|",
        ]
    )
    for row in report["semantic_cases"]:
        hallucinations = "<br>".join(row["hallucinations"]) if row["hallucinations"] else "-"
        missing = "<br>".join(row["missing_classes"]) if row["missing_classes"] else "-"
        lines.append(
            f"| {row['id']} | {row['expected_pass']} | {row['actual_pass']} | "
            f"{row['percent']} | {hallucinations} | {missing} | "
            f"{row['limitation_note'] or '-'} | {row['passed']} |  |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ocl_rows = run_ocl_cases()
    semantic_rows = run_semantic_cases()
    report = {
        "metadata": {
            "scope": "backend/src/ocl_engine and backend/src/evaluators",
            "llm_calls": False,
            "autonomous_repair_reproduced": False,
            "repair_experiment_log": "backend/evaluation/results/shared_benchmark_llm_experiment.json",
            "repair_experiment_scope": "shared S01-S50 benchmark; deterministic and LLM repair use the same cases",
        },
        "summary": {
            "ocl_total": len(ocl_rows),
            "ocl_passed": sum(1 for row in ocl_rows if row["passed"]),
            "semantic_total": len(semantic_rows),
            "semantic_passed": sum(1 for row in semantic_rows if row["passed"]),
        },
        "shared_repair_benchmark": {
            "case_count": 50,
            "max_iterations": 3,
            "deterministic": wilson_interval(31, 50),
            "llm_autonomous": wilson_interval(47, 50),
            "deterministic_log": "backend/evaluation/results/shared_benchmark_deterministic_experiment.json",
            "llm_log": "backend/evaluation/results/shared_benchmark_llm_experiment.json",
        },
        "ocl_cases": ocl_rows,
        "semantic_cases": semantic_rows,
    }

    output_dir = BACKEND_ROOT / "evaluation" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "validation_results.json"
    md_path = output_dir / "validation_report.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown_report(report, md_path)
    print(json_path)
    print(md_path)
    print(json.dumps(report["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
