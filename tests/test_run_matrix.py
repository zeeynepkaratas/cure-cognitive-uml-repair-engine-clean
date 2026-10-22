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


def test_interrupted_budget_preserves_partial_trace(tmp_path):
    from dataclasses import replace
    from ai_core.src.ai.repair_agent import UMLRepairAgent
    from tests.test_repair_agent import ScriptedClient, BAD, validation

    budget = Budget(tmp_path / "budget.json", 1, 1)
    agent = UMLRepairAgent(
        replace(RepairConfig(), mode="healer_only_compiler_feedback"),
        ScriptedClient([BAD]),
        validation,
        before_call=budget.reserve,
    )
    state = agent.run("", BAD, True, True)
    assert state["budget_stopped"] is True
    assert state["terminated_by"] == "budget_exhausted"
    assert len(state["trace"]) == state["llm_call_count"] == 1


def test_concurrent_budget_never_exceeds_call_limit(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    import json

    budget = Budget(tmp_path / "budget.json", 7, 10)

    def reserve(_):
        try:
            budget.reserve("healer", "text", RepairConfig())
            return True
        except BudgetExceeded:
            return False

    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(reserve, range(100))) == 7
    assert json.loads(budget.path.read_text())["calls_reserved"] == 7


def fake_runner(monkeypatch, tmp_path):
    from backend.evaluation import run_matrix as runner

    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "load_cases", lambda *args: [{"case_id": f"T{i}"} for i in range(12)])
    monkeypatch.setattr(
        runner,
        "metadata",
        lambda args, cases: {
            "git_commit": "test",
            "protocol_commit": "test",
            "prompt_hashes": {},
            "input_sha256": "test",
            "model_critic": args.model_critic,
            "model_healer": args.model_healer,
            "seed": args.seed,
            "config": {k: v for k, v in vars(args).items() if k not in {"run_dir", "resume"}},
        },
    )

    def evaluate(case, condition, rep, args, budget):
        return {
            **case,
            "condition": condition,
            "rep": rep,
            "run_status": "completed",
            "agent_status": "not_applicable",
            "compiler_valid": True,
        }

    monkeypatch.setattr(runner, "evaluate", evaluate)
    return runner, evaluate


def test_parallel_and_serial_have_same_cases_reproducible_order_and_resume(monkeypatch, tmp_path):
    import json

    runner, _ = fake_runner(monkeypatch, tmp_path)
    root = tmp_path / "backend/evaluation/results_v4"
    manifests = []
    case_sets = []
    for name, workers in [("serial", 1), ("parallel", 4), ("parallel2", 4)]:
        directory = root / name
        manifests.append(
            runner.main(["--conditions", "C0", "C1", "--workers", str(workers), "--run-dir", str(directory)])
        )
        rows = json.loads((directory / "results.json").read_text())
        case_sets.append({(r["condition"], r["case_id"], r["rep"]) for r in rows})
        assert len(rows) == len(case_sets[-1]) == 24
    assert case_sets[0] == case_sets[1] == case_sets[2]
    assert manifests[1]["task_order_sha256"] == manifests[2]["task_order_sha256"]
    before = (root / "parallel/cases/C0_T0_1.json").read_bytes()
    monkeypatch.setattr(runner, "evaluate", lambda *args: pytest.fail("completed case rerun"))
    runner.main(
        ["--conditions", "C0", "C1", "--workers", "4", "--run-dir", str(root / "parallel"), "--resume"]
    )
    assert (root / "parallel/cases/C0_T0_1.json").read_bytes() == before


def test_parallel_failure_saves_other_inflight_cases_and_error(monkeypatch, tmp_path):
    import threading
    import json

    runner, evaluate = fake_runner(monkeypatch, tmp_path)
    barrier = threading.Barrier(4)
    calls = []
    lock = threading.Lock()

    def failing(case, *args):
        with lock:
            index = len(calls)
            calls.append(case["case_id"])
        if index < 4:
            barrier.wait(timeout=10)
        if index == 0:
            raise RuntimeError("worker failed")
        return evaluate(case, *args)

    monkeypatch.setattr(runner, "evaluate", failing)
    directory = tmp_path / "backend/evaluation/results_v4/failure"
    manifest = runner.main(["--conditions", "C0", "--workers", "4", "--run-dir", str(directory)])
    assert manifest["status"] == "worker_error"
    assert len(manifest["worker_error_files"]) == 1
    assert len(json.loads((directory / "results.json").read_text())) >= 3


def test_runner_cannot_write_retained_evidence(monkeypatch, tmp_path):
    runner, _ = fake_runner(monkeypatch, tmp_path)
    target = tmp_path / "backend/evaluation/results"
    with pytest.raises(SystemExit):
        runner.main(["--conditions", "C0", "--run-dir", str(target)])
    assert not target.exists()
