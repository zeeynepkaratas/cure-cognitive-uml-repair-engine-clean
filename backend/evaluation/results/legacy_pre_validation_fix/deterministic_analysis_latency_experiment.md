# Deterministic /api/analyze Latency Experiment

This is a reproducible latency check for the non-LLM analyze workload.
It should not be interpreted as LLM repair latency.

## Summary

- Run id: `3afe0c80-248d-418b-bcf4-22235eda65bc`
- Generated at: `2026-07-06T23:40:53.428718+00:00`
- Measurement scope: `deterministic_analyze_pipeline_no_llm`
- Request count: 50
- Successful count: 50
- Average latency: 1.054 ms
- Min latency: 0.745 ms
- Max latency: 6.796 ms
- P50 latency: 0.824 ms
- P95 latency: 1.629 ms
- P99 latency: 6.796 ms
- SLA pass rate: 100.0%
- LLM calls: 0

## Scope Note

The measured chain is:

```text
srs_to_plantuml -> validate_ocl -> calculate_semantic_fidelity
```

Real LLM repair evidence is measured separately by
`backend/evaluation/shared_benchmark_llm_experiment.py`.
