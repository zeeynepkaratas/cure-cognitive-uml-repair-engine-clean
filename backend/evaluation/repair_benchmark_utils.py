"""Shared utilities for CURE repair benchmark experiments."""

from __future__ import annotations

import math
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = BACKEND_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from ocl_engine.error_handler import plantuml_syntax_kontrol  # noqa: E402
from ocl_engine.ocl_validator import validate_ocl  # noqa: E402
from plantuml_runtime import validate_with_plantuml  # noqa: E402


MAX_ITERATIONS = 3


def current_commit_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=BACKEND_ROOT.parent,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


def execution_metadata(
    *,
    benchmark: str,
    scope: str,
    max_iterations: int | None,
    model: str | None = None,
    temperature: float | int | None = None,
    **extra,
) -> dict:
    metadata = {
        "commit_sha": current_commit_sha(),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "benchmark": benchmark,
        "scope": scope,
        "model": model,
        "temperature": temperature,
        "max_iterations": max_iterations,
        "openai_api_key_present": bool(os.getenv("OPENAI_API_KEY")),
    }
    metadata.update(extra)
    return metadata


def compile_check(plantuml_code: str) -> dict:
    syntax = plantuml_syntax_kontrol(plantuml_code)
    ocl = validate_ocl(plantuml_code)
    plantuml_runtime = validate_with_plantuml(plantuml_code)
    project_defined_success = syntax["gecerli"] and ocl["gecerli_mi"]
    plantuml_validated_success = (
        plantuml_runtime["successful"] if plantuml_runtime["available"] else None
    )
    errors = syntax["hatalar"] + ocl["hatalar"]
    if plantuml_runtime["available"] and plantuml_runtime["successful"] is False:
        errors.extend(plantuml_runtime["errors"])
    warnings = ocl["uyarilar"]
    return {
        "successful": project_defined_success,
        "success_definition": "project_defined_lightweight_validation",
        "project_defined_success": project_defined_success,
        "plantuml_validated_success": plantuml_validated_success,
        "plantuml_runtime_available": plantuml_runtime["available"],
        "syntax_valid": syntax["gecerli"],
        "ocl_valid": ocl["gecerli_mi"],
        "plantuml_runtime": plantuml_runtime,
        "score": ocl["skor"],
        "percent": ocl["yuzde"],
        "errors": errors,
        "warnings": warnings,
        "class_count": ocl["sinif_sayisi"],
        "relationship_count": ocl["iliski_sayisi"],
    }


def deterministic_backend_repair(plantuml_code: str) -> tuple[str, list[str]]:
    """Mirror the local backend's deterministic repair scope."""
    actions: list[str] = []
    code = plantuml_code.strip()

    if "@startuml" not in code:
        code = "@startuml\n" + code
        actions.append("added_missing_startuml")

    if "@enduml" not in code:
        code = code + "\n@enduml"
        actions.append("added_missing_enduml")

    if "class " not in code:
        code = code.replace("@enduml", "class GeneratedDiagram {}\n@enduml")
        actions.append("inserted_generated_class_for_empty_diagram")

    if not actions:
        actions.append("no_supported_repair_action")

    return code, actions


def wilson_interval(successes: int, total: int, z: float = 1.96) -> dict:
    if total <= 0:
        raise ValueError("total must be positive")
    phat = successes / total
    denominator = 1 + z**2 / total
    center = (phat + z**2 / (2 * total)) / denominator
    margin = z * math.sqrt((phat * (1 - phat) + z**2 / (4 * total)) / total) / denominator
    return {
        "successes": successes,
        "total": total,
        "rate": phat,
        "lower": center - margin,
        "upper": center + margin,
        "z": z,
    }
