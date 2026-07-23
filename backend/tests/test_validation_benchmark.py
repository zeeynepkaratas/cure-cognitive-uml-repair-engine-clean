import os
import sys
import json
from pathlib import Path


BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(BACKEND_ROOT)
sys.path.insert(0, BACKEND_ROOT)
sys.path.insert(0, REPO_ROOT)

from backend.evaluation.validation_benchmark import (
    OCL_CASES,
    SEMANTIC_CASES,
    run_ocl_cases,
    run_semantic_cases,
    wilson_interval,
)
from backend.evaluation.shared_benchmark_deterministic_experiment import build_report


RESULTS = Path(BACKEND_ROOT) / "evaluation" / "results"


def test_ocl_validation_sample_matches_expected_flags():
    rows = run_ocl_cases()
    assert len(rows) == len(OCL_CASES)
    failed = [row["id"] for row in rows if not row["passed"]]
    assert failed == []


def test_semantic_validation_sample_matches_expected_flags():
    rows = run_semantic_cases()
    assert len(rows) == len(SEMANTIC_CASES)
    failed = [row["id"] for row in rows if not row["passed"]]
    assert failed == []


def test_wilson_interval_for_shared_llm_benchmark():
    interval = wilson_interval(47, 50)
    assert interval["successes"] == 47
    assert interval["total"] == 50
    assert interval["rate"] == 0.94
    assert interval["lower_percent"] == 83.8
    assert interval["upper_percent"] == 97.9


def test_shared_deterministic_repair_benchmark_reproduces_31_of_50_success_rate():
    report = build_report()
    assert report["summary"]["total_cases"] == 50
    assert report["summary"]["initially_invalid_cases"] == 50
    assert report["summary"]["successful_repairs"] == 31
    assert report["summary"]["failed_repairs"] == 19
    assert report["summary"]["success_rate_percent"] == 62.0


def test_saved_shared_llm_benchmark_reports_47_of_50_success_rate():
    report = json.loads((RESULTS / "shared_benchmark_llm_experiment.json").read_text(encoding="utf-8"))
    assert report["summary"]["total_cases"] == 50
    assert report["summary"]["successful_repairs"] == 47
    assert report["summary"]["failed_repairs"] == 3
    assert report["summary"]["success_rate_percent"] == 94.0


if __name__ == "__main__":
    tests = [
        test_ocl_validation_sample_matches_expected_flags,
        test_semantic_validation_sample_matches_expected_flags,
        test_wilson_interval_for_shared_llm_benchmark,
        test_shared_deterministic_repair_benchmark_reproduces_31_of_50_success_rate,
        test_saved_shared_llm_benchmark_reports_47_of_50_success_rate,
    ]
    passed = 0
    for test in tests:
        test()
        passed += 1
        print(f"PASS: {test.__name__}")
    print(f"Sonuc: {passed}/{len(tests)} test gecti")
