from tools.sanitize_artifact import numeric_values, redact


def test_identity_redaction_preserves_other_text():
    assert "<REDACTED_PATH>" in redact(
        "Error " + chr(92).join(["C:", "Users", "example", "Temp", "diagram.puml"])
    )
    assert "anonymous@example.invalid" in redact("author@example.org")
    assert redact("rate=0.82, compiler=True") == "rate=0.82, compiler=True"


def test_numeric_fingerprint_tracks_types_and_paths():
    original = {"path": "private", "rate": 0.82, "ok": True, "rows": [1, None]}
    cleaned = {**original, "path": "redacted"}
    assert numeric_values(original) == numeric_values(cleaned)
    assert numeric_values(original) != numeric_values({**cleaned, "ok": 1})
