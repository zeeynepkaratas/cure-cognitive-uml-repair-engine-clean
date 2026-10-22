"""Seeded semantic changes applied without consulting repair outputs."""

import random
import re
from backend.src.utils.plantuml_parser import parse_model

DISTRACTORS = ("WeatherStation", "MusicPlaylist", "Spacecraft", "RecipeBook")


def inject(code: str, defect_id: str, seed: int) -> tuple[str, dict]:
    rng = random.Random(seed)
    model = parse_model(code)
    names = [d.name for d in model.declarations]
    selected = rng.choice(model.declarations)
    edges = model.relationships
    detail = {"defect_id": defect_id, "seed": seed, "selected_class": selected.name}
    if defect_id == "D1":
        code = code[: selected.start] + code[selected.end :]
        code = "\n".join(
            line
            for line in code.splitlines()
            if not (
                re.match(r"^\s*" + re.escape(selected.name) + r'\s+["<*.o-]', line)
                or re.search(r'[>.o*-]\s*(?:"[^"]*"\s*)?' + re.escape(selected.name) + r"\b", line)
            )
        )
    elif defect_id == "D2":
        extra = rng.choice([n for n in DISTRACTORS if n not in names])
        code = code.replace("@enduml", f"class {extra} {{}}\n@enduml")
        detail["added_class"] = extra
    elif defect_id in {"D3", "D4", "D5", "D6"}:
        lines = code.splitlines()
        candidates = [
            i for i, line in enumerate(lines) if parse_model("@startuml\n" + line + "\n@enduml").relationships
        ]
        i = rng.choice(candidates)
        relation = parse_model("@startuml\n" + lines[i] + "\n@enduml").relationships[0]
        detail["original_relation"] = list(relation)
        if defect_id == "D3":
            lines.pop(i)
        elif defect_id == "D4":
            target = rng.choice([n for n in names if n not in {relation.src, relation.tgt}])
            lines[i] = re.sub(r"\b" + re.escape(relation.tgt) + r"\b", target, lines[i])
        elif defect_id == "D5":
            lines[i] = re.sub(r"\b" + re.escape(relation.src) + r"\b", "__SWAP__", lines[i])
            lines[i] = re.sub(r"\b" + re.escape(relation.tgt) + r"\b", relation.src, lines[i]).replace(
                "__SWAP__", relation.tgt
            )
        else:
            lines[i] = re.sub(
                r"\*--|o--|-->|\.\.>|--\|>", "--|>" if relation.type != "inheritance" else "-->", lines[i]
            )
        code = "\n".join(lines)
    elif defect_id == "D7":
        code = re.sub(r"\b" + re.escape(selected.name) + r"\b", "UnspecifiedEntity", code)
    elif defect_id == "D8":
        code = code.replace("  +id: String\n", "", 1)
    elif defect_id == "D9":
        code = code.replace("@enduml", f"class {selected.name} {{}}\n@enduml")
    elif defect_id == "D10":
        code = code.replace("@enduml", "")
    else:
        raise ValueError("Unknown defect operator: " + defect_id)
    if not edges or code == model:
        raise ValueError("Unsupported source model")
    return code, detail
