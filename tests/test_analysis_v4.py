import pytest
from backend.evaluation.analyze_v4 import exact_mcnemar, holm, paired_delta


def test_exact_two_sided_discordants_and_holm():
    result = exact_mcnemar([False] * 29, [True] * 29)
    assert result["a_fail_b_pass"] == 29 and result["a_pass_b_fail"] == 0
    assert result["p_exact_two_sided"] == pytest.approx(3.725290298461914e-9)
    assert exact_mcnemar([True, False], [False, True])["p_exact_two_sided"] == 1
    assert holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])


def test_cluster_bootstrap_and_degenerate_wilcoxon():
    result = paired_delta([0.0, 0.0], ["same", "same"], draws=100)
    assert result["wilcoxon_p"] == 1 and result["bootstrap_ci"] == [0, 0]
    result = paired_delta([1.0, 1.0, 1.0], ["a", "a", "b"], draws=100)
    assert result["bootstrap_ci"] == [1.0, 1.0]
    assert result["clusters"] == 2
    result = paired_delta([1.0, -1.0], ["same", "same"], draws=100)
    assert result["wilcoxon_p"] == 1 and result["all_cluster_means_zero"] is True


def test_development_without_none_baseline_and_repetition_semantic_sd():
    from backend.evaluation.analyze_v4 import compute
    from backend.evaluation.reference_metrics import reference_metrics

    code = "@startuml\nclass Document {}\n@enduml"
    rows = [
        {
            "dataset": "semantic",
            "case_id": "T1",
            "condition": "C3",
            "rep": rep,
            "compiler_valid": True,
            "project_valid": True,
            "critic_valid": None,
            "agent_status": "ok",
            "regression": False,
            "compiler_valid_if_reverted": True,
            "terminated_by": "accepted",
            "elapsed_seconds": 10.0,
            "end_to_end_seconds": 12.0,
            "tokens_in": 10,
            "tokens_out": 10,
            "warnings_added": 0,
            "warnings_removed": 0,
            "defect_ids": ["D1"],
            "output_sha256": str(rep),
            "metrics": reference_metrics(code, code, code),
        }
        for rep in [1, 2]
    ]
    numbers = compute(rows)
    assert numbers["mcnemar"] == []
    assert numbers["summaries"][0]["latency"]["mean"] == 12.0
    assert numbers["repetitions"][0]["class_f1_across_reps"]["mean"] == 1.0
    assert numbers["repetitions"][0]["class_f1_across_reps"]["sd"] == 0.0
    assert numbers["repetitions"][0]["output_disagreement_rate"] == 1.0
