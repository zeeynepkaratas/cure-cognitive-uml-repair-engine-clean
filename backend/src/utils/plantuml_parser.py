"""PlantUML parsing helpers shared by validators, metrics, and render previews."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import NamedTuple


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
    (?P<op>{"|".join(RELATION_OPERATORS)})
    \s*(?:"[^"]*"\s*)?
    (?P<tgt>{IDENT})
    """,
    re.VERBOSE,
)


def strip_comments(code: str, mask_strings: bool = False) -> str:
    """Preserve offsets/newlines while removing comments and optional literals."""
    out = list(code)
    i = 0
    quote = False
    while i < len(code):
        if code[i] == '"':
            quote = not quote
            if mask_strings:
                out[i] = " "
            i += 1
        elif quote:
            if code[i] == "\\" and i + 1 < len(code):
                if mask_strings:
                    out[i] = out[i + 1] = " "
                i += 2
            else:
                if mask_strings and code[i] != "\n":
                    out[i] = " "
                i += 1
        elif code.startswith("/'", i):
            end = code.find("'/", i + 2)
            end = len(code) if end < 0 else end + 2
            for k in range(i, end):
                if code[k] != "\n":
                    out[k] = " "
            i = end
        elif code[i] == "'":
            end = code.find("\n", i)
            end = len(code) if end < 0 else end
            out[i:end] = " " * (end - i)
            i = end
        else:
            i += 1
    return "".join(out)


@dataclass(frozen=True)
class ClassDeclaration:
    name: str
    kind: str
    attributes: tuple[str, ...] = ()
    methods: tuple[str, ...] = ()
    start: int = 0
    end: int = 0
    body: str = ""


class Relationship(NamedTuple):
    src: str
    tgt: str
    type: str
    src_mult: str = ""
    tgt_mult: str = ""
    label: str = ""


@dataclass
class UMLModel:
    declarations: list[ClassDeclaration]
    relationships: list[Relationship]


NAME = r'(?:"[^"\n]+"|[A-Za-z_][\w.]*)'
DECLARATION = re.compile(r"\b(abstract\s+class|class|interface|enum)\s+")
OPERATORS = sorted(
    [
        "<|--",
        "--|>",
        "<|..",
        "..|>",
        "*--",
        "--*",
        "o--",
        "--o",
        "-->",
        "<--",
        "->",
        "<-",
        "..>",
        "<..",
        "--",
        "..",
    ],
    key=len,
    reverse=True,
)


def parse_model(code: str) -> UMLModel:
    """Parse class declarations and typed relations; no compiler-validity claim.

    Comments and quoted literals cannot create declarations. Aliases are the
    logical names. Brace matching honours nested bodies, strings and comments.
    Directional arrowheads determine source/target; a diamond marks the whole.
    """
    clean = strip_comments(code)
    masked = strip_comments(code, mask_strings=True)
    declarations = []
    for match in DECLARATION.finditer(masked):
        name_start = match.end(1)
        name_match = re.match(r"\s*(" + NAME + ")", clean[name_start:])
        if not name_match:
            continue
        name = name_match.group(1).strip('"')
        if name in {"class", "interface", "enum", "abstract", "as"}:
            continue
        end = name_start + name_match.end()
        alias = re.match(r"\s+as\s+(" + NAME + ")", clean[end:])
        if alias:
            name = alias.group(1).strip('"')
            end += alias.end()
        opening = re.match(r"[^\n{}]*\{", masked[end:])
        body = ""
        if opening:
            start_body = end + opening.end()
            depth = 1
            k = start_body
            while k < len(masked) and depth:
                depth += (masked[k] == "{") - (masked[k] == "}")
                k += 1
            body = clean[start_body : k - 1 if depth == 0 else k]
            end = k
        attributes, methods = [], []
        for line in body.splitlines():
            member = line.strip()
            if not member or member.startswith(("{", "}", "//", "--", "..")):
                continue
            if "(" in member:
                methods.append(member)
            elif re.match(r"^[+\-#~]?\s*[A-Za-z_]\w*(?:\s*:|\s*=|\s*$)", member):
                attributes.append(member)
        declarations.append(
            ClassDeclaration(
                name, match.group(1), tuple(attributes), tuple(methods), match.start(), end, body
            )
        )
    relationships = []
    for line in clean.splitlines():
        # Style directives are removed only from arrow syntax, not from labels.
        line = re.sub(r"(?<=[.\-])\[[^\]\n]+\]", "", line)
        pattern = (
            r"^\s*("
            + NAME
            + r')\s*(?:"([^"]*)"\s*)?('
            + "|".join(re.escape(op) for op in OPERATORS)
            + r')\s*(?:"([^"]*)"\s*)?('
            + NAME
            + r")(?:\s*:\s*(.*))?\s*$"
        )
        m = re.match(pattern, line)
        if not m:
            continue
        src, sm, op, tm, tgt, label = m.groups()
        src, tgt = src.strip('"'), tgt.strip('"')
        kind = (
            "realization"
            if "|" in op and "." in op
            else "inheritance"
            if "|" in op
            else "composition"
            if "*" in op
            else "aggregation"
            if "o" in op
            else "dependency"
            if "." in op
            else "association"
        )
        reverse = op.startswith("<") or op.endswith(("*", "o"))
        if reverse:
            src, tgt, sm, tm = tgt, src, tm, sm
        relationships.append(Relationship(src, tgt, kind, sm or "", tm or "", label or ""))
    return UMLModel(declarations, relationships)


def parse_classes(plantuml_code: str, legacy: bool = False) -> set[str]:
    if legacy:
        return set(re.findall(rf"\bclass\s+({IDENT})", plantuml_code)) | set(
            re.findall(rf"\binterface\s+({IDENT})", plantuml_code)
        )
    return {decl.name for decl in parse_model(plantuml_code).declarations}


def parse_relationships(plantuml_code: str, legacy: bool = False) -> set[tuple[str, str]]:
    if not legacy:
        return {(rel.src, rel.tgt) for rel in parse_model(plantuml_code).relationships}
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
