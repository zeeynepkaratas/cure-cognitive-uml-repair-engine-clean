"""Versioned API-only containment; the frozen v4 research runner is unchanged.

This is a restricted class-diagram service, not a general PlantUML execution
service. Authentication/rate quotas and an OS container remain deployment work.
"""

import base64
from functools import lru_cache
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile
import threading
import xml.etree.ElementTree as ET

from backend.src.ocl_engine.error_handler import plantuml_syntax_kontrol
from backend.src.ocl_engine.ocl_validator import validate_ocl

PROFILE = "v5-api-sandbox"
JAR_SHA256 = "89948f14c93756c7a3fb7b69078ff37e8489fd79dd430c582b931e2f65358690"
MAX_UML_CHARS = 20000
MAX_SRS_CHARS = 64000
MAX_BODY_BYTES = 128 * 1024
SLOTS = threading.BoundedSemaphore(2)


@lru_cache(maxsize=8)
def _verified_jar(path, size, modified_ns):
    """Operator file identity invalidates the process-local checksum cache."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest() == JAR_SHA256


def input_policy(code):
    if len(code) > MAX_UML_CHARS or len(code.encode("utf-8")) > 65536:
        raise ValueError("PlantUML exceeds the API size limit")
    if any(ord(c) < 32 and c not in "\r\n\t" for c in code):
        raise ValueError("PlantUML contains a control character")
    if len(code.splitlines()) > 2000 or len(re.findall(r"\b(?:class|interface|enum)\s+", code)) > 256:
        raise ValueError("PlantUML exceeds the API structural limit")
    if re.search(r"(?m)^\s*!|%[A-Za-z_]\w*\s*\(|\[\[|<(?:img|image)\b|javascript:|file:|data:", code, re.I):
        raise ValueError("Preprocessing, resource loading and embedded links are disabled in the API")
    return code


class BoundedBodyMiddleware:
    """Bound bytes before JSON decoding, including chunked request bodies."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        parts, size = [], 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            body = message.get("body", b"")
            size += len(body)
            if size > MAX_BODY_BYTES:
                await send(
                    {
                        "type": "http.response.start",
                        "status": 413,
                        "headers": [(b"content-type", b"application/json")],
                    }
                )
                await send(
                    {"type": "http.response.body", "body": b'{"detail":"Request body exceeds API limit"}'}
                )
                return
            parts.append(body)
            if not message.get("more_body", False):
                break
        delivered = False

        async def bounded_receive():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": b"".join(parts), "more_body": False}
            return await receive()

        await self.app(scope, bounded_receive, send)


def sanitize_svg(svg):
    if len(svg.encode("utf-8")) > 2 * 1024 * 1024 or re.search(r"<!DOCTYPE|<!ENTITY", svg, re.I):
        raise ValueError("SVG exceeds the API policy")
    root = ET.fromstring(svg)
    allowed = {
        "svg",
        "g",
        "defs",
        "style",
        "rect",
        "path",
        "line",
        "ellipse",
        "polygon",
        "polyline",
        "text",
        "tspan",
        "title",
        "desc",
        "circle",
        "marker",
        "linearGradient",
        "radialGradient",
        "stop",
        "clipPath",
        "filter",
        "feGaussianBlur",
        "feOffset",
        "feBlend",
        "feColorMatrix",
        "pattern",
        "symbol",
        "use",
    }

    def local(tag):
        return tag.rsplit("}", 1)[-1]

    if local(root.tag) != "svg":
        raise ValueError("Renderer did not return SVG")
    for parent in list(root.iter()):
        for child in list(parent):
            if local(child.tag) not in allowed:
                parent.remove(child)
        for key, value in list(parent.attrib.items()):
            name = local(key).lower()
            external_css = re.search(r"url\(\s*['\"]?(?!#)|@import", value, re.I)
            if name.startswith("on") or (name == "href" and not value.startswith("#")) or external_css:
                del parent.attrib[key]
        if local(parent.tag) == "style" and re.search(r"url\(|@import", parent.text or "", re.I):
            parent.text = ""
    return ET.tostring(root, encoding="unicode")


