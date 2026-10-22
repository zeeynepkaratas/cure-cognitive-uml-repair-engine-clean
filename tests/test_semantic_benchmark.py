import json
from pathlib import Path
from backend.evaluation.semantic_benchmark.defect_injector import inject
from backend.src.utils.plantuml_parser import parse_model

ROOT = Path(__file__).resolve().parents[1] / "backend/evaluation/semantic_benchmark"


def test_benchmark_sizes_split_and_seeded_changes():
    cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
    scenarios = json.loads((ROOT / "scenarios.json").read_text(encoding="utf-8"))
    assert len(scenarios) == 30 and len(cases) == 60
    dev = {c["scenario_id"] for c in cases if c["split"] == "dev"}
    test = {c["scenario_id"] for c in cases if c["split"] == "test"}
    assert not dev & test
    assert sum(c["split"] == "dev" for c in cases) == 20
    assert {d for c in cases for d in c["defect_ids"]} == {f"D{i}" for i in range(1, 11)}
    for case in cases:
        actual = case["gold"]
        for offset, operator in enumerate(case["defect_ids"]):
            actual, _ = inject(actual, operator, case["seed"] + offset)
        assert actual == case["defective"] != case["gold"]
    for scenario in scenarios:
        model = parse_model(scenario["gold"])
        assert 4 <= len(model.declarations) <= 8
        assert 3 <= len(model.relationships) <= 10
        assert all(r.src_mult and r.tgt_mult for r in model.relationships)
