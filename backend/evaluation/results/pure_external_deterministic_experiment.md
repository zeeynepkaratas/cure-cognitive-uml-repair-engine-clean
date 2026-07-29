# PURE-Derived Deterministic Repair Pilot

This preliminary pilot does not replace the shared S01-S50 benchmark.
It uses selected PURE requirement excerpts, curated reference UML models, and controlled injected PlantUML defects.

## Summary

- Total cases: 10
- Project-defined fallback repairs: 7/10
- Project-defined fallback success rate: 70.0%
- Project-defined Wilson 95% CI: 39.7%-89.2%
- PlantUML runtime available: False
- PlantUML-validated repairs: None
- PlantUML-validated Wilson 95% CI: not run
- Mean class F1 against reference UML: 1.0
- Mean relationship F1 against reference UML: 1.0
- Relationship metric: source-target endpoint-pair F1; relation type, multiplicity, and labels are not scored.

## Execution Metadata

- Commit SHA: `77d5aa5df248d8c58408e5543804670bc1a53211`
- Generated at UTC: `2026-07-29T10:33:17.940025+00:00`
- Python: `3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]`
- Platform: `Windows-11-10.0.26200-SP0`
- Model: `none`
- Temperature: `none`
- Max iterations: `3`

## Case Results

| Case | PURE row | Category | Project-defined success | PlantUML-validated success | Runtime available | Class F1 | Relationship F1 |
|---|---:|---|---:|---:|---:|---:|---:|
| P01 | 30 | missing_startuml | True | None | False | 1.0 | 1.0 |
| P02 | 31 | missing_enduml | True | None | False | 1.0 | 1.0 |
| P03 | 33 | duplicate_class | False | None | False | 1.0 | 1.0 |
| P04 | 37 | missing_both_boundaries | True | None | False | 1.0 | 1.0 |
| P05 | 42 | missing_enduml | True | None | False | 1.0 | 1.0 |
| P06 | 49 | duplicate_class_missing_start | False | None | False | 1.0 | 1.0 |
| P07 | 51 | missing_startuml | True | None | False | 1.0 | 1.0 |
| P08 | 59 | duplicate_class | False | None | False | 1.0 | 1.0 |
| P09 | 64 | missing_both_boundaries | True | None | False | 1.0 | 1.0 |
| P10 | 106 | missing_enduml | True | None | False | 1.0 | 1.0 |
