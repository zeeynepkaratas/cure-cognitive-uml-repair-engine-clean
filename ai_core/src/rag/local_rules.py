"""Cached deterministic lexical retrieval; no embedding API calls."""

import json
from functools import lru_cache
from pathlib import Path
import re


@lru_cache(maxsize=1)
def rule_catalogue():
    return json.loads(
        (Path(__file__).resolve().parents[2] / "rules/catalogue.json").read_text(encoding="utf-8")
    )


class LocalRuleRetriever:
    backend = "cached_lexical"

    def retrieve(self, srs: str, diagram: str, legacy: bool = False, top_k: int = 2, threshold: float = 0.01):
        query = set(re.findall(r"\w+", (srs + " " + diagram).lower()))
        results = []
        for rule in rule_catalogue():
            if legacy and not rule["domain_example"]:
                continue
            if not legacy and rule["domain_example"]:
                if not all(name.lower() in query for name in rule["entities"]):
                    continue
                if not all(term.lower() in srs.lower() for term in rule.get("required_terms", [])):
                    continue
            words = set(re.findall(r"\w+", rule["text"].lower()))
            score = len(query & words) / max(1, len(query | words))
            if legacy or score >= threshold:
                results.append({**rule, "score": score})
        return sorted(results, key=lambda r: (-r["score"], r["id"]))[: top_k if legacy else 9]
