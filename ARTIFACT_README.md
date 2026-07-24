# CURE Anonymous Software Artifact

This package is an anonymized source-code snapshot accompanying the CURE submission.

It intentionally excludes Git history, branch names, commit metadata, author metadata, and repository-owner information. The included files correspond to the final source tree used for the reported S01-S50 shared repair benchmark results.

Key reproducibility entry points:

- `backend/evaluation/shared_repair_benchmark_cases.py`
- `backend/evaluation/repair_benchmark_utils.py`
- `backend/evaluation/shared_benchmark_deterministic_experiment.py`
- `backend/evaluation/shared_benchmark_llm_experiment.py`
- `backend/evaluation/results/shared_benchmark_deterministic_experiment.*`
- `backend/evaluation/results/shared_benchmark_llm_experiment.*`

The autonomous LLM experiment requires an OpenAI API key in the local execution environment.
