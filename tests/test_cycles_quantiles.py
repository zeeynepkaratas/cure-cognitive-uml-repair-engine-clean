import numpy as np
import pytest

from backend.src.api.performance import percentile_hesapla
from backend.src.ocl_engine.ocl_validator import detect_cycle, validate_ocl


def test_all_cyclic_components_are_reported():
    assert detect_cycle(
        ["A", "B", "C", "D", "E"], [("A", "B"), ("B", "A"), ("C", "D"), ("D", "C"), ("E", "E")]
    ) == ["SCC: {A, B}", "SCC: {C, D}", "SCC: {E}"]


@pytest.mark.parametrize("p", [0, 25, 50, 95, 99, 100])
def test_quantiles_match_documented_numpy_method(p):
    data = list(range(50))
    assert percentile_hesapla(data, p) == pytest.approx(float(np.percentile(data, p)))


def test_god_class_methods_survive_nested_braces():
    code = (
        "@startuml\nclass A {\n"
        + "\n".join(f"+m{i}() {{ if(x) {{ call(); }} }}" for i in range(11))
        + "\n}\n@enduml"
    )
    assert "UYARI" in validate_ocl(code)["detaylar"]["OCL-04"]
