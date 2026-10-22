import json
from pathlib import Path

import pytest

from backend.src.utils.plantuml_parser import OPERATORS, parse_classes, parse_model, parse_relationships


@pytest.mark.parametrize("operator", OPERATORS)
def test_all_relationship_operators(operator):
    model = parse_model(f'A "1" {operator} "*" B : owns')
    assert len(model.relationships) == 1
    rel = model.relationships[0]
    assert {rel.src, rel.tgt} == {"A", "B"}
    assert {rel.src_mult, rel.tgt_mult} == {"1", "*"}
    assert rel.label == "owns"


@pytest.mark.parametrize("kind", ["class", "abstract class", "interface", "enum"])
def test_declaration_kinds(kind):
    assert parse_classes(f"{kind} Sample {{}}") == {"Sample"}


@pytest.mark.parametrize(
    "code",
    [
        "' class Fake {}",
        "/' class Fake {} '/",
        'note "class Fake"',
        "classy Fake",
        "xclass Fake",
        '"class Fake"',
    ],
)
def test_comments_and_literals_do_not_declare(code):
    assert parse_classes(code) == set()


@pytest.mark.parametrize("operator", ["-[#red]->", "-[dashed]->", "..[#blue]>", "-[#red,bold]->"])
def test_styled_arrows(operator):
    assert parse_relationships(f"A {operator} B") == {("A", "B")}


def test_nested_braces_and_members():
    model = parse_model("class A {\n +name: String\n +run() {\n if (x) { call(); }\n }\n}\nclass B {}")
    assert {d.name for d in model.declarations} == {"A", "B"}
    assert "+name: String" in model.declarations[0].attributes
    assert "+run() {" in model.declarations[0].methods


def test_quoted_alias_and_direction():
    assert parse_classes('class "User Account" as Account {}') == {"Account"}
    rel = parse_model("A <|.. B").relationships[0]
    assert (rel.src, rel.tgt, rel.type) == ("B", "A", "realization")


def test_self_relation_is_retained():
    assert parse_relationships("A --> A") == {("A", "A")}


def test_retained_class_set_regression():
    results = Path(__file__).resolve().parents[1] / "backend/evaluation/results"
    differences = []
    for file in results.glob("*_experiment.json"):
        for case in json.loads(file.read_text(encoding="utf-8")).get("cases", []):
            code = case.get("final_plantuml", "")
            before, after = parse_classes(code, legacy=True), parse_classes(code)
            if before != after:
                differences.append((file.name, case["case_id"], sorted(before), sorted(after)))
    # S46 contains a nameless declaration followed by a real declaration. The
    # old cross-line regex calls the next keyword 'class' a class name (F19).
    assert differences == [
        ("shared_benchmark_deterministic_experiment.json", "S46", ["class"], ["GeneratedDiagram"])
    ], differences
