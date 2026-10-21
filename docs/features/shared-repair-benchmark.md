# Shared repair benchmark S01–S50

The retained results distinguish project-defined validation, real compilation,
and the Critic terminal flag. Source files are in `backend/evaluation/results/`:
`shared_benchmark_deterministic_experiment.json` and
`shared_benchmark_llm_experiment.json`. They have not been regenerated.

| Mode | Project-defined valid | PlantUML valid | Critic valid |
|---|---:|---:|---:|
| No repair (local audit, 2026-10-20) | 0/50 | 12/50 | N/A |
| Deterministic | 31/50 | 41/50 | N/A |
| LLM (`gpt-4o-mini`, temperature 0, budget 3) | 49/50 | 40/50 | 4/50 |

The 50 scenarios fail project validation initially; twelve already compile.
They are controlled structural defects, not a benchmark of semantic corruption.
The deterministic repair adds absent boundary tokens and a placeholder class
when no literal `class ` token is present; it does not repair arbitrary UML.

Critic-valid cases are S05, S09, S23 and S43. All four fail compilation;
S43 also fails project validation. Forty-seven cases reach three repair
attempts, but S05 is accepted on that attempt: **46/50** terminate with the
Critic still invalid after exhausting the budget.

Paired tables have deterministic pass/fail as rows and LLM pass/fail as columns:
compilation `[[33,8],[7,2]]`, project validation `[[30,1],[19,0]]`.
Exact two-sided McNemar p-values are 1.0 and 0.0000400543212890625.
Against no repair, compilation gains/losses are 29/0 (deterministic,
p=3.725290298461914e-9) and 29/1 (LLM, p=5.774199962615967e-8).
The LLM loss is S04 (empty diagram). Comparisons are exploratory and unadjusted.

The mean retained LLM endpoint time is 16.547 s (`sure_saniye`);
deterministic duration uses `elapsed_seconds`. No compiler output enters the
Critic–Healer loop; compilation checks run outside it.

The fixed `paper-submission-v2` tag contains older documentation. Do not infer
these corrected figures from that tag's README. The corrected documentation is
published as `paper-submission-v3`; the v2 tag remains unchanged. Per-case evidence, the local
baseline runtime output, and audit scripts are in
`../submission-audit-2026-10-20/`. No new LLM run was made for this audit.
