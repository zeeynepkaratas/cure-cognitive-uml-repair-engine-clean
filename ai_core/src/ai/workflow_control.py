"""Dependency-free workflow routing helpers."""

from __future__ import annotations


def route_repair_decision(is_valid: bool, repair_attempt_count: int, max_iterations: int) -> str:
    if is_valid:
        return "end"
    if repair_attempt_count >= max_iterations:
        return "end"
    return "continue"
