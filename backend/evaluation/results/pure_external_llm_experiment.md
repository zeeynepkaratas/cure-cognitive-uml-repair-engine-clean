# PURE-Derived LLM Repair Pilot

This preliminary pilot does not replace the shared S01-S50 benchmark.
It uses selected PURE requirement excerpts, curated reference UML models, and controlled injected PlantUML defects.

## Summary

- Total cases: 10
- Successful repairs: 10
- Failed repairs: 0
- Success rate: 100.0%
- Wilson 95% CI: 72.2%-100.0%
- Mean class F1 against reference UML: 0.773
- Mean relationship F1 against reference UML: 0.845
- Agent terminal-state valid: 0
- Final-valid and agent-terminal-valid: 0
- Final-valid but agent-terminal-invalid: 10

Success is defined by the endpoint's final syntax/OCL validation. The
`agent_is_valid` field is a secondary LangGraph terminal-state diagnostic
from the internal Critic-Healer loop and should not be interpreted as the
primary repair-success criterion.

## Case Results

| Case | PURE row | Category | Final success | Class F1 | Relationship F1 | LLM calls |
|---|---:|---|---:|---:|---:|---:|
| P01 | 30 | missing_startuml | True | 0.8 | 1.0 | 7 |
| P02 | 31 | missing_enduml | True | 0.833 | 0.889 | 7 |
| P03 | 33 | duplicate_class | True | 0.727 | 0.857 | 7 |
| P04 | 37 | missing_both_boundaries | True | 0.8 | 0.857 | 7 |
| P05 | 42 | missing_enduml | True | 0.727 | 0.75 | 7 |
| P06 | 49 | duplicate_class_missing_start | True | 0.833 | 0.889 | 7 |
| P07 | 51 | missing_startuml | True | 0.727 | 0.6 | 7 |
| P08 | 59 | duplicate_class | True | 0.833 | 1.0 | 7 |
| P09 | 64 | missing_both_boundaries | True | 0.727 | 0.857 | 7 |
| P10 | 106 | missing_enduml | True | 0.727 | 0.75 | 7 |
