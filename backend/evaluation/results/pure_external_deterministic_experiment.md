# PURE-Derived Deterministic Repair Pilot

This preliminary pilot does not replace the shared S01-S50 benchmark.
It uses selected PURE requirement excerpts, curated reference UML models, and controlled injected PlantUML defects.

## Summary

- Total cases: 10
- Successful repairs: 7
- Failed repairs: 3
- Success rate: 70.0%
- Wilson 95% CI: 39.7%-89.2%
- Mean class F1 against reference UML: 1.0
- Mean relationship F1 against reference UML: 1.0

## Execution Metadata

- Commit SHA: `739890bb0221fe92873e5504052f80077d72ca56`
- Generated at UTC: `2026-07-29T09:39:56.219747+00:00`
- Python: `3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]`
- Platform: `Windows-11-10.0.26200-SP0`
- Model: `none`
- Temperature: `none`
- Max iterations: `3`

## Case Results

| Case | PURE row | Category | Final success | Class F1 | Relationship F1 |
|---|---:|---|---:|---:|---:|
| P01 | 30 | missing_startuml | True | 1.0 | 1.0 |
| P02 | 31 | missing_enduml | True | 1.0 | 1.0 |
| P03 | 33 | duplicate_class | False | 1.0 | 1.0 |
| P04 | 37 | missing_both_boundaries | True | 1.0 | 1.0 |
| P05 | 42 | missing_enduml | True | 1.0 | 1.0 |
| P06 | 49 | duplicate_class_missing_start | False | 1.0 | 1.0 |
| P07 | 51 | missing_startuml | True | 1.0 | 1.0 |
| P08 | 59 | duplicate_class | False | 1.0 | 1.0 |
| P09 | 64 | missing_both_boundaries | True | 1.0 | 1.0 |
| P10 | 106 | missing_enduml | True | 1.0 | 1.0 |
