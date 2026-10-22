"""Optional pinned-compiler smoke checks; the normal suite remains JVM-free."""

import os
from pathlib import Path
import shutil
import pytest
from backend.src.plantuml_runtime import validate_with_plantuml

AVAILABLE = bool(
    os.getenv("PLANTUML_JAR") and Path(os.environ["PLANTUML_JAR"]).is_file() and shutil.which("java")
)


@pytest.mark.compiler
@pytest.mark.skipif(not AVAILABLE, reason="Pinned PlantUML JAR and Java not configured")
@pytest.mark.parametrize(
    ("code", "expected"),
    [("@startuml\nclass A {}\n@enduml", True), ("@startuml\nclass A {}\n--> A\n@enduml", False)],
)
def test_real_compiler_smoke(code, expected):
    result = validate_with_plantuml(code)
    assert result["available"] is True
    assert result["successful"] is expected
