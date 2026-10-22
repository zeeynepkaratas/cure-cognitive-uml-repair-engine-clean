from pathlib import Path
import hashlib
import json


def test_legacy_prompt_values_are_byte_identical_to_v3_literals():
    root = Path(__file__).resolve().parents[1]
    fixture = json.loads((root / "tests/fixtures/legacy_prompt_hashes.json").read_text(encoding="utf-8"))
    for name, expected in fixture["sha256_utf8_literal"].items():
        text = (root / f"ai_core/prompts/legacy/{name}_prompt.txt").read_text(encoding="utf-8")
        assert hashlib.sha256(text.encode("utf-8")).hexdigest() == expected
