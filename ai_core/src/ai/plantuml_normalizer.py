"""Utilities for normalizing PlantUML returned by LLM components."""

from __future__ import annotations

import re


FENCE_PATTERN = re.compile(r"```(?:plantuml|puml|uml)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)


def _strip_fence_lines(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def normalize_plantuml_text(raw_text: str | None) -> str:
    """Extract a clean PlantUML block from an LLM response.

    The Healer prompt asks for only PlantUML code, but real LLM responses may
    include Markdown fences or short explanatory prose. This function keeps the
    first fenced PlantUML-like block when present, then trims any prose before
    `@startuml` and after `@enduml`.
    """
    if raw_text is None:
        return ""

    text = str(raw_text).strip().replace("\ufeff", "")
    if not text:
        return ""

    fenced_blocks = FENCE_PATTERN.findall(text)
    if fenced_blocks:
        text = next(
            (
                block
                for block in fenced_blocks
                if "@startuml" in block.lower() or "@enduml" in block.lower()
            ),
            fenced_blocks[0],
        )

    text = _strip_fence_lines(text)
    lowered = text.lower()
    start = lowered.find("@startuml")
    end = lowered.find("@enduml")

    if start != -1:
        if end != -1 and end >= start:
            end += len("@enduml")
            return text[start:end].strip()
        return text[start:].strip()

    if end != -1:
        return text[: end + len("@enduml")].strip()

    return text.strip()
