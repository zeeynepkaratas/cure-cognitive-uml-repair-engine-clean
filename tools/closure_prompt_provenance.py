"""Independently reconstruct every first prompt without importing agent code."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    rows = json.loads((ROOT / "backend/evaluation/results_v4/test-frozen-20261022/results.json").read_text(encoding="utf-8"))
    catalogue = {r["id"]: r for r in json.loads((ROOT / "ai_core/rules/catalogue.json").read_text(encoding="utf-8"))}
    checked, errors = 0, []
    for row in rows:
        if not row["trace"]:
            continue
        trace = row["trace"][0]
        legacy = row["condition"] in {"C5", "C6"}
        role = trace["role"]
        filename = f"legacy/{role}_prompt.txt" if legacy else f"v4.1/{role}.txt"
        rules = [catalogue[r] for r in trace["retrieved_rule_ids"]]
        feedback = json.dumps(row["input_validation"], ensure_ascii=False) if row["condition"] in {"C4", "C7"} else "Not provided in this condition."
        template = (ROOT / "ai_core/prompts" / filename).read_text(encoding="utf-8")
        prompt = template.format(
            original_text=row["srs"] if role == "critic" or not legacy else "",
            current_uml=row["input_plantuml"], errors=json.dumps([], ensure_ascii=legacy), feedback=feedback,
            ocl_rules="\n".join("- " + (r.get("legacy_text", r["text"]) if legacy else r["text"]) for r in rules),
        )
        checked += 1
        if hashlib.sha256(prompt.encode()).hexdigest() != trace["prompt_hash"]:
            errors.append([row["condition"], row["case_id"], row["rep"]])
    report = {"first_request_prompts_checked": checked, "matching_hashes": checked-len(errors), "mismatches": errors,
              "scope": "Initial prompts only, independently reconstructed from templates/raw initial validation and rule IDs. Full intermediate SDK request bodies are not retained; prompt hashes cannot reveal every request field or verify provider seed handling."}
    (ROOT / "docs/closure_audit/PROMPT_PROVENANCE.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report))
    if errors or checked != 2500:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
