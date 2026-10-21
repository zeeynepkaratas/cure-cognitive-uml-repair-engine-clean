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
