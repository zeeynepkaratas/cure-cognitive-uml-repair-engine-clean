"""Independent project/compiler checks used by all v4 conditions."""

from subprocess import TimeoutExpired
from backend.src.ocl_engine.error_handler import plantuml_syntax_kontrol
from backend.src.ocl_engine.ocl_validator import validate_ocl
from backend.src.plantuml_runtime import validate_with_plantuml


def check_diagram(code: str, legacy: bool = False) -> dict:
    syntax = plantuml_syntax_kontrol(code, legacy=legacy)
    ocl = validate_ocl(code, legacy=legacy)
    try:
        compiler = validate_with_plantuml(code)
    except (OSError, TimeoutError, TimeoutExpired) as exc:
        compiler = {"available": False, "successful": None, "errors": [type(exc).__name__ + ": " + str(exc)]}
    return {
        "project_valid": syntax["gecerli"] and ocl["gecerli_mi"],
        "compiler_valid": compiler["successful"] if compiler["available"] else None,
        "compiler_available": compiler["available"],
        "compiler_errors": compiler.get("errors", []),
        "project_errors": syntax["hatalar"] + ocl["hatalar"],
        "warnings": ocl["uyarilar"],
        "rule_results": ocl["detaylar"],
        "compiler": compiler,
    }
