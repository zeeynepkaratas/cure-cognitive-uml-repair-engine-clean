"""Versioned structural agreement heuristic; not semantic correctness."""
from __future__ import annotations

import re
from typing import Protocol

from backend.src.utils.entity_rules import STOP_WORDS
from backend.src.utils.plantuml_parser import parse_classes, parse_relationships
from .semantic_eval_legacy import hesapla_f1, calculate_semantic_fidelity as calculate_semantic_fidelity_legacy


class EntityExtractor(Protocol):
    def __call__(self, text: str) -> dict: ...


def extract_uml_entities(plantuml_kodu: str, legacy: bool = False) -> dict:
    return {"siniflar": parse_classes(plantuml_kodu, legacy=legacy),
            "iliskiler": parse_relationships(plantuml_kodu, legacy=legacy)}


def extract_srs_entities(srs_metni: str) -> dict:
    """Explicit proper-name heuristic. It cannot recover arbitrary domain concepts."""
    names = {x for x in re.findall(r"\b[A-Z][A-Za-z0-9_]*\b", srs_metni)
             if x.lower() not in STOP_WORDS and len(x) > 1}
    by_name = {x.lower(): x for x in names}
    edges = set()
    pattern = r"\b(\w+)\s+(?:uses?|contains?|manages?|creates?|extends?|calls?|connects?\s+to)\s+(?:the\s+)?(\w+)"
    for source, target in re.findall(pattern, srs_metni, re.I):
        if source.lower() in by_name and target.lower() in by_name:
            edges.add((by_name[source.lower()], by_name[target.lower()]))
    return {"siniflar": names, "iliskiler": edges}


class GoldModelExtractor:
    def __init__(self, plantuml: str):
        self.entities = extract_uml_entities(plantuml)

    def __call__(self, text: str) -> dict:
        return self.entities


def calculate_semantic_fidelity(srs_metni: str, plantuml_kodu: str,
                               entity_extractor: EntityExtractor | None = None,
                               legacy: bool = False) -> dict:
    """Structural agreement proxy v2, not a semantic-correctness measurement.

    Let S/U be case-folded source/diagram class sets; M=S-U, H=U-S.
    C=1-|M|/|S|, K=1-|H|/|U| (K=1 when U is empty).
    Base weights: class F1 .35, directed endpoint F1 .25, C .25, K .15.
    If source relations are empty, omit relationship F1 and divide the other
    weighted terms by .75. If S is empty, return score=None/not_applicable.
    Names are case-folded before set construction and denominators count those
    unique names. Full precision is retained until the displayed score.
    """
    if legacy:
        return calculate_semantic_fidelity_legacy(srs_metni, plantuml_kodu)
    source = (entity_extractor or extract_srs_entities)(srs_metni)
    diagram = extract_uml_entities(plantuml_kodu)
    source_names = {x.lower(): x for x in source['siniflar']}
    diagram_names = {x.lower(): x for x in diagram['siniflar']}
    missing = sorted(source_names[x] for x in source_names.keys()-diagram_names.keys())
    extra = sorted(diagram_names[x] for x in diagram_names.keys()-source_names.keys())
    common = dict(missing_classes=missing, extra_classes=extra, eksik_siniflar=missing,
                  halusinasyonlar=extra, metric_version='structural_proxy_v2')
    if not source_names:
        return dict(common, score=None, status='not_applicable', genel_skor=None,
                    yuzde='N/A', gecti_mi=None, ieee_kriterleri={})
    s,u = set(source_names),set(diagram_names)
    p,r = (len(s & u)/len(u) if u else 0),len(s & u)/len(s)
    class_f1 = 2*p*r/(p+r) if p+r else 0
    sr = {tuple(x.lower() for x in edge) for edge in source['iliskiler']}
    ur = {tuple(x.lower() for x in edge) for edge in diagram['iliskiler']}
    p,r = (len(sr & ur)/len(ur) if ur else 0),(len(sr & ur)/len(sr) if sr else 0)
    rel_f1 = 2*p*r/(p+r) if p+r else 0
    completeness = 1-len(s-u)/len(s)
    consistency = 1-len(u-s)/len(u) if u else 1
    weights = {'class_f1':.35,'relationship_f1':.25 if sr else 0,'completeness':.25,'consistency':.15}
    components = dict(class_f1=class_f1,relationship_f1=rel_f1 if sr else None,
                      completeness=completeness,consistency=consistency)
    total = sum(weights.values())
    score = sum(weights[k]*(components[k] or 0) for k in weights)/total
    return dict(common, score=score, status='applicable', genel_skor=round(score,3),
                yuzde=f'{score*100:.1f}%', gecti_mi=score>=.75,
                components=components, effective_weights={k:v/total for k,v in weights.items()},
                ieee_kriterleri=components)
