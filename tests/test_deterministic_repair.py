import pytest

from backend.src.repair.deterministic import deterministic_extended, deterministic_minimal
from backend.src.utils.plantuml_parser import parse_classes, parse_model


@pytest.mark.parametrize("code", ["class A {}", "@startuml\nclass A {}", "class A {}\n@enduml"])
def test_boundaries(code):
    fixed, actions = deterministic_extended(code)
    assert fixed.startswith("@startuml\n") and fixed.endswith("\n@enduml")
    assert parse_classes(fixed) == {"A"}


@pytest.mark.parametrize("code", ["' class Fake {}", 'note "class Fake"'])
def test_comment_and_literal_do_not_prevent_placeholder(code):
    fixed, actions = deterministic_extended(code)
    assert "GeneratedDiagram" in parse_classes(fixed)
    assert "inserted_placeholder_for_no_declarations" in actions


def test_interfaces_do_not_get_placeholder():
    assert parse_classes(deterministic_extended("interface API {}")[0]) == {"API"}


def test_duplicates_merge_members():
    fixed, actions = deterministic_extended("class A {\n+x: int\n}\nclass A {\n+f()\n}")
    assert len(parse_model(fixed).declarations) == 1
    assert "+x: int" in fixed and "+f()" in fixed
    assert any("merged_duplicate" in a for a in actions)


def test_braces_tokens_and_truncated_edges():
    fixed, actions = deterministic_extended(
        "@startuml\nclass A {\nclass B {}\n}\n}\nA -->\nA --> Missing\n@enduml\n@enduml"
    )
    assert fixed.count("@startuml") == fixed.count("@enduml") == 1
    assert fixed.count("{") == fixed.count("}")
    assert "A -->" not in fixed


def test_nameless_class_removed():
    fixed, _ = deterministic_extended("class\nclass A {}")
    assert parse_classes(fixed) == {"A"}


def test_minimal_is_original_function():
    from backend.evaluation.repair_benchmark_utils import deterministic_backend_repair

    code = "' class Fake {}"
    assert deterministic_minimal(code) == deterministic_backend_repair(code)


import pytest


@pytest.mark.parametrize("fragment", ["--> WorkerService", "<-- WorkerService", "..> WorkerService"])
def test_truncated_arrow_without_source_is_dropped(fragment):
    code = "@startuml\nclass WorkerService {}\n" + fragment + "\n@enduml"
    output, actions = deterministic_extended(code)
    assert fragment not in output
    assert any("without_source" in action for action in actions)
    assert "class WorkerService" in output
