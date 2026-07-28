# PURE-Derived Repair Pilot

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

The deterministic F1=1.000 values apply only to the structurally repaired
deterministic cases. They should not be interpreted as evidence that the
deterministic layer is semantically stronger overall; the deterministic repair
mostly restores simple boundaries and therefore avoids adding new graph content,
but it also leaves three pilot cases unrepaired.

The LLM pilot used the same prototype retrieval context as the main
Critic-Healer workflow, including the fixed curated OCL rules in
`ai_core/src/rag/ocl_retriever.py`. These rules can encourage extra classes or
relations such as `Order`, `OrderItem`, `Product`, or `User`, so lower
graph-level F1 values should be interpreted as a semantic-preservation
limitation and possible retrieval confound.

Success is defined by the endpoint's final syntax/OCL validation. The
`agent_is_valid` field is a secondary LangGraph terminal-state diagnostic; in
this pilot, 0/10 cases ended with `agent_is_valid=True` even though 10/10
reached final structural validity.
Because the Critic uses a strict prompt and the same fixed curated OCL-rule
retrieval context, this field may reflect retrieval-rule mismatch or over-strict
Critic behavior rather than an independent semantic verdict.

This result should be reported as a preliminary PURE-derived pilot, not as a
broad real-world generalization claim.

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
