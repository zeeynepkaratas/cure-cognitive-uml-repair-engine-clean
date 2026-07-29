import os
import sys
from types import SimpleNamespace
from unittest.mock import patch


BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(BACKEND_ROOT)
AI_CORE_SRC = os.path.join(REPO_ROOT, "ai_core", "src")
sys.path.insert(0, os.path.join(BACKEND_ROOT, "src"))
sys.path.insert(0, AI_CORE_SRC)

from ai.critic_decision import parse_critic_decision
from ai.workflow_control import route_repair_decision
from plantuml_runtime import plantuml_runtime_available, validate_with_plantuml
from renderers import plantuml_renderer
from utils.plantuml_parser import parse_relationships


def test_relationship_parser_handles_multiplicity_edges():
    code = '@startuml\nclass Order {}\nclass OrderItem {}\nOrder "1" --> "*" OrderItem\n@enduml'
    assert parse_relationships(code) == {("Order", "OrderItem")}


def test_relationship_parser_handles_common_plantuml_operators():
    code = """
@startuml
PaymentGateway --|> Gateway
Order o-- OrderItem
Cart ..> PricingService
@enduml
"""
    assert ("PaymentGateway", "Gateway") in parse_relationships(code)
    assert ("Order", "OrderItem") in parse_relationships(code)
    assert ("Cart", "PricingService") in parse_relationships(code)


def test_critic_parser_accepts_structured_dict():
    decision = parse_critic_decision(
        {"is_valid": False, "errors": ["Missing class: User"], "categories": ["semantic"]}
    )
    assert decision["is_valid"] is False
    assert decision["errors"] == ["Missing class: User"]
    assert decision["categories"] == ["semantic"]


def test_critic_parser_accepts_legacy_valid_token_with_punctuation():
    decision = parse_critic_decision(SimpleNamespace(content="GECERLI."))
    assert decision == {"is_valid": True, "errors": [], "categories": []}


def test_plantuml_runtime_reports_unavailable_without_configured_binary():
    with patch.dict(os.environ, {"PLANTUML_JAR": "", "PLANTUML_CMD": ""}, clear=False):
        with patch("plantuml_runtime.shutil.which", return_value=None):
            result = validate_with_plantuml("@startuml\nclass User {}\n@enduml")
    assert result["available"] is False
    assert result["successful"] is None


def test_renderer_marks_fallback_when_runtime_is_unavailable():
    with patch("renderers.plantuml_renderer.render_with_plantuml") as mocked:
        mocked.return_value = {"available": False, "successful": False, "error": "missing runtime"}
        result = plantuml_renderer.render_plantuml("@startuml\nclass User {}\n@enduml")
    assert result["render_source"] == "fallback_svg_preview"
    assert result["plantuml_runtime"]["available"] is False
    assert result["svg"].startswith("<svg")


def test_renderer_uses_real_runtime_output_when_available():
    with patch("renderers.plantuml_renderer.render_with_plantuml") as mocked:
        mocked.return_value = {
            "available": True,
            "successful": True,
            "svg": "<svg>real</svg>",
            "svg_base64": "PHN2Zz5yZWFsPC9zdmc+",
        }
        result = plantuml_renderer.render_plantuml("@startuml\nclass User {}\n@enduml")
    assert result["render_source"] == "plantuml_runtime"
    assert result["svg"] == "<svg>real</svg>"


def test_runtime_availability_is_boolean():
    assert plantuml_runtime_available() in {True, False}


def test_routing_stops_after_configured_repair_attempts():
    assert route_repair_decision(False, repair_attempt_count=3, max_iterations=3) == "end"


def test_routing_allows_repair_before_limit():
    assert route_repair_decision(False, repair_attempt_count=2, max_iterations=3) == "continue"


if __name__ == "__main__":
    tests = [
        test_relationship_parser_handles_multiplicity_edges,
        test_relationship_parser_handles_common_plantuml_operators,
        test_critic_parser_accepts_structured_dict,
        test_critic_parser_accepts_legacy_valid_token_with_punctuation,
        test_plantuml_runtime_reports_unavailable_without_configured_binary,
        test_renderer_marks_fallback_when_runtime_is_unavailable,
        test_renderer_uses_real_runtime_output_when_available,
        test_runtime_availability_is_boolean,
        test_routing_stops_after_configured_repair_attempts,
        test_routing_allows_repair_before_limit,
    ]
    passed = 0
    for test in tests:
        test()
        passed += 1
        print(f"PASS: {test.__name__}")
    print(f"Sonuc: {passed}/{len(tests)} test gecti")
