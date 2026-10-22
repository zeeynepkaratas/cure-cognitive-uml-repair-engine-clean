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


def test_measured_cache_rejects_wrong_jar_and_detects_conflicts(tmp_path):
    import hashlib
    import json
    import pytest
    from backend.evaluation.validator_audit import measured_cache
    from backend.evaluation.run_matrix import JAR_SHA

    code = "@startuml\nclass Document {}\n@enduml"
    folders = []
    for i, valid in enumerate([True, False]):
        folder = tmp_path / str(i)
        folder.mkdir()
        rows = [
            {
                "input_plantuml": code,
                "output_plantuml": code,
                "input_validation": {"compiler_valid": valid},
                "output_validation": {"compiler_valid": valid},
            }
        ]
        raw = folder / "results.json"
        raw.write_text(json.dumps(rows))
        manifest = {
            "plantuml_jar_sha256": JAR_SHA,
            "git_commit": "test",
            "output_hashes": {"results.json": hashlib.sha256(raw.read_bytes()).hexdigest()},
        }
        (folder / "manifest.json").write_text(json.dumps(manifest))
        folders.append(folder)
    cache, proof = measured_cache(folders)
    assert cache == {} and len(proof["conflicting_hashes_requiring_recheck"]) == 1
    cache, proof = measured_cache(folders[:1])
    assert len(cache) == 1 and next(iter(cache.values()))["compiler_valid"] is True
    manifest["plantuml_jar_sha256"] = "wrong"
    (folders[1] / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="different JAR"):
        measured_cache(folders)
