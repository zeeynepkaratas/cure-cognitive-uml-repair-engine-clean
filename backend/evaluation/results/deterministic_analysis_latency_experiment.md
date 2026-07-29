# Deterministic /api/analyze Latency Experiment

This is a reproducible latency check for the non-LLM analyze workload.
It should not be interpreted as LLM repair latency.

## Summary

- Run id: `297a44b9-dc0b-4a20-adb2-17c770083b1c`
- Generated at: `2026-07-29T10:03:49.428760+00:00`
- Commit SHA: `d18c96d2ce50bc01c1d044ca18714c68c4b8954e`
- Python: `3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]`
- Platform: `Windows-11-10.0.26200-SP0`
- Model: `none`
- Temperature: `none`
- Max iterations: `None`
- Measurement scope: `deterministic_analyze_pipeline_no_llm`
- Request count: 50
- Successful count: 50
- Average latency: 1.181 ms
- Min latency: 0.552 ms
- Max latency: 16.197 ms
- P50 latency: 0.764 ms
- P95 latency: 1.569 ms
- P99 latency: 16.197 ms
- SLA pass rate: 100.0%
- LLM calls: 0

## Scope Note

The measured chain is:

```text
srs_to_plantuml -> validate_ocl -> calculate_semantic_fidelity
```

Real LLM repair evidence is measured separately by
`backend/evaluation/shared_benchmark_llm_experiment.py`.
