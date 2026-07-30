"""PlantUML parsing helpers shared by validators, metrics, and render previews."""

from __future__ import annotations

import re


IDENT = r"[A-Za-z_][A-Za-z0-9_]*"
RELATION_OPERATORS = (
    r"<\|--",
    r"--\|>",
    r"<--",
    r"-->",
    r"<\.\.",
    r"\.\.>",
    r"\*--",
    r"--\*",
    r"o--",
    r"--o",
    r"--",
)

RELATION_PATTERN = re.compile(
    rf"""
    ^\s*
    (?P<src>{IDENT})
    \s*(?:"[^"]*"\s*)?
    (?P<op>{'|'.join(RELATION_OPERATORS)})
    \s*(?:"[^"]*"\s*)?
    (?P<tgt>{IDENT})
    """,
    re.VERBOSE,
)


def parse_classes(plantuml_code: str) -> set[str]:
    classes = set(re.findall(rf"\bclass\s+({IDENT})", plantuml_code))
    interfaces = set(re.findall(rf"\binterface\s+({IDENT})", plantuml_code))
    return classes | interfaces


def parse_relationships(plantuml_code: str) -> set[tuple[str, str]]:
    relationships: set[tuple[str, str]] = set()
    for raw_line in plantuml_code.splitlines():
        line = raw_line.split("'", 1)[0].strip()
        if not line:
            continue
        match = RELATION_PATTERN.match(line)
        if not match:
            continue
        source = match.group("src")
        target = match.group("tgt")
        if source != target:
            relationships.add((source, target))
    return relationships
