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
