# Shared Repair Benchmark

## Scope

The current repair evaluation uses one shared benchmark of 50 invalid PlantUML
class-diagram scenarios (`S01`-`S50`). The deterministic backend repair layer
and the real LLM-based `/api/autonomous-repair` endpoint are evaluated on the
same cases.

This replaces the earlier paper-risky comparison where deterministic and LLM
repair evidence came from separate 20-case scenario sets.

## Main Results

| Repair mode | Cases | Successful repairs | Success rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| Deterministic backend repair | 50 | 31 | 62.0% | 48.2%-74.1% |
| LLM autonomous repair (`gpt-4o-mini`) | 50 | 47 | 94.0% | 83.8%-97.9% |

The LLM benchmark was run once with `max_iterations=3`. Because LLM behavior is
non-deterministic, repeated runs should not be used to select a preferred
success rate.

## Files

```text
backend/evaluation/shared_repair_benchmark_cases.py
backend/evaluation/shared_benchmark_deterministic_experiment.py
backend/evaluation/shared_benchmark_llm_experiment.py
backend/evaluation/results/shared_benchmark_deterministic_experiment.csv
backend/evaluation/results/shared_benchmark_deterministic_experiment.json
backend/evaluation/results/shared_benchmark_deterministic_experiment.md
backend/evaluation/results/shared_benchmark_llm_experiment.csv
backend/evaluation/results/shared_benchmark_llm_experiment.json
backend/evaluation/results/shared_benchmark_llm_experiment.md
```

## Reproduction

Deterministic benchmark:

```bash
python backend/evaluation/shared_benchmark_deterministic_experiment.py
```

LLM benchmark:

```bash
$env:OPENAI_API_KEY="sk-..."
python backend/evaluation/shared_benchmark_llm_experiment.py --max-iterations 3
```

The LLM script writes `.partial.csv` and `.partial.json` files after each
completed case during an active run. These partial files are interruption
checkpoints only and should not be reported as final paper results.

## Failure Cases

The final LLM run failed on three cases:

| Case | Category |
|---|---|
| S09 | only_start_token |
| S34 | missing_end_truncated_relation |
| S50 | complex_mixed_defect |
