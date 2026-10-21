# Semantic defect taxonomy

The 30 explicit requirement/model pairs are new curated constructions, not externally validated PURE gold annotations. M01–M10 are inspired by recorded sentences in the retained PURE CSV; the original document mapping remains NOT RECORDED. Each extension spells out its classes, attributes, direction, type and multiplicities. Independent domain-expert review is pending. The shared graph template limits structural diversity and must be disclosed.

| ID | Operator |
|---|---|
| D1 | Delete one class and its incident edges |
| D2 | Add a class from a fixed unrelated distractor pool |
| D3 | Delete one relationship |
| D4 | Redirect one relationship to another declared class |
| D5 | Reverse the endpoint direction |
| D6 | Change relationship type to inheritance (or association) |
| D7 | Rename one class and every endpoint reference to a non-SRS term |
| D8 | Remove an id attribute |
| D9 | Duplicate a class declaration |
| D10 | Remove the end boundary |

Seeds and exact selected elements are recorded per case. Cases are split by scenario: M01–M10 (20 cases) are development only; M11–M30 (40 cases) are test only. No scenario crosses the split. Some cases combine two operators. Compiler validity is measured in C0 and never inferred from defect type. The nullable compiles_before data field is intentionally unmeasured in the frozen input file; measured flags live in run results.
