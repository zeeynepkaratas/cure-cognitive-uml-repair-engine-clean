# Deterministic /api/analyze Latency Experiment

This is a reproducible latency check for the non-LLM analyze workload.
It should not be interpreted as LLM repair latency.

## Summary

- Run id: `af5e2522-bfa9-483e-9203-d1cf95140ca1`
- Generated at: `2026-07-29T09:39:56.171586+00:00`
- Commit SHA: `739890bb0221fe92873e5504052f80077d72ca56`
- Python: `3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]`
- Platform: `Windows-11-10.0.26200-SP0`
- Model: `none`
- Temperature: `none`
- Max iterations: `None`
- Measurement scope: `deterministic_analyze_pipeline_no_llm`
- Request count: 50
- Successful count: 50
- Average latency: 4.027 ms
- Min latency: 2.521 ms
- Max latency: 29.226 ms
- P50 latency: 3.533 ms
- P95 latency: 4.165 ms
- P99 latency: 29.226 ms
- SLA pass rate: 100.0%
- LLM calls: 0

## Scope Note

The measured chain is:

```text
srs_to_plantuml -> validate_ocl -> calculate_semantic_fidelity
```

Real LLM repair evidence is measured separately by
`backend/evaluation/shared_benchmark_llm_experiment.py`.
