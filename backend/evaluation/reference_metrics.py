"""Versioned gold-model set metrics. These are structural, not behavioural correctness."""

from __future__ import annotations
import re
import statistics
from backend.src.utils.plantuml_parser import parse_model

METRIC_VERSION = "gold-structural-v2"


def normalise_name(name: str) -> str:
    """Split CamelCase/acronyms, strip punctuation, casefold, singularise final token.

    Conservative English suffix rules: ies->y, sses->ss, trailing s except ss/us/is.
    status, news and series are protected. No synonym matching or general stemming.
    Collisions are reported separately; a set metric must not hide duplicate classes.
    """
    spaced = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", name)
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", spaced)
    words = re.findall(r"[a-z0-9]+", spaced.casefold())
    if not words:
        return ""
    word = words[-1]
    if word not in {"status", "news", "series"}:
        if word.endswith("ies") and len(word) > 4:
            word = word[:-3] + "y"
        elif word.endswith("sses"):
            word = word[:-2]
        elif word.endswith("s") and len(word) > 3 and not word.endswith(("ss", "us", "is")):
            word = word[:-1]
    words[-1] = word
    return "".join(words)


def prf(reference: set, predicted: set) -> dict:
    overlap = len(reference & predicted)
    precision = overlap / len(predicted) if predicted else float(not reference)
    recall = overlap / len(reference) if reference else float(not predicted)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "reference_count": len(reference),
        "predicted_count": len(predicted),
        "missing": sorted(reference - predicted),
        "spurious": sorted(predicted - reference),
    }


def model_elements(code: str) -> dict:
    model = parse_model(code)
    names = [normalise_name(c.name) for c in model.declarations]
    directed = {(normalise_name(r.src), normalise_name(r.tgt)) for r in model.relationships}
    undirected = {tuple(sorted(pair)) for pair in directed}
    typed = {(normalise_name(r.src), normalise_name(r.tgt), r.type) for r in model.relationships}
    strict = {
        (normalise_name(r.src), normalise_name(r.tgt), r.type, r.src_mult, r.tgt_mult)
        for r in model.relationships
    }
    attrs = set()
    for declaration in model.declarations:
        for attribute in declaration.attributes:
            match = re.match(r"^[+\-#~]?\s*([A-Za-z_]\w*)", attribute)
            if match:
                attrs.add((normalise_name(declaration.name), normalise_name(match[1])))
    return {
        "class": set(names),
        "rel_undirected": undirected,
        "rel_directed": directed,
        "rel_typed": typed,
        "rel_multiplicity": strict,
        "attribute": attrs,
        "duplicate_normalised_names": len(names) - len(set(names)),
        "declaration_count": len(model.declarations),
        "relationship_count": len(model.relationships),
    }


def reference_metrics(reference: str, predicted: str, original: str | None = None) -> dict:
    gold, output = model_elements(reference), model_elements(predicted)
    result = {
        "metric_version": METRIC_VERSION,
        "reference_class_count": gold["declaration_count"],
        "reference_relationship_count": gold["relationship_count"],
        "output_class_count": output["declaration_count"],
        "output_relationship_count": output["relationship_count"],
        "normalisation_collisions_or_duplicates": output["duplicate_normalised_names"],
    }
    before = model_elements(original) if original is not None else None
    for name in ("class", "rel_undirected", "rel_directed", "rel_typed", "rel_multiplicity", "attribute"):
        metric = prf(gold[name], output[name])
        if name == "attribute" and not gold[name]:
            metric.update(f1=None, precision=None, recall=None, status="not_applicable")
        result["reference_" + name] = metric
        if before is not None and metric["f1"] is not None:
            result["delta_" + name + "_f1"] = metric["f1"] - prf(gold[name], before[name])["f1"]
    return result


def describe(values) -> dict:
    values = [v for v in values if v is not None]
    return {
        "n": len(values),
        "mean": statistics.mean(values) if values else None,
        "sd": statistics.stdev(values) if len(values) > 1 else (0.0 if values else None),
        "median": statistics.median(values) if values else None,
        "min": min(values) if values else None,
        "max": max(values) if values else None,
    }


def macro(rows: list[dict], field: str) -> dict:
    """Rows contain metrics and explicit compiler_valid; never exclude failures silently."""
    return {
        label: describe(row["metrics"][field]["f1"] for row in subset)
        for label, subset in [
            ("all_outputs", rows),
            ("compiling_outputs", [r for r in rows if r["compiler_valid"] is True]),
        ]
    }