def _run(code, render=False):
    base = {"available": False, "successful": None, "errors": [], "security_profile": PROFILE}
    try:
        input_policy(code)
    except ValueError as exc:
        return {**base, "errors": [str(exc)], "policy_rejected": True}
    jar = Path(os.getenv("PLANTUML_JAR", ""))
    if not jar.is_file():
        return {**base, "errors": ["Pinned JAR is not configured for the secure API"]}
    try:
        stat = jar.stat()
        if not _verified_jar(str(jar.resolve()), stat.st_size, stat.st_mtime_ns):
            return {**base, "errors": ["PlantUML JAR checksum mismatch"]}
    except OSError:
        return {**base, "errors": ["PlantUML JAR cannot be verified"]}
    if not SLOTS.acquire(blocking=False):
        return {**base, "errors": ["Compiler capacity is busy"], "busy": True}
    try:
        # Do not forward model credentials or unrelated host environment to Java.
        env = {
            k: v
            for k, v in os.environ.items()
            if k.upper() in {"PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "JAVA_HOME", "LANG", "LC_ALL"}
        }
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "diagram.puml"
            source.write_text(code, encoding="utf-8")
            command = [
                "java", "-Xmx256m", "-DPLANTUML_SECURITY_PROFILE=SANDBOX",
                "-Duser.language=en", "-Duser.country=US", "-jar", str(jar), "-tsvg",
            ]
            if not render:
                command.append("-checkonly")
            command.append(str(source))
            response = subprocess.run(
                command, cwd=directory, env=env, capture_output=True, text=True, timeout=20, check=False
            )
            result = {
                **base,
                "available": True,
                "successful": response.returncode == 0,
                "returncode": response.returncode,
                "errors": [] if response.returncode == 0 else ["PlantUML rejected the diagram"],
            }
            if render and response.returncode == 0:
                path = Path(directory) / "diagram.svg"
                if not path.is_file() or path.stat().st_size > 2 * 1024 * 1024:
                    return {**result, "successful": False, "errors": ["SVG unavailable or exceeds API limit"]}
                svg = sanitize_svg(path.read_text(encoding="utf-8"))
                result.update(svg=svg, svg_base64=base64.b64encode(svg.encode()).decode())
            return result
    except (OSError, subprocess.TimeoutExpired, ValueError, ET.ParseError) as exc:
        return {**base, "errors": [type(exc).__name__ + ": compiler unavailable or output rejected"]}
    finally:
        SLOTS.release()


def validate_untrusted_plantuml(code):
    return _run(code)


def render_untrusted_plantuml(code):
    result = _run(code, render=True)
    # Preserve the old JSON contract; this pixel is not a rendered UML PNG.
    png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
    return {
        "svg": result.get("svg", ""),
        "svg_base64": result.get("svg_base64", ""),
        "png_base64": png,
        "png_data_uri": "data:image/png;base64," + png,
        "png_is_placeholder": True,
        "formatlar": ["svg", "png"],
        "render_source": PROFILE,
        "plantuml_runtime": {k: v for k, v in result.items() if k not in {"svg", "svg_base64"}},
    }


def check_untrusted_diagram(code):
    compiler = validate_untrusted_plantuml(code)
    try:
        input_policy(code)
    except ValueError:
        return {
            "project_valid": None,
            "compiler_valid": None,
            "compiler_available": False,
            "compiler_errors": compiler["errors"],
            "project_errors": [],
            "warnings": [],
            "rule_results": [],
            "compiler": compiler,
            "security_valid": False,
        }
    syntax, ocl = plantuml_syntax_kontrol(code), validate_ocl(code)
    return {
        "project_valid": syntax["gecerli"] and ocl["gecerli_mi"],
        "compiler_valid": compiler["successful"] if compiler["available"] else None,
        "compiler_available": compiler["available"],
        "compiler_errors": compiler["errors"],
        "project_errors": syntax["hatalar"] + ocl["hatalar"],
        "warnings": ocl["uyarilar"],
        "rule_results": ocl["detaylar"],
        "compiler": compiler,
        "security_valid": True,
    }
