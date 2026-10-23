"""Frozen failure observations and API-only containment; never fabricate evidence."""

import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from pydantic import ValidationError
from backend.src import security_runtime_v5 as secure
from backend.src.api import endpoints
from backend.src.utils.plantuml_parser import parse_model

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_m11_failure_is_preserved_not_declared_fixed():
    directory = ROOT / "backend/evaluation/results_v4/test-frozen-20261022/cases"
    for rep in range(1, 6):
        row = json.loads((directory / f"C7_M11_2_{rep}.json").read_text(encoding="utf-8"))
        assert "WeatherStation" not in row["srs"]
        assert "WeatherStation" in {c.name for c in parse_model(row["output_plantuml"]).declarations}
        assert row["critic_valid"] is True and row["terminated_by"] == "accepted"
        assert row["metrics"]["reference_class"]["f1"] == pytest.approx(8 / 9)
        assert row["metrics"]["reference_class"]["spurious"] == ["weatherstation"]


@pytest.mark.parametrize(
    "code",
    [
        "!include /private/file",
        "!includeurl https://example.invalid/a",
        'title %getenv("OPENAI_API_KEY")',
        "<img:file:///private/file>",
        "class A [[javascript:alert(1)]]",
        "class A\x00",
        "x" * 20001,
        "class A {}\n" * 257,
    ],
)
def test_restricted_api_input_rejected_without_subprocess(code, monkeypatch):
    monkeypatch.setattr(secure.subprocess, "run", lambda *a, **k: pytest.fail("Forbidden subprocess"))
    result = secure.validate_untrusted_plantuml(code)
    assert result["successful"] is None and result["policy_rejected"] is True


def test_large_body_and_directive_rejected_without_model_calls(monkeypatch):
    monkeypatch.setattr(endpoints, "UMLRepairAgent", lambda *a, **k: pytest.fail("No API call permitted"))
    with pytest.raises(ValidationError):
        endpoints.UMLDogrulamaGirdisi(plantuml_kodu="!include /private")
    with pytest.raises(ValidationError):
        endpoints.AutonomousRepairRequest(plantuml_kodu="x" * 20001)
    messages = []

    async def receive():
        return {"type": "http.request", "body": b" " * (secure.MAX_BODY_BYTES + 1)}

    async def send(message):
        messages.append(message)

    async def forbidden(*args):
        pytest.fail("Oversized body must not reach the application")

    coroutine = secure.BoundedBodyMiddleware(forbidden)({"type": "http"}, receive, send)
    with pytest.raises(StopIteration):
        coroutine.send(None)
    assert messages[0]["status"] == 413


def test_sandbox_command_no_shell_and_child_credentials_removed(monkeypatch, tmp_path):
    monkeypatch.setattr(secure, "_verified_jar", lambda *args: True)
    jar = tmp_path / "jar"
    jar.write_bytes(b"fixture")
    monkeypatch.setenv("PLANTUML_JAR", str(jar))
    monkeypatch.setenv("OPENAI_API_KEY", "private-test-value")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "private-test-value")
    calls = []

    def run(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(secure.subprocess, "run", run)
    assert secure.validate_untrusted_plantuml("@startuml\nclass A {}\n@enduml")["successful"] is True
    command, options = calls[0]
    assert "-DPLANTUML_SECURITY_PROFILE=SANDBOX" in command and "-Xmx256m" in command
    assert "-Duser.language=en" in command and "-Duser.country=US" in command
    assert options["timeout"] == 20 and not options.get("shell", False)
    assert "OPENAI_API_KEY" not in options["env"] and "AWS_SECRET_ACCESS_KEY" not in options["env"]


def test_busy_timeout_and_svg_active_content(monkeypatch, tmp_path):
    monkeypatch.setattr(secure, "_verified_jar", lambda *args: True)
    jar = tmp_path / "jar"
    jar.write_bytes(b"fixture")
    monkeypatch.setenv("PLANTUML_JAR", str(jar))
    monkeypatch.setattr(secure, "SLOTS", __import__("threading").BoundedSemaphore(1))
    secure.SLOTS.acquire()
    assert secure.validate_untrusted_plantuml("class A {}")["busy"] is True
    secure.SLOTS.release()

    def timeout(*args, **kwargs):
        raise secure.subprocess.TimeoutExpired(["private-path"], 20)

    monkeypatch.setattr(secure.subprocess, "run", timeout)
    result = secure.validate_untrusted_plantuml("class A {}")
    assert result["successful"] is None and "private-path" not in str(result)
    assert secure.SLOTS.acquire(blocking=False)
    secure.SLOTS.release()
    svg = secure.sanitize_svg(
        '<svg xmlns="http://www.w3.org/2000/svg" onload="bad()"><script>bad()</script><foreignObject/><use href="javascript:bad()"/><rect style="fill:url(https://example.invalid)"/></svg>'
    )
    assert all(s not in svg for s in ["onload", "script", "foreignObject", "javascript", "https:"])
    with pytest.raises(ValueError):
        secure.sanitize_svg('<!DOCTYPE svg [<!ENTITY a "b">]><svg/>')


def test_gold_is_only_used_in_posthoc_evaluation(monkeypatch):
    from backend.evaluation import run_matrix as matrix
    from ai_core.src.ai.repair_agent import UMLRepairAgent
    from tests.test_repair_agent import ScriptedClient, GOOD, validation

    client = ScriptedClient([GOOD])
    monkeypatch.setattr(matrix, "cached_check", lambda code: {**validation(code), "warnings": []})
    monkeypatch.setattr(
        matrix, "UMLRepairAgent", lambda config, **kw: UMLRepairAgent(config, client, matrix.cached_check)
    )
    args = SimpleNamespace(prompt_revision="v4.1", seed=1729, model_critic="unused", model_healer="unused")
    case = {
        "case_id": "fixture",
        "srs": "Document stores content.",
        "input_plantuml": GOOD,
        "gold": "@startuml\nclass GoldSentinelNotInRequest {}\n@enduml",
    }
    row = matrix.evaluate(case, "C3", 1, args, SimpleNamespace(reserve=lambda *a: None))
    assert row["metrics"] is not None
    assert client.calls and all("GoldSentinelNotInRequest" not in text for role, text in client.calls)


def test_freeze_verification_covers_changed_runner_and_agent_parser(monkeypatch):
    import tools.finalize_v4 as finalize

    def changed(args, **kwargs):
        assert "backend/evaluation/run_matrix.py" in args and "ai_core/src" in args
        return "backend/evaluation/run_matrix.py\n"

    monkeypatch.setattr(finalize.subprocess, "check_output", changed)
    with pytest.raises(ValueError, match="changed after freeze"):
        finalize.verify_generation_freeze("fixture-commit")


def test_frozen_parser_note_text_false_class_is_an_open_boundary():
    # Preserve the observed limitation; do not tune a frozen metric after test.
    code = "@startuml\nclass A {}\nnote as N\nclass Ghost\nend note\n@enduml"
    assert {c.name for c in parse_model(code).declarations} == {"A", "Ghost"}


def test_frozen_parser_omits_valid_compound_arrow():
    code = "@startuml\nclass A {}\nclass B {}\nA *--> B\n@enduml"
    assert parse_model(code).relationships == []
