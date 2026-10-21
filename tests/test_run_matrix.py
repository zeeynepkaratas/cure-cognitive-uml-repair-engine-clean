"""Runner planning and cost guards are tested without calling a provider."""

import pytest
from ai_core.src.ai.repair_agent import RepairConfig
from backend.evaluation.run_matrix import Budget, BudgetExceeded, load_cases, plan, main


def test_fixed_inputs_and_upper_bound():
    cases = load_cases()
    assert len(cases) == 100
    assert len(load_cases("dev")) == 20
    assert plan(cases, ["C0", "C3"], 5)["upper_bound_api_attempts"] == 1500
    assert main(["--conditions", "C0", "C1", "C2", "--dry-run"])["upper_bound_api_attempts"] == 0


def test_budget_is_reserved_before_dispatch_and_survives_resume(tmp_path):
    path = tmp_path / "budget.json"
    budget = Budget(path, 1, 1)
    budget.reserve("healer", "text", RepairConfig())
    with pytest.raises(BudgetExceeded):
        budget.reserve("healer", "text", RepairConfig())
    resumed = Budget(path, 1, 1)
    with pytest.raises(BudgetExceeded):
        resumed.reserve("critic", "text", RepairConfig())
    assert resumed.state["calls_reserved"] == 1
    assert resumed.state["usd_reserved"] > 0
    with pytest.raises(BudgetExceeded):
        Budget(tmp_path / "small.json", 10, 0.0000001).reserve("healer", "text", RepairConfig())
