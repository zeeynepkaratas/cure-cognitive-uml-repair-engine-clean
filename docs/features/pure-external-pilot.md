# PURE-derived P01–P10 repair pilot

Ten selected requirement excerpts have manually curated UML references and
controlled injected structural defects. This pilot does not establish broad
real-world generalization. Its results are retained in
`backend/evaluation/results/pure_external_{deterministic,llm}_experiment.json`.

| Mode | Project valid | PlantUML valid | Critic valid | Mean class F1 | Mean endpoint-pair F1 |
|---|---:|---:|---:|---:|---:|
| No repair (local audit, 2026-10-20) | 0/10 | 2/10 | N/A | N/A | N/A |
| Deterministic | 7/10 | 10/10 | N/A | 1.000 | 1.000 |
| LLM (`gpt-4o-mini`, temperature 0, budget 3) | 9/10 | 9/10 | 2/10 | 0.864 | 0.914 |

P04 fails both LLM validation criteria. Deterministic F1=1 applies to **all ten**
cases, including the three project-invalid outputs: set metrics discard repeated
class declarations. A perfect name/pair score therefore does not prove valid UML.
P03 and P08 already compile before any repair.

| LLM metric | n | Mean | Sample SD | Min | Max |
|---|---:|---:|---:|---:|---:|
| Class F1, P04 included | 10 | 0.8644 | 0.0793 | 0.8000 | 1.0000 |
| Pair F1, P04 included | 10 | 0.9137 | 0.0786 | 0.8000 | 1.0000 |
| Class F1, P04 excluded | 9 | 0.8716 | 0.0806 | 0.8000 | 1.0000 |
| Pair F1, P04 excluded | 9 | 0.9041 | 0.0769 | 0.8000 | 1.0000 |

These statistics use retained per-case values (rounded to three decimals),
with SD denominator n−1. Deterministic mean/min/max are 1 and SD is 0 with
P04 included or excluded. References contain 4–5 unique classes and 3–5 pairs.

Extra classes are Order and OrderItem in P03/P05/P06/P07/P08, OrderItem in
P09, and User in P10. None of these cases loses a reference class or pair.
P07 class F1=2×4/(4+6)=0.800; its pair F1 remains 1.000. Added attributes and
constraints, relationship types, multiplicities, roles and labels are outside
these metrics. The fixed retrieved rules are a possible confound; their causal
contribution has not been isolated experimentally.

Mean endpoint time is 17.200 s (`sure_saniye`). Two Critic terminal flags are
true; one is also project-valid. No new LLM run was made for this audit.
Documentation release: `paper-submission-v3`; retained experiment outputs are unchanged.
For PURE licensing, attribution and unresolved original document identities,
see `../../data_pipeline/datasets/README.md` and its provenance CSV.
Per-case evidence is in `../submission-audit-2026-10-20/`.
