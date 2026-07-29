"""Structured Critic decision parsing helpers."""

from __future__ import annotations

import json
import re
from typing import Any


CRITIC_DECISION_SCHEMA = {
    "title": "CriticDecision",
    "description": "Structured UML validation decision from the Critic agent.",
    "type": "object",
    "properties": {
        "is_valid": {"type": "boolean"},
        "errors": {"type": "array", "items": {"type": "string"}},
        "categories": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["is_valid", "errors", "categories"],
}


def parse_critic_decision(response: Any) -> dict:
    if isinstance(response, dict):
        return {
            "is_valid": bool(response.get("is_valid")),
            "errors": list(response.get("errors") or []),
            "categories": list(response.get("categories") or []),
        }

    content = getattr(response, "content", response)
    text = str(content).strip()
    if re.fullmatch(r"GECERLI\.?", text, flags=re.IGNORECASE):
        return {"is_valid": True, "errors": [], "categories": []}

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            errors = parsed.get("errors") or parsed.get("hatalar") or []
            categories = parsed.get("categories") or parsed.get("kategori") or []
            explicit_valid = parsed.get("is_valid")
            return {
                "is_valid": bool(explicit_valid) if explicit_valid is not None else not bool(errors),
                "errors": list(errors),
                "categories": list(categories),
            }
    except json.JSONDecodeError:
        pass

    return {"is_valid": False, "errors": [text], "categories": ["unstructured"]}
