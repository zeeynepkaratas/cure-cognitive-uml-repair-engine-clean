# PURE-Derived LLM Repair Pilot

This preliminary pilot does not replace the shared S01-S50 benchmark.
It uses selected PURE requirement excerpts, curated reference UML models, and controlled injected PlantUML defects.

## Summary

- Total cases: 10
- Project-defined fallback repairs: 9/10
- Project-defined fallback success rate: 90.0%
- Project-defined Wilson 95% CI: 59.6%-98.2%
- PlantUML runtime available: True
- PlantUML-validated repairs: 9
- Mean class F1 against reference UML: 0.864
- Mean relationship F1 against reference UML: 0.914
- Relationship metric: source-target endpoint-pair F1; relation type, multiplicity, and labels are not scored.
- Agent terminal-state valid: 2
- Final-valid and agent-terminal-valid: 1
- Final-valid but agent-terminal-invalid: 8

## Execution Metadata

- Commit SHA: `f2689cc2407c0d6f17eaee272f93cd233063cfc7`
- Generated at UTC: `2026-07-30T07:10:28.705701+00:00`
- Python: `3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)]`
- Platform: `Windows-11-10.0.26200-SP0`
- Model: `gpt-4o-mini`
- Temperature: `0.0`
- Max iterations: `3`

Success is defined by the endpoint's final syntax/OCL validation. The
`agent_is_valid` field is a secondary LangGraph terminal-state diagnostic
from the internal Critic-Healer loop and should not be interpreted as the
primary repair-success criterion.
Because the Critic receives a strict prompt and fixed curated OCL-rule
retrieval context, this field may reflect retrieval-rule mismatch or
over-strict Critic behavior rather than independent semantic correctness.

## Case Results

| Case | PURE row | Category | Project-defined success | PlantUML-validated success | Class F1 | Relationship F1 | LLM calls |
|---|---:|---|---:|---:|---:|---:|---:|
| P01 | 30 | missing_startuml | True | True | 1.0 | 1.0 | 7 |
| P02 | 31 | missing_enduml | True | True | 1.0 | 1.0 | 7 |
| P03 | 33 | duplicate_class | True | True | 0.8 | 0.857 | 7 |
| P04 | 37 | missing_both_boundaries | False | False | 0.8 | 1.0 | 7 |
| P05 | 42 | missing_enduml | True | True | 0.8 | 0.857 | 7 |
| P06 | 49 | duplicate_class_missing_start | True | True | 0.833 | 0.8 | 7 |
| P07 | 51 | missing_startuml | True | True | 0.8 | 1.0 | 7 |
| P08 | 59 | duplicate_class | True | True | 0.833 | 0.909 | 7 |
| P09 | 64 | missing_both_boundaries | True | True | 0.889 | 0.857 | 7 |
| P10 | 106 | missing_enduml | True | True | 0.889 | 0.857 | 7 |
