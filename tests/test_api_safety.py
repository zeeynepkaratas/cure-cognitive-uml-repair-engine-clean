"""API safety contracts independent of optional model/compiler runtimes."""

from ai_core.src.ai.repair_agent import RepairConfig, UMLRepairAgent
from backend.src.api import endpoints
from tests.test_repair_agent import BAD, GOOD, ScriptedClient, validation


def compile_result(code):
    check = validation(code)
    return {**check, "basarili": check["project_valid"]}


def test_api_explicit_error_does_not_report_success(monkeypatch):
    agent = UMLRepairAgent(RepairConfig(max_retries=0), ScriptedClient([RuntimeError("offline")]), validation)
    monkeypatch.setattr(endpoints, "UMLRepairAgent", lambda *args: agent)
    monkeypatch.setattr(endpoints, "_compile_test", compile_result)
    result = endpoints.autonomous_repair(endpoints.AutonomousRepairRequest(plantuml_kodu=BAD))
    assert result["agent_status"] == "api_error"
    assert result["basarili"] is False
    assert result["compiler_valid"] is False


def test_api_returns_safe_output_and_retains_raw_regression(monkeypatch):
    agent = UMLRepairAgent(RepairConfig(mode="single_pass"), ScriptedClient([BAD]), validation)
    monkeypatch.setattr(endpoints, "UMLRepairAgent", lambda *args: agent)
    monkeypatch.setattr(endpoints, "_compile_test", compile_result)
    monkeypatch.setattr(endpoints, "render_plantuml", lambda code: {"svg": "<svg/>"})
    result = endpoints.autonomous_repair(
        endpoints.AutonomousRepairRequest(plantuml_kodu=GOOD, force_repair=True)
    )
    assert result["raw_final_plantuml"] == BAD
    assert result["final_plantuml"] == GOOD
    assert result["reverted"] is True
    assert result["compiler_valid"] is True
    assert result["raw_compiler_valid"] is False
    assert result["repair_accepted"] is False


def test_compiler_pass_with_critic_rejection_is_not_accepted(monkeypatch):
    import json

    rejection = json.dumps({"is_valid": False, "errors": ["missing source element"]})
    agent = UMLRepairAgent(
        RepairConfig(max_iterations=1), ScriptedClient([rejection, GOOD, rejection]), validation
    )
    monkeypatch.setattr(endpoints, "UMLRepairAgent", lambda *args: agent)
    monkeypatch.setattr(endpoints, "_compile_test", compile_result)
    monkeypatch.setattr(endpoints, "render_plantuml", lambda code: {"svg": "<svg/>"})
    result = endpoints.autonomous_repair(endpoints.AutonomousRepairRequest(plantuml_kodu=BAD))
    assert result["compiler_valid"] is True
    assert result["critic_valid"] is False
    assert result["terminated_by"] == "budget_exhausted"
    assert result["repair_accepted"] is result["basarili"] is False


def test_evaluate_endpoint_returns_new_proxy_and_not_applicable():
    result = endpoints.semantik_degerlendir(
        endpoints.TamAnalizGirdisi(srs_metni="The User signs in.", plantuml_kodu="class User {}")
    )
    assert result["status"] == "applicable" and result["score"] == 1
    result = endpoints.semantik_degerlendir(
        endpoints.TamAnalizGirdisi(
            srs_metni="the solution should respond quickly.", plantuml_kodu="class User {}"
        )
    )
    assert result["status"] == "not_applicable" and result["score"] is None
