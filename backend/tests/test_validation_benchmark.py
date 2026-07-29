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
    metadata = report["metadata"]
    for field in ["commit_sha", "generated_at_utc", "python", "platform", "model", "temperature", "max_iterations"]:
        assert field in metadata
    assert report["summary"]["total_cases"] == 50
    assert report["summary"]["initially_invalid_cases"] == 50
    assert report["summary"]["successful_repairs"] == 31
    assert report["summary"]["failed_repairs"] == 19
    assert report["summary"]["success_rate_percent"] == 62.0


def test_legacy_llm_result_is_preserved_but_not_reported_as_current():
    legacy_path = RESULTS / "legacy_pre_validation_fix" / "shared_benchmark_llm_experiment.json"
    current_path = RESULTS / "shared_benchmark_llm_experiment.json"
    assert legacy_path.exists()
    assert not current_path.exists()


if __name__ == "__main__":
    tests = [
        test_ocl_validation_sample_matches_expected_flags,
        test_semantic_validation_sample_matches_expected_flags,
        test_wilson_interval_for_shared_llm_benchmark,
        test_shared_deterministic_repair_benchmark_reproduces_31_of_50_success_rate,
        test_legacy_llm_result_is_preserved_but_not_reported_as_current,
    ]
    passed = 0
    for test in tests:
        test()
        passed += 1
        print(f"PASS: {test.__name__}")
    print(f"Sonuc: {passed}/{len(tests)} test gecti")
