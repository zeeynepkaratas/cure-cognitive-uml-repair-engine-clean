"""Explicit minimal and extended deterministic repair conditions (no SRS oracle)."""

from __future__ import annotations

import re

from backend.src.utils.plantuml_parser import parse_model, strip_comments


def deterministic_minimal(code: str) -> tuple[str, list[str]]:
    from backend.evaluation.repair_benchmark_utils import deterministic_backend_repair

    return deterministic_backend_repair(code)


def deterministic_extended(code: str) -> tuple[str, list[str]]:
    """Apply conservative, logged structural repairs without access to gold data."""
    actions = []
    source = code.strip()
    source = re.sub(r"^```(?:plantuml|puml)?\s*|\s*```$", "", source, flags=re.I)
    lines = source.splitlines()
    kept, depth = [], 0
    for line in lines:
        clean = strip_comments(line, mask_strings=True).strip()
        if re.match(r"^@(?:startuml|enduml)\b", clean):
            actions.append("normalised_boundary_token")
            continue
        if re.fullmatch(r"(?:abstract\s+)?class\s*(?:\{\s*\})?", clean):
            actions.append("removed_nameless_class")
            continue
        if re.match(r"^(?:abstract\s+class|class|interface|enum)\s+", clean) and depth:
            kept.extend("}" for _ in range(depth))
            actions.append("closed_unterminated_class_before_next_declaration")
            depth = 0
        masked = strip_comments(line, mask_strings=True)
        chars = list(line)
        for i, char in enumerate(masked):
            if char == "{":
                depth += 1
            elif char == "}":
                if depth:
                    depth -= 1
                else:
                    chars[i] = ""
                    actions.append("removed_dangling_closing_brace")
        kept.append("".join(chars))
    if depth:
        kept.extend("}" for _ in range(depth))
        actions.append("closed_dangling_open_braces")
    source = "\n".join(kept)
    model = parse_model(source)
    groups = {}
    for declaration in model.declarations:
        groups.setdefault(declaration.name, []).append(declaration)
    replacements = []
    for name, declarations in groups.items():
        if len(declarations) < 2:
            continue
        bodies = list(
            dict.fromkeys(line.strip() for d in declarations for line in d.body.splitlines() if line.strip())
        )
        merged = declarations[0].kind + " " + name + " {\n" + "\n".join(bodies) + "\n}"
        for i, declaration in enumerate(declarations):
            replacements.append((declaration.start, declaration.end, merged if i == 0 else ""))
        actions.append("merged_duplicate_declarations:" + name)
    for start, end, replacement in sorted(replacements, reverse=True):
        source = source[:start] + replacement + source[end:]
    model = parse_model(source)
    names = {d.name for d in model.declarations}
    kept = []
    for line in source.splitlines():
        rels = parse_model(line).relationships
        if rels and any(r.src not in names or r.tgt not in names for r in rels):
            actions.append("removed_relation_with_undeclared_endpoint:" + line.strip())
            continue
        clean = strip_comments(line, mask_strings=True).strip()
        if not rels and re.match(r"^(?:[<*o|]+)?[-.][-.<>|*o\[\]#\w,]*", clean):
            actions.append("removed_truncated_relation_without_source:" + line.strip())
            continue
        if (
            not rels
            and re.match(r'^\w+\s+(?:"[^"]*"\s*)?(?:[-.][-.<>|*o\[\]#\w,]*)', clean)
            and not re.match(r"^(class|interface|enum|abstract)\b", clean)
        ):
            actions.append("removed_truncated_relation:" + line.strip())
            continue
        kept.append(line)
    if not names:
        kept.append("class GeneratedDiagram {}")
        actions.append("inserted_placeholder_for_no_declarations")
    repaired = "@startuml\n" + "\n".join(line for line in kept if line.strip()) + "\n@enduml"
    if not actions:
        actions.append("no_supported_repair_action")
    return repaired, actions
