from backend.evaluation.validator_audit import confusion, extract_diagrams


def test_compiler_agreement_and_missing_values():
    rows = [
        {"project_valid": p, "compiler_valid": c}
        for p, c in [(True, True), (True, False), (False, True), (False, False), (True, None)]
    ]
    result = confusion(rows)
    assert result == {
        "TP": 1,
        "FP": 1,
        "FN": 1,
        "TN": 1,
        "unavailable": 1,
        "sensitivity": 0.5,
        "specificity": 0.5,
    }
    assert list(
        extract_diagrams({"cases": [{"input_plantuml": "class A", "metadata": "not a diagram"}]})
    ) == [("input_plantuml", "class A")]
