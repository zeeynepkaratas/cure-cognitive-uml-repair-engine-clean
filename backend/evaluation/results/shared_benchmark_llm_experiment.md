# Shared Benchmark LLM Repair Experiment

This report evaluates the real LLM-based /api/autonomous-repair endpoint
on the shared S01-S50 invalid PlantUML benchmark.

## Summary

- Total cases: 50
- Successful repairs: 47
- Failed repairs: 3
- Success rate: 94.0%
- Wilson 95% CI: 83.8% - 97.9%
- Model: gpt-4o-mini
- Max iterations: 3

## Case Results

| Case | Category | Success | Time (s) | Repair attempts | LLM calls |
|---|---|---:|---:|---:|---:|
| S01 | missing_startuml | True | 10.479 | 3 | 7 |
| S02 | missing_enduml | True | 9.674 | 3 | 7 |
| S03 | missing_both_boundaries | True | 8.276 | 3 | 7 |
| S04 | empty_diagram | True | 10.752 | 3 | 7 |
| S05 | plain_empty_input | True | 10.057 | 3 | 7 |
| S06 | missing_startuml_with_relation | True | 2.967 | 1 | 3 |
| S07 | missing_enduml_with_relation | True | 6.437 | 3 | 7 |
| S08 | missing_both_with_relation | True | 7.322 | 3 | 7 |
| S09 | only_start_token | False | 1.21 | 0 | 1 |
| S10 | only_end_token | True | 13.264 | 3 | 7 |
| S11 | comment_only | True | 11.823 | 3 | 7 |
| S12 | whitespace_empty | True | 13.997 | 3 | 7 |
| S13 | no_class_relation_with_tags | True | 3.259 | 1 | 3 |
| S14 | missing_start_no_class | True | 8.238 | 3 | 7 |
| S15 | missing_end_no_class | True | 7.555 | 3 | 7 |
| S16 | duplicate_class | True | 11.319 | 3 | 7 |
| S17 | duplicate_class_missing_start | True | 14.253 | 3 | 7 |
| S18 | duplicate_class_missing_end | True | 11.227 | 3 | 7 |
| S19 | duplicate_lowercase | True | 10.323 | 3 | 7 |
| S20 | duplicate_with_relation | True | 3.523 | 1 | 3 |
| S21 | unbalanced_brace | True | 12.14 | 3 | 7 |
| S22 | extra_closing_brace | True | 11.257 | 3 | 7 |
| S23 | missing_boundary_and_unbalanced_brace | True | 19.441 | 3 | 7 |
| S24 | missing_end_lowercase_class | True | 9.309 | 3 | 7 |
| S25 | missing_start_lowercase_class | True | 10.178 | 3 | 7 |
| S26 | missing_start_isolated_classes | True | 13.206 | 3 | 7 |
| S27 | missing_end_isolated_classes | True | 10.326 | 3 | 7 |
| S28 | missing_end_cyclic_dependency | True | 8.472 | 3 | 7 |
| S29 | missing_start_cycle | True | 7.944 | 3 | 7 |
| S30 | missing_start_god_class_warning | True | 10.341 | 3 | 7 |
| S31 | missing_both_god_class_warning | True | 9.092 | 3 | 7 |
| S32 | missing_start_truncated_relation_target | True | 14.555 | 3 | 7 |
| S33 | missing_end_truncated_relation_source | True | 9.809 | 3 | 7 |
| S34 | missing_end_truncated_relation | False | 1.277 | 0 | 1 |
| S35 | duplicate_and_unbalanced_brace | True | 8.722 | 3 | 7 |
| S36 | duplicate_three_times | True | 5.818 | 2 | 5 |
| S37 | duplicate_interface_like_class | True | 11.655 | 3 | 7 |
| S38 | only_notes | True | 9.609 | 3 | 7 |
| S39 | missing_both_only_notes | True | 11.398 | 3 | 7 |
| S40 | duplicate_with_missing_both | True | 17.513 | 3 | 7 |
| S41 | mixed_missing_start_duplicate_relation | True | 12.18 | 3 | 7 |
| S42 | mixed_missing_end_duplicate_relation | True | 3.348 | 1 | 3 |
| S43 | missing_end_self_relation | True | 7.374 | 3 | 7 |
| S44 | missing_start_self_relation | True | 7.01 | 3 | 7 |
| S45 | class_keyword_without_name | True | 9.268 | 3 | 7 |
| S46 | missing_end_class_keyword_without_name | True | 13.838 | 3 | 7 |
| S47 | invalid_lowercase_duplicate_relation | True | 9.837 | 3 | 7 |
| S48 | duplicate_and_cycle | True | 11.301 | 3 | 7 |
| S49 | missing_both_duplicate_and_cycle | True | 10.836 | 3 | 7 |
| S50 | complex_mixed_defect | False | 1.443 | 0 | 1 |
