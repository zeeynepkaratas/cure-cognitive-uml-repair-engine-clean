import pytest
from tools.finalize_v4 import coverage


def test_complete_matrix_and_duplicate_missing_partial_rejection():
    cases = [{"case_id": "A"}, {"case_id": "B"}]
    rows = [
        {"condition": c, "case_id": case["case_id"], "rep": rep, "run_status": "completed"}
        for c in ["C0", "C3"]
        for case in cases
        for rep in range(1, 2 if c == "C0" else 6)
    ]
    assert coverage(rows, cases, ["C0", "C3"], 5)["observed_unique_case_runs"] == 12
    for invalid in [rows[:-1], rows + [rows[0]], [{**rows[0], "run_status": "budget_stopped"}, *rows[1:]]]:
        with pytest.raises(ValueError):
            coverage(invalid, cases, ["C0", "C3"], 5)
