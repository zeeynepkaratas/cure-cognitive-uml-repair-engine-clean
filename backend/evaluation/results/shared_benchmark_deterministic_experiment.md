# Shared Benchmark Deterministic Repair Experiment

This report evaluates the deterministic backend repair layer on the
shared S01-S50 invalid PlantUML benchmark. The same benchmark is used
by `shared_benchmark_llm_experiment.py` for the LLM-based endpoint.

## Summary

- Total cases: 50
- Initially invalid cases: 50
- Project-defined fallback repairs: 31/50
- Project-defined fallback success rate: 62.0%
- Project-defined Wilson 95% CI: 48.2% - 74.1%
- PlantUML runtime available: True
- PlantUML-validated repairs: 41
- PlantUML-validated Wilson 95% CI: {'successes': 41, 'total': 50, 'rate': 0.82, 'lower': 0.692, 'upper': 0.9023, 'lower_percent': 69.2, 'upper_percent': 90.2, 'z': 1.96}

The project-defined fallback result is based on the repository's lightweight syntax/OCL-like checks.
It must not be reported as a real PlantUML-runtime-validated success rate.

## Execution Metadata

- Commit SHA: `f2689cc2407c0d6f17eaee272f93cd233063cfc7`
- Generated at UTC: `2026-07-30T06:43:51.593543+00:00`
- Python: `3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)]`
- Platform: `Windows-11-10.0.26200-SP0`
- Model: `none`
- Temperature: `none`
- Max iterations: `3`

## Case Results

| Case | Category | Initially invalid | Project-defined success | PlantUML-validated success | Runtime available | Iterations | Final errors |
|---|---|---:|---:|---:|---:|---:|---|
| S01 | missing_startuml | True | True | True | True | 1 | - |
| S02 | missing_enduml | True | True | True | True | 1 | - |
| S03 | missing_both_boundaries | True | True | True | True | 1 | - |
| S04 | empty_diagram | True | True | True | True | 1 | - |
| S05 | plain_empty_input | True | True | True | True | 1 | - |
| S06 | missing_startuml_with_relation | True | True | True | True | 1 | - |
| S07 | missing_enduml_with_relation | True | True | True | True | 1 | - |
| S08 | missing_both_with_relation | True | True | True | True | 1 | - |
| S09 | only_start_token | True | True | True | True | 1 | - |
| S10 | only_end_token | True | True | True | True | 1 | - |
| S11 | comment_only | True | True | True | True | 1 | - |
| S12 | whitespace_empty | True | True | True | True | 1 | - |
| S13 | no_class_relation_with_tags | True | True | True | True | 1 | - |
| S14 | missing_start_no_class | True | True | True | True | 1 | - |
| S15 | missing_end_no_class | True | True | True | True | 1 | - |
| S16 | duplicate_class | True | False | True | True | 1 | Tekrar eden sinif ismi: ['InventoryService'] |
| S17 | duplicate_class_missing_start | True | False | True | True | 2 | Tekrar eden sinif ismi: ['ShipmentService'] |
| S18 | duplicate_class_missing_end | True | False | True | True | 2 | Tekrar eden sinif ismi: ['DocumentParser'] |
| S19 | duplicate_lowercase | True | False | True | True | 1 | Tekrar eden sinif ismi: ['searchService'] |
| S20 | duplicate_with_relation | True | False | True | True | 1 | Tekrar eden sinif ismi: ['EventStore'] |
| S21 | unbalanced_brace | True | False | False | True | 1 | Eslesmeyen suslu parantez: 1 acik, 0 kapali; Some diagram description contains errors |
| S22 | extra_closing_brace | True | False | True | True | 1 | Eslesmeyen suslu parantez: 1 acik, 2 kapali |
| S23 | missing_boundary_and_unbalanced_brace | True | False | False | True | 2 | Eslesmeyen suslu parantez: 1 acik, 0 kapali; Some diagram description contains errors |
| S24 | missing_end_lowercase_class | True | True | True | True | 1 | - |
| S25 | missing_start_lowercase_class | True | True | True | True | 1 | - |
| S26 | missing_start_isolated_classes | True | True | True | True | 1 | - |
| S27 | missing_end_isolated_classes | True | True | True | True | 1 | - |
| S28 | missing_end_cyclic_dependency | True | True | True | True | 1 | - |
| S29 | missing_start_cycle | True | True | True | True | 1 | - |
| S30 | missing_start_god_class_warning | True | True | True | True | 1 | - |
| S31 | missing_both_god_class_warning | True | True | True | True | 1 | - |
| S32 | missing_start_truncated_relation_target | True | True | False | True | 1 | Some diagram description contains errors |
| S33 | missing_end_truncated_relation_source | True | True | False | True | 1 | Some diagram description contains errors |
| S34 | missing_end_truncated_relation | True | True | False | True | 1 | Some diagram description contains errors |
| S35 | duplicate_and_unbalanced_brace | True | False | False | True | 1 | Eslesmeyen suslu parantez: 2 acik, 1 kapali; Tekrar eden sinif ismi: ['CustomerService']; Some diagram description contains errors |
| S36 | duplicate_three_times | True | False | True | True | 1 | Tekrar eden sinif ismi: ['RoleManager'] |
| S37 | duplicate_interface_like_class | True | False | True | True | 1 | Tekrar eden sinif ismi: ['EmailSender'] |
| S38 | only_notes | True | True | True | True | 1 | - |
| S39 | missing_both_only_notes | True | True | True | True | 1 | - |
| S40 | duplicate_with_missing_both | True | False | True | True | 2 | Tekrar eden sinif ismi: ['TokenService'] |
| S41 | mixed_missing_start_duplicate_relation | True | False | True | True | 2 | Tekrar eden sinif ismi: ['AuthService'] |
| S42 | mixed_missing_end_duplicate_relation | True | False | True | True | 2 | Tekrar eden sinif ismi: ['OrderRepository'] |
| S43 | missing_end_self_relation | True | True | True | True | 1 | - |
| S44 | missing_start_self_relation | True | True | True | True | 1 | - |
| S45 | class_keyword_without_name | True | False | False | True | 1 | Hic sinif tanimlanmamis; Hic sinif tanimlanmamis; Some diagram description contains errors |
| S46 | missing_end_class_keyword_without_name | True | True | False | True | 1 | Some diagram description contains errors |
| S47 | invalid_lowercase_duplicate_relation | True | False | True | True | 1 | Tekrar eden sinif ismi: ['searchService'] |
| S48 | duplicate_and_cycle | True | False | True | True | 1 | Tekrar eden sinif ismi: ['CacheService'] |
| S49 | missing_both_duplicate_and_cycle | True | False | True | True | 2 | Tekrar eden sinif ismi: ['CacheService'] |
| S50 | complex_mixed_defect | True | False | False | True | 2 | Eslesmeyen suslu parantez: 4 acik, 3 kapali; Tekrar eden sinif ismi: ['AnalyticsService']; Some diagram description contains errors |
