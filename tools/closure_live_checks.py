"""Opt-in local JVM/HTTP closure checks. No model or external HTTP calls."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.pop("OPENAI_API_KEY", None)
from fastapi.testclient import TestClient
from backend.src import security_runtime_v5 as secure
from backend.src.api import endpoints
from backend.src.utils.plantuml_parser import parse_model

FIXTURES = {
    "normal": "@startuml\nclass A {}\n@enduml",
    "malformed": "@startuml\nclass A {}\n--> A\n@enduml",
    "note_declaration": "@startuml\nclass A {}\nnote as N\nclass Ghost\nend note\n@enduml",
    "compound_arrow": "@startuml\nclass A {}\nclass B {}\nA *--> B\n@enduml",
}


def main():
    def no_model(*args, **kwargs):
        raise AssertionError("No model invocation allowed in closure audit")

    endpoints.UMLRepairAgent = no_model
    endpoints.UMLMultiAgentSystem = no_model
    checks = {}
    for name, code in FIXTURES.items():
        result = secure.validate_untrusted_plantuml(code)
        model = parse_model(code)
        checks[name] = {
            "fixture": code,
            "compiler": result,
            "parser_classes": [c.name for c in model.declarations],
            "parser_relationships": [list(r) for r in model.relationships],
        }
    with TestClient(endpoints.app) as client:
        cases = [
            ("directive", "/api/render", {"plantuml_kodu": "!include /closure-canary"}, 422),
            ("body_limit", "/api/render", {"plantuml_kodu": " " * 140000}, 413),
            ("legacy_disabled", "/api/autonomous-repair", {"plantuml_kodu": FIXTURES["normal"], "legacy": True}, 422),
            ("normal_render", "/api/render", {"plantuml_kodu": FIXTURES["normal"]}, 200),
        ]
        http = {}
        for name, route, data, expected in cases:
            response = client.post(route, json=data)
            http[name] = {"status_code": response.status_code, "expected": expected}
            assert response.status_code == expected, (name, response.text[:200])
            if name == "normal_render":
                result = response.json()
                # Retain only runtime status, never an echoed request or absolute path.
                http[name]["keys"] = sorted(result)
                render = result["render"]
                http[name]["runtime"] = render.get("plantuml_runtime")
                http[name]["statuses"] = {k: result.get(k) for k in ("project_valid", "compiler_valid", "critic_valid", "basarili")}
                assert render.get("svg") and render["plantuml_runtime"]["successful"] is True
    assert checks["normal"]["compiler"]["successful"] is True
    assert checks["malformed"]["compiler"]["successful"] is False
    assert checks["note_declaration"]["compiler"]["successful"] is True
    assert checks["compound_arrow"]["compiler"]["successful"] is True
    jar = Path(os.environ["PLANTUML_JAR"])
    report = {
        "status": "PASS",
        "model_calls": 0,
        "scope": "Local in-process HTTP and pinned JVM; no provider/network service or load test",
        "jar_sha256": hashlib.sha256(jar.read_bytes()).hexdigest(),
        "java_version": subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=15).stderr.strip(),
        "fixtures": checks,
        "http": http,
        "known_parser_failures": ["note text creates a Ghost declaration", "valid compound arrow is omitted"],
    }
    assert report["jar_sha256"] == secure.JAR_SHA256
    (ROOT / "docs/closure_audit/LIVE_RUNTIME_CHECKS.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "compiler_fixtures": 4, "http_checks": 4, "model_calls": 0}))


if __name__ == "__main__":
    main()
