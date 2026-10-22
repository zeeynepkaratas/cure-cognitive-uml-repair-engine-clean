from types import SimpleNamespace
from backend.src import plantuml_runtime


def test_compiler_diagnostics_do_not_expose_temporary_paths(monkeypatch):
    monkeypatch.setattr(plantuml_runtime, "_runtime_command", lambda *args: ["java"])

    def response(*args, **kwargs):
        return SimpleNamespace(returncode=1, stderr=kwargs["cwd"] + "/diagram.puml: error", stdout="")

    monkeypatch.setattr(plantuml_runtime.subprocess, "run", response)
    result = plantuml_runtime.validate_with_plantuml("invalid")
    assert result["stderr"] == "<TEMP>/diagram.puml: error"
