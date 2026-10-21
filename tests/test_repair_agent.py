"""No network, API key, or JVM is used by the scripted agent tests."""
import json
from dataclasses import replace

import pytest

from ai_core.src.ai.repair_agent import RepairConfig, UMLRepairAgent
from ai_core.src.rag.local_rules import LocalRuleRetriever, rule_catalogue

BAD = '@startuml\nclass Broken\n@enduml'
GOOD = '@startuml\nclass Document {}\n@enduml'


def validation(code):
    valid = code == GOOD
    return {'project_valid': valid, 'compiler_valid': valid,
            'compiler_errors': [] if valid else ['TEST compiler error'], 'project_errors': []}


class ScriptedClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def invoke(self, role, prompt, config):
        self.calls.append((role, prompt))
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return {'content': response, 'tokens_in': 12, 'tokens_out': 6,
                'model_name': 'fake-offline', 'request_id': 'test-only'}


def decision(valid):
    return json.dumps({'is_valid': valid, 'errors': [] if valid else ['invalid']})


def run(responses, config=None, code=BAD, validator=validation, force=True):
    client = ScriptedClient(responses)
    agent = UMLRepairAgent(config or RepairConfig(max_retries=0), client, validator)
    return agent.run('Document stores requirements.', code, True, force), client


def test_always_invalid_exhausts_three_repairs_and_seven_calls():
    state, _ = run([decision(False), BAD] * 3 + [decision(False)])
    assert state['terminated_by'] == 'budget_exhausted'
    assert state['repair_attempt_count'] == 3
    assert state['llm_call_count'] == len(state['trace']) == 7
    assert state['tokens_in'] == 84


def test_valid_first_critic_requires_compiler_and_project():
    state, _ = run([decision(True)], code=GOOD)
    assert state['terminated_by'] == 'accepted'
    assert state['repair_attempt_count'] == 0
    assert state['first_compiler_valid_iteration'] == 0
    state, client = run([decision(True), GOOD, decision(True)])
    assert [c[0] for c in client.calls] == ['critic', 'healer', 'critic']
    assert state['first_compiler_valid_iteration'] == 1


@pytest.mark.parametrize(('response', 'status'), [
    ('not JSON', 'parse_error'), (RuntimeError('API unavailable'), 'api_error'),
    (TimeoutError('deadline'), 'timeout'),
    ('{"is_valid": "yes", "errors": []}', 'parse_error'),
])
def test_failures_are_explicit(response, status):
    state, _ = run([response])
    assert state['agent_status'] == status
    assert state['terminated_by'] == 'error'
    assert state['agent_error']


def test_feedback_and_srs_are_in_modern_healer_prompt():
    state, client = run([decision(False), GOOD, decision(True)])
    healer = client.calls[1][1]
    assert 'Document stores requirements.' in healer
    assert 'TEST compiler error' in healer
    assert state['trace'][1]['model_name'] == 'fake-offline'


def test_legacy_healer_excludes_srs_and_preserves_early_acceptance():
    config = replace(RepairConfig(), mode='legacy_critic_healer', max_retries=0)
    state, client = run([decision(False), BAD, decision(True)], config)
    assert 'Document stores requirements.' not in client.calls[1][1]
    assert 'TEST compiler error' not in client.calls[1][1]
    assert state['terminated_by'] == 'accepted'
    assert state['compiler_valid'] is False


@pytest.mark.parametrize('mode', ['single_pass', 'healer_only_compiler_feedback'])
def test_conditions_without_critic(mode):
    state, client = run([GOOD], replace(RepairConfig(), mode=mode))
    assert [c[0] for c in client.calls] == ['healer']
    assert state['critic_valid'] is None


def test_raw_regression_and_reversion_are_both_retained():
    state, _ = run([BAD], replace(RepairConfig(), mode='single_pass'), GOOD)
    assert state['regression'] is True
    assert state['current_uml'] == BAD
    assert state['safe_plantuml'] == GOOD


def test_compiler_failure_triggers_repair_even_if_project_passes():
    def divergent(code):
        return {**validation(code), 'project_valid': True}
    state, _ = run([GOOD], replace(RepairConfig(), mode='single_pass'), validator=divergent, force=False)
    assert state['llm_call_count'] == 1


def test_domain_guard_and_catalogue_cache():
    retriever = LocalRuleRetriever()
    unrelated = retriever.retrieve('Document stores requirements.', BAD)
    assert not any(r['domain_example'] for r in unrelated)
    relevant = retriever.retrieve('An Order contains an OrderItem.', 'class Order\nclass OrderItem')
    assert any(r['id'] == 'DOMAIN-02' for r in relevant)
    assert rule_catalogue() is rule_catalogue()


def test_missing_usage_is_unknown_and_counts_reset_per_run():
    class MissingUsage:
        def invoke(self, *args):
            return {'content': GOOD}
    agent = UMLRepairAgent(replace(RepairConfig(), mode='single_pass'), MissingUsage(), validation)
    for _ in range(2):
        state = agent.run('', BAD, True)
        assert state['llm_call_count'] == 1
        assert state['tokens_in'] is None
        assert state['usage_complete'] is False

