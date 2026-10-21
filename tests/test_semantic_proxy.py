import json
from pathlib import Path

import pytest

from backend.src.evaluators.semantic_eval import GoldModelExtractor, calculate_semantic_fidelity, calculate_semantic_fidelity_legacy


def test_retained_s02_legacy_score_is_exactly_preserved():
    path=Path(__file__).resolve().parents[1]/'backend/evaluation/results/shared_benchmark_llm_experiment.json'
    case=next(c for c in json.loads(path.read_text(encoding='utf-8'))['cases'] if c['case_id']=='S02')
    assert calculate_semantic_fidelity_legacy(case['srs_metni'],case['final_plantuml'])['genel_skor']==.25
    assert calculate_semantic_fidelity(case['srs_metni'],case['final_plantuml'])['score']==0


def test_no_source_entities_is_not_applicable():
    result=calculate_semantic_fidelity('the solution should respond quickly.','class Order {}')
    assert result['score'] is None and result['status']=='not_applicable'
    assert result['gecti_mi'] is None


def test_no_source_relationship_does_not_give_free_credit():
    result=calculate_semantic_fidelity('The User signs in.','class Order {}')
    assert result['score']==0
    assert result['effective_weights']['relationship_f1']==0


def test_gold_extractor_is_configurable():
    result=calculate_semantic_fidelity('no explicit names', 'class A {}', GoldModelExtractor('class A {}'))
    assert result['score']==pytest.approx(1)


def test_modern_stop_words_are_shared():
    from backend.src.evaluators.semantic_eval import STOP_WORDS as a
    from backend.src.parsers.srs_parser import STOP_WORDS as b
    assert a is b
