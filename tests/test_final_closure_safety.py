"""The author/reviewer verifier must never write into historical evidence."""

from pathlib import Path
import pytest
from tools.verify_v4_artifact import ROOT, safe_output


@pytest.mark.parametrize("relative", ["backend/evaluation/results_v4/new", "docs/closure_audit", "data_pipeline/datasets", "."])
def test_reject_historical_or_unrestricted_checkout_output(relative):
    with pytest.raises(ValueError, match="docs/final_closure"):
        safe_output(ROOT / relative)


def test_refuse_overwriting_an_existing_verification(tmp_path):
    (tmp_path / "proof.json").write_text("previous evidence")
    with pytest.raises(FileExistsError):
        safe_output(tmp_path)
    assert (tmp_path / "proof.json").read_text() == "previous evidence"


def test_external_empty_review_output_is_allowed(tmp_path):
    assert safe_output(Path(tmp_path)) == tmp_path.resolve()
