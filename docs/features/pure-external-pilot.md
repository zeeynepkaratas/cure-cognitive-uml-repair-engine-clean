# PURE-Derived External Repair Pilot

## Scope

This preliminary pilot supplements, but does not replace, the shared S01-S50
repair benchmark. It uses 10 selected PURE requirement excerpts, curated
reference UML models, and controlled injected PlantUML defects.

The pilot is intended to check two separate properties:

- whether each repair output reaches final structural validity;
- how closely the final UML graph matches the curated reference UML model.

## Results

| Repair mode | Cases | Structurally valid repairs | Success rate | Wilson 95% CI | Mean class F1 | Mean relationship F1 |
|---|---:|---:|---:|---:|---:|---:|
| Deterministic backend repair | 10 | 7 | 70.0% | 39.7%-89.2% | 1.000 | 1.000 |
| LLM autonomous repair (`gpt-4o-mini`) | 10 | 10 | 100.0% | 72.2%-100.0% | 0.773 | 0.845 |

## Interpretation

The deterministic repair layer repaired boundary-related defects but failed on
duplicate-class defects. The LLM-based repair endpoint reached final structural
validity on all 10 pilot cases. However, graph-level comparison against the
curated reference UML models showed imperfect semantic preservation, mainly due
to extra classes or relationships introduced during repair.

This result should be reported as a preliminary external pilot, not as a broad
real-world generalization claim.

## Files

```text
backend/evaluation/pure_external_repair_cases.py
backend/evaluation/pure_external_metrics.py
backend/evaluation/pure_external_deterministic_experiment.py
backend/evaluation/pure_external_llm_experiment.py
backend/evaluation/results/pure_external_deterministic_experiment.csv
backend/evaluation/results/pure_external_deterministic_experiment.json
backend/evaluation/results/pure_external_deterministic_experiment.md
backend/evaluation/results/pure_external_llm_experiment.csv
backend/evaluation/results/pure_external_llm_experiment.json
backend/evaluation/results/pure_external_llm_experiment.md
```

## Reproduction

```bash
python backend/evaluation/pure_external_deterministic_experiment.py
$env:OPENAI_API_KEY="sk-..."
python backend/evaluation/pure_external_llm_experiment.py --max-iterations 3
```
