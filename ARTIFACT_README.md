# CURE Cleaned Source-Code Artifact

This package is a cleaned source-code snapshot accompanying the CURE submission.

It excludes development branch history and commit-level metadata. The included files correspond to the final source tree used for the reported S01-S50 shared repair benchmark results and the preliminary PURE-derived external repair pilot.

Key reproducibility entry points:

- `backend/evaluation/shared_repair_benchmark_cases.py`
- `backend/evaluation/repair_benchmark_utils.py`
- `backend/evaluation/shared_benchmark_deterministic_experiment.py`
- `backend/evaluation/shared_benchmark_llm_experiment.py`
- `backend/evaluation/pure_external_repair_cases.py`
- `backend/evaluation/pure_external_metrics.py`
- `backend/evaluation/pure_external_deterministic_experiment.py`
- `backend/evaluation/pure_external_llm_experiment.py`
- `backend/evaluation/results/shared_benchmark_deterministic_experiment.*`
- `backend/evaluation/results/shared_benchmark_llm_experiment.*`
- `backend/evaluation/results/pure_external_deterministic_experiment.*`
- `backend/evaluation/results/pure_external_llm_experiment.*`

The autonomous LLM experiment requires an OpenAI API key in the local execution environment.
