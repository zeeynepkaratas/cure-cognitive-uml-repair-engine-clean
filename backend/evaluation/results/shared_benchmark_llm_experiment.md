# Shared Benchmark LLM Repair Experiment

This report evaluates the real LLM-based /api/autonomous-repair endpoint
on the shared S01-S50 invalid PlantUML benchmark.

## Summary

- Total cases: 50
- Project-defined fallback repairs: 49/50
- Project-defined fallback success rate: 98.0%
- Project-defined Wilson 95% CI: 89.5% - 99.6%
- PlantUML runtime available: True
- PlantUML-validated repairs: 40
- Agent terminal-state valid: 4
- Final-valid and agent-terminal-valid: 3
- Final-valid but agent-terminal-invalid: 46
- Model: gpt-4o-mini
- Max iterations: 3

## Execution Metadata

- Commit SHA: `f2689cc2407c0d6f17eaee272f93cd233063cfc7`
- Generated at UTC: `2026-07-30T07:05:25.120606+00:00`
- Python: `3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)]`
- Platform: `Windows-11-10.0.26200-SP0`
- Model: `gpt-4o-mini`
- Temperature: `0.0`
- Max iterations: `3`

Project-defined fallback success must not be reported as a real PlantUML-runtime-validated success rate.

Success is defined by the endpoint's final syntax/OCL validation. The
`agent_is_valid` field is a secondary LangGraph terminal-state diagnostic
from the internal Critic-Healer loop and should not be interpreted as the
primary repair-success criterion.
Because the Critic receives a strict prompt and fixed curated OCL-rule
retrieval context, this field may reflect retrieval-rule mismatch or
over-strict Critic behavior rather than independent semantic correctness.

## Case Results

| Case | Category | Project-defined success | PlantUML-validated success | Time (s) | Repair attempts | LLM calls |
|---|---|---:|---:|---:|---:|---:|
| S01 | missing_startuml | True | True | 24.452 | 3 | 7 |
| S02 | missing_enduml | True | True | 17.891 | 3 | 7 |
| S03 | missing_both_boundaries | True | True | 17.044 | 3 | 7 |
| S04 | empty_diagram | True | False | 17.306 | 3 | 7 |
| S05 | plain_empty_input | True | False | 18.256 | 3 | 7 |
| S06 | missing_startuml_with_relation | True | True | 16.264 | 3 | 7 |
| S07 | missing_enduml_with_relation | True | True | 17.338 | 3 | 7 |
| S08 | missing_both_with_relation | True | True | 18.63 | 3 | 7 |
| S09 | only_start_token | True | False | 13.416 | 1 | 3 |
| S10 | only_end_token | True | False | 17.71 | 3 | 7 |
| S11 | comment_only | True | True | 16.89 | 3 | 7 |
| S12 | whitespace_empty | True | True | 17.76 | 3 | 7 |
| S13 | no_class_relation_with_tags | True | True | 16.238 | 3 | 7 |
| S14 | missing_start_no_class | True | False | 16.638 | 3 | 7 |
| S15 | missing_end_no_class | True | True | 21.251 | 3 | 7 |
| S16 | duplicate_class | True | True | 16.629 | 3 | 7 |
| S17 | duplicate_class_missing_start | True | False | 19.043 | 3 | 7 |
| S18 | duplicate_class_missing_end | True | True | 16.029 | 3 | 7 |
| S19 | duplicate_lowercase | True | True | 16.228 | 3 | 7 |
| S20 | duplicate_with_relation | True | True | 16.421 | 3 | 7 |
| S21 | unbalanced_brace | True | True | 14.322 | 3 | 7 |
| S22 | extra_closing_brace | True | True | 14.796 | 3 | 7 |
| S23 | missing_boundary_and_unbalanced_brace | True | False | 9.533 | 1 | 3 |
| S24 | missing_end_lowercase_class | True | True | 16.846 | 3 | 7 |
| S25 | missing_start_lowercase_class | True | True | 15.57 | 3 | 7 |
| S26 | missing_start_isolated_classes | True | True | 14.773 | 3 | 7 |
| S27 | missing_end_isolated_classes | True | True | 17.253 | 3 | 7 |
| S28 | missing_end_cyclic_dependency | True | True | 14.263 | 3 | 7 |
| S29 | missing_start_cycle | True | True | 14.646 | 3 | 7 |
| S30 | missing_start_god_class_warning | True | True | 18.9 | 3 | 7 |
| S31 | missing_both_god_class_warning | True | True | 17.074 | 3 | 7 |
| S32 | missing_start_truncated_relation_target | True | True | 15.038 | 3 | 7 |
| S33 | missing_end_truncated_relation_source | True | True | 14.207 | 3 | 7 |
| S34 | missing_end_truncated_relation | True | True | 16.642 | 3 | 7 |
| S35 | duplicate_and_unbalanced_brace | True | True | 16.969 | 3 | 7 |
| S36 | duplicate_three_times | True | True | 16.53 | 3 | 7 |
| S37 | duplicate_interface_like_class | True | True | 20.234 | 3 | 7 |
| S38 | only_notes | True | True | 17.671 | 3 | 7 |
| S39 | missing_both_only_notes | True | True | 17.158 | 3 | 7 |
| S40 | duplicate_with_missing_both | True | True | 15.905 | 3 | 7 |
| S41 | mixed_missing_start_duplicate_relation | True | False | 16.558 | 3 | 7 |
| S42 | mixed_missing_end_duplicate_relation | True | True | 19.398 | 3 | 7 |
| S43 | missing_end_self_relation | False | False | 4.633 | 0 | 1 |
| S44 | missing_start_self_relation | True | True | 15.075 | 3 | 7 |
| S45 | class_keyword_without_name | True | True | 18.344 | 3 | 7 |
| S46 | missing_end_class_keyword_without_name | True | True | 16.939 | 3 | 7 |
| S47 | invalid_lowercase_duplicate_relation | True | True | 15.692 | 3 | 7 |
| S48 | duplicate_and_cycle | True | True | 16.776 | 3 | 7 |
| S49 | missing_both_duplicate_and_cycle | True | True | 17.289 | 3 | 7 |
| S50 | complex_mixed_defect | True | False | 16.87 | 3 | 7 |
