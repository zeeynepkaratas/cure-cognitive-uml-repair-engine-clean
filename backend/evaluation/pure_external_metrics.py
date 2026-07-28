"""Graph-level metrics for PURE-derived external repair pilot cases."""

from __future__ import annotations

from pathlib import Path
import sys


BACKEND_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = BACKEND_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from evaluators.semantic_eval import extract_uml_entities, hesapla_f1  # noqa: E402


def compare_to_reference(reference_plantuml: str, repaired_plantuml: str) -> dict:
    reference = extract_uml_entities(reference_plantuml)
    repaired = extract_uml_entities(repaired_plantuml)
    class_metrics = hesapla_f1(repaired["siniflar"], reference["siniflar"])
    relationship_metrics = hesapla_f1(repaired["iliskiler"], reference["iliskiler"])

    ref_classes = {item.lower(): item for item in reference["siniflar"]}
    rep_classes = {item.lower(): item for item in repaired["siniflar"]}
    ref_relationships = {_norm_pair(item): item for item in reference["iliskiler"]}
    rep_relationships = {_norm_pair(item): item for item in repaired["iliskiler"]}

    missing_classes = sorted(ref_classes[key] for key in ref_classes.keys() - rep_classes.keys())
    extra_classes = sorted(rep_classes[key] for key in rep_classes.keys() - ref_classes.keys())
    missing_relationships = sorted(ref_relationships[key] for key in ref_relationships.keys() - rep_relationships.keys())
    extra_relationships = sorted(rep_relationships[key] for key in rep_relationships.keys() - ref_relationships.keys())

    return {
        "reference_class_count": len(reference["siniflar"]),
        "repaired_class_count": len(repaired["siniflar"]),
        "reference_relationship_count": len(reference["iliskiler"]),
        "repaired_relationship_count": len(repaired["iliskiler"]),
        "class_precision": class_metrics["precision"],
        "class_recall": class_metrics["recall"],
        "class_f1": class_metrics["f1"],
        "relationship_precision": relationship_metrics["precision"],
        "relationship_recall": relationship_metrics["recall"],
        "relationship_f1": relationship_metrics["f1"],
        "missing_classes": missing_classes,
        "extra_classes": extra_classes,
        "missing_relationships": missing_relationships,
        "extra_relationships": extra_relationships,
    }


def _norm_pair(pair: tuple[str, str]) -> str:
    return "->".join(part.lower() for part in pair)
