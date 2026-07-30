# Deterministic /api/analyze Latency Experiment

This is a reproducible latency check for the non-LLM analyze workload.
It should not be interpreted as LLM repair latency.

## Summary

- Run id: `c7074930-f417-478a-8612-d79072956c60`
- Generated at: `2026-07-29T10:33:17.381909+00:00`
- Commit SHA: `77d5aa5df248d8c58408e5543804670bc1a53211`
- Python: `3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]`
- Platform: `Windows-11-10.0.26200-SP0`
- Model: `none`
- Temperature: `none`
- Max iterations: `None`
- Measurement scope: `deterministic_analyze_pipeline_no_llm`
- Request count: 50
- Successful count: 50
- Average latency: 0.981 ms
- Min latency: 0.51 ms
- Max latency: 12.763 ms
- P50 latency: 0.704 ms
- P95 latency: 1.141 ms
- P99 latency: 12.763 ms
- SLA pass rate: 100.0%
- LLM calls: 0

## Scope Note

The measured chain is:

```text
srs_to_plantuml -> validate_ocl -> calculate_semantic_fidelity
```

Real LLM repair evidence is measured separately by
`backend/evaluation/shared_benchmark_llm_experiment.py`.
