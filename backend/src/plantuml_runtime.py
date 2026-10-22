"""Optional real PlantUML runtime integration.

The repository does not bundle PlantUML. When `PLANTUML_JAR` or `PLANTUML_CMD`
is configured, these helpers call the real PlantUML runtime for validation and
rendering. When it is unavailable, callers get an explicit `available=False`
result instead of a synthetic success.
"""

from __future__ import annotations

import base64
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def _runtime_command(output_format: str) -> list[str] | None:
    jar = os.getenv("PLANTUML_JAR")
    if jar:
        jar_path = Path(jar)
        if jar_path.exists():
            return ["java", "-jar", str(jar_path), f"-t{output_format}"]

    configured_cmd = os.getenv("PLANTUML_CMD")
    if configured_cmd:
        return [configured_cmd, f"-t{output_format}"]

    discovered = shutil.which("plantuml")
    if discovered:
        return [discovered, f"-t{output_format}"]

    return None


def plantuml_runtime_available() -> bool:
    return _runtime_command("svg") is not None


def validate_with_plantuml(plantuml_code: str, timeout_seconds: int = 20) -> dict:
    command = _runtime_command("svg")
    if not command:
        return {
            "available": False,
            "successful": None,
            "errors": ["PlantUML runtime not available. Set PLANTUML_JAR or PLANTUML_CMD."],
            "stderr": "",
        }

    with tempfile.TemporaryDirectory() as tmpdir:
        source = Path(tmpdir) / "diagram.puml"
        source.write_text(plantuml_code, encoding="utf-8")
        completed = subprocess.run(
            [*command, "-checkonly", str(source)],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    stderr = (completed.stderr or "").replace(tmpdir, "<TEMP>").strip()
    stdout = (completed.stdout or "").replace(tmpdir, "<TEMP>").strip()
    return {
        "available": True,
        "successful": completed.returncode == 0,
        "errors": [] if completed.returncode == 0 else [stderr or stdout or "PlantUML validation failed."],
        "stderr": stderr,
        "stdout": stdout,
        "returncode": completed.returncode,
    }


def render_with_plantuml(plantuml_code: str, timeout_seconds: int = 20) -> dict:
    command = _runtime_command("svg")
    if not command:
        return {
            "available": False,
            "successful": False,
            "error": "PlantUML runtime not available. Set PLANTUML_JAR or PLANTUML_CMD.",
        }

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        source = tmp / "diagram.puml"
        source.write_text(plantuml_code, encoding="utf-8")
        completed = subprocess.run(
            [*command, str(source)],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        svg_path = tmp / "diagram.svg"
        if completed.returncode != 0 or not svg_path.exists():
            return {
                "available": True,
                "successful": False,
                "error": (completed.stderr or completed.stdout or "PlantUML render failed.")
                .replace(tmpdir, "<TEMP>")
                .strip(),
                "returncode": completed.returncode,
            }
        svg = svg_path.read_text(encoding="utf-8")
    return {
        "available": True,
        "successful": True,
        "svg": svg,
        "svg_base64": base64.b64encode(svg.encode("utf-8")).decode("ascii"),
    }
