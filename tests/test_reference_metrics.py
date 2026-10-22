import pytest
from backend.evaluation.reference_metrics import normalise_name, reference_metrics, prf


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("OrderItems", "orderitem"),
        ("order_items", "orderitem"),
        ("ORDER-ITEM", "orderitem"),
        ("Categories", "category"),
        ("Classes", "class"),
        ("Status", "status"),
        ("Account", "account"),
        ("HTTPRequests", "httprequest"),
    ],
)
def test_normalisation(value, expected):
    assert normalise_name(value) == expected


def test_direction_type_attributes_and_delta():
    gold = '@startuml\nclass A {\n+id: String\n}\nclass B {}\nA "1" --> "*" B\n@enduml'
    reverse = gold.replace('A "1" --> "*" B', 'B "*" --> "1" A')
    result = reference_metrics(gold, reverse, gold)
    assert result["reference_class"]["f1"] == 1
    assert result["reference_rel_undirected"]["f1"] == 1
    assert result["reference_rel_directed"]["f1"] == 0
    assert result["delta_rel_directed_f1"] == -1
    assert result["reference_attribute"]["f1"] == 1
    wrongtype = reference_metrics(gold, gold.replace("-->", "--|>"))
    assert wrongtype["reference_rel_directed"]["f1"] == 1
    assert wrongtype["reference_rel_typed"]["f1"] == 0
    assert prf(set(), set())["f1"] == 1
