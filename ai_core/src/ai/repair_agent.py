"""Configurable, instrumented repair conditions with injectable model clients."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import logging
import os
import re
from pathlib import Path
import time
from typing import Literal

from backend.src.repair.validation import check_diagram
from .plantuml_normalizer import normalize_plantuml_text
from ai_core.src.rag.local_rules import LocalRuleRetriever

logger = logging.getLogger(__name__)
PROMPTS = Path(__file__).resolve().parents[2] / "prompts"
MODES = {
    "legacy_critic_healer",
    "critic_healer_norules",
    "healer_only_compiler_feedback",
    "single_pass",
    "improved_critic_healer",
}


@dataclass(frozen=True)
class RepairConfig:
    mode: Literal[
        "legacy_critic_healer",
        "critic_healer_norules",
        "healer_only_compiler_feedback",
        "single_pass",
        "improved_critic_healer",
    ] = "improved_critic_healer"
    use_rules: bool = True
    compiler_feedback: bool = True
    healer_sees_srs: bool = True
    max_iterations: int = 3
    model_critic: str = "gpt-4o-mini-2024-07-18"
    model_healer: str = "gpt-4o-mini-2024-07-18"
    temperature: float = 0
    seed: int | None = 1729
    timeout_s: float = 45
    max_retries: int = 2
    max_tokens: int = 2048

    def __post_init__(self):
        if (
            self.mode not in MODES
            or self.max_iterations < 1
            or self.max_tokens < 1
            or self.timeout_s <= 0
            or self.max_retries < 0
        ):
            raise ValueError("Invalid repair configuration")


class OpenAIModelClient:
    """Lazy SDK boundary. Retries are performed by the agent so every attempt is counted."""

    def invoke(self, role: str, prompt: str, config: RepairConfig):
        from openai import OpenAI
        from .critic_decision import CRITIC_DECISION_SCHEMA

        client = OpenAI(timeout=config.timeout_s, max_retries=0)
        arguments = dict(
            model=config.model_critic if role == "critic" else config.model_healer,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.temperature,
            max_completion_tokens=config.max_tokens,
        )
        if config.seed is not None:
            arguments["seed"] = config.seed
        if role == "critic":
            schema = {**CRITIC_DECISION_SCHEMA, "additionalProperties": False}
            arguments["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": "critic_decision", "strict": True, "schema": schema},
            }
        response = client.chat.completions.create(**arguments)
        return {
            "content": response.choices[0].message.content or "",
            "model_name": response.model,
            "system_fingerprint": getattr(response, "system_fingerprint", None),
            "request_id": getattr(response, "_request_id", None),
            "tokens_in": response.usage.prompt_tokens if response.usage else None,
            "tokens_out": response.usage.completion_tokens if response.usage else None,
        }


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def safe_error_text(error):
    text = str(error)
    key = os.getenv("OPENAI_API_KEY")
    if key:
        text = text.replace(key, "<REDACTED_API_KEY>")
    return re.sub(r"sk-[^\s\"']+", "<REDACTED_API_KEY>", text)


class UMLRepairAgent:
    def __init__(
        self,
        config: RepairConfig | None = None,
        client=None,
        validator=None,
        retriever=None,
        before_call=None,
    ):
        self.config = config or RepairConfig()
        self.client = client or OpenAIModelClient()
        self.validator = validator or check_diagram
        self.retriever = retriever or LocalRuleRetriever()
        self.before_call = before_call
        self.llm_call_count = 0
        self.last_final_state = None

    def _prompt(self, role, srs, diagram, errors, validation, rules):
        legacy = self.config.mode in {"legacy_critic_healer", "critic_healer_norules"}
        filename = ("legacy/" + role + "_prompt.txt") if legacy else ("v4/" + role + ".txt")
        template = (PROMPTS / filename).read_text(encoding="utf-8")
        feedback = (
            json.dumps(validation, ensure_ascii=False)
            if self.config.compiler_feedback and not legacy
            else "Not provided in this condition."
        )
        return template.format(
            original_text=srs if role == "critic" or self.config.healer_sees_srs else "",
            current_uml=diagram,
            errors=json.dumps(errors, ensure_ascii=legacy),
            feedback=feedback,
            ocl_rules="\n".join(
                "- " + r.get("legacy_text", r["text"]) if legacy else "- " + r["text"] for r in rules
            ),
        )

    def _call(self, role, prompt, iteration, diagram, validation, rules, trace):
        for attempt in range(self.config.max_retries + 1):
            if self.before_call:
                self.before_call(role, prompt, self.config)
            started = time.perf_counter()
            self.llm_call_count += 1
            item = {
                "iteration": iteration,
                "role": role,
                "attempt": attempt + 1,
                "prompt_hash": digest(prompt),
                "tokens_in": None,
                "tokens_out": None,
                "latency_s": None,
                "diagram_hash": digest(diagram),
                "project_valid": validation["project_valid"],
                "compiler_valid": validation["compiler_valid"],
                "compiler_errors": validation.get("compiler_errors", []),
                "critic_valid": None,
                "retrieved_rule_ids": [r["id"] for r in rules],
                "retrieved_rules": [{"id": r["id"], "score": r["score"]} for r in rules],
            }
            try:
                response = self.client.invoke(role, prompt, self.config)
                item.update(
                    {
                        key: response.get(key)
                        for key in [
                            "tokens_in",
                            "tokens_out",
                            "model_name",
                            "system_fingerprint",
                            "request_id",
                        ]
                    }
                )
                item["latency_s"] = time.perf_counter() - started
                item["response_text"] = response["content"]
                trace.append(item)
                return response["content"], item
            except Exception as exc:
                item.update(
                    error_type=type(exc).__name__,
                    error=safe_error_text(exc),
                    latency_s=time.perf_counter() - started,
                )
                trace.append(item)
                if attempt == self.config.max_retries or getattr(exc, "status_code", None) in {
                    400,
                    401,
                    403,
                    404,
                }:
                    raise
                time.sleep(min(2**attempt, 4))

    def run(
        self, original_text: str, initial_uml: str, return_state: bool = False, force_repair: bool = False
    ):
        self.llm_call_count = 0
        config = self.config
        legacy = config.mode in {"legacy_critic_healer", "critic_healer_norules"}
        diagram = initial_uml
        initial = self.validator(diagram)
        validation = initial
        trace = []
        errors = []
        repairs = 0
        critic = None
        state = {
            "agent_status": "ok",
            "agent_error": None,
            "terminated_by": "budget_exhausted",
            "first_compiler_valid_iteration": 0 if initial["compiler_valid"] is True else None,
            "first_project_valid_iteration": 0 if initial["project_valid"] else None,
        }
        needs_repair = not initial["project_valid"] or initial["compiler_valid"] is False
        if force_repair or needs_repair:
            try:
                while True:
                    rules = []
                    if config.mode not in {"single_pass", "healer_only_compiler_feedback"}:
                        if config.use_rules and config.mode != "critic_healer_norules":
                            rules = self.retriever.retrieve(
                                "" if legacy else original_text, diagram, legacy=legacy
                            )
                        prompt = self._prompt("critic", original_text, diagram, errors, validation, rules)
                        raw, item = self._call("critic", prompt, repairs, diagram, validation, rules, trace)
                        decision = json.loads(raw) if isinstance(raw, str) else raw
                        if (
                            not isinstance(decision, dict)
                            or type(decision.get("is_valid")) is not bool
                            or not isinstance(decision.get("errors"), list)
                            or not all(isinstance(e, str) for e in decision["errors"])
                        ):
                            raise ValueError("Invalid structured Critic decision")
                        critic = decision["is_valid"]
                        errors = decision["errors"]
                        item["critic_valid"] = critic
                        item["critic_errors"] = list(errors)
                        item["critic_categories"] = decision.get("categories", [])
                        accepted = critic and (
                            legacy or (validation["project_valid"] and validation["compiler_valid"] is True)
                        )
                        if accepted:
                            state["terminated_by"] = "accepted"
                            break
                    maximum = 1 if config.mode == "single_pass" else config.max_iterations
                    if repairs >= maximum:
                        break
                    prompt = self._prompt("healer", original_text, diagram, errors, validation, [])
                    raw, item = self._call("healer", prompt, repairs + 1, diagram, validation, [], trace)
                    if not isinstance(raw, str) or not raw.strip():
                        raise ValueError("Empty/non-text Healer output")
                    diagram = normalize_plantuml_text(raw)
                    item["output_plantuml"] = diagram
                    repairs += 1
                    validation = self.validator(diagram)
                    item.update(
                        diagram_hash=digest(diagram),
                        project_valid=validation["project_valid"],
                        compiler_valid=validation["compiler_valid"],
                        compiler_errors=validation.get("compiler_errors", []),
                    )
                    for field, valid in [
                        ("first_compiler_valid_iteration", validation["compiler_valid"] is True),
                        ("first_project_valid_iteration", validation["project_valid"]),
                    ]:
                        if valid and state[field] is None:
                            state[field] = repairs
                    if (
                        config.mode in {"single_pass", "healer_only_compiler_feedback"}
                        and validation["project_valid"]
                        and validation["compiler_valid"] is True
                    ):
                        state["terminated_by"] = "accepted"
                        break
                    if config.mode == "single_pass":
                        break
            except (ValueError, json.JSONDecodeError) as exc:
                state.update(
                    agent_status="parse_error", agent_error=safe_error_text(exc), terminated_by="error"
                )
            except Exception as exc:
                if getattr(exc, "budget_exceeded", False):
                    state.update(
                        budget_stopped=True,
                        agent_error=safe_error_text(exc),
                        terminated_by="budget_exhausted",
                    )
                    status = "ok"
                else:
                    status = "timeout" if "timeout" in type(exc).__name__.lower() else "api_error"
                    state.update(
                        provider_status_code=getattr(exc, "status_code", None),
                        agent_status=status,
                        agent_error=type(exc).__name__ + ": " + safe_error_text(exc),
                        terminated_by="error",
                    )
        else:
            state["terminated_by"] = "accepted"
        regression = initial["compiler_valid"] is True and validation["compiler_valid"] is False
        state.update(
            current_uml=diagram,
            repair_attempt_count=repairs,
            is_valid=critic,
            critic_valid=critic,
            final_critic_errors=list(errors),
            project_valid=validation["project_valid"],
            compiler_valid=validation["compiler_valid"],
            regression=regression,
            safe_plantuml=initial_uml if regression else diagram,
            trace=trace,
            llm_call_count=self.llm_call_count,
            initial_validation=initial,
            final_validation=validation,
            retrieval_backend=self.retriever.backend,
            tokens_in=sum(t["tokens_in"] for t in trace)
            if all(t["tokens_in"] is not None for t in trace)
            else None,
            tokens_out=sum(t["tokens_out"] for t in trace)
            if all(t["tokens_out"] is not None for t in trace)
            else None,
            usage_complete=all(t["tokens_in"] is not None and t["tokens_out"] is not None for t in trace),
        )
        self.last_final_state = state
        return state if return_state else diagram
