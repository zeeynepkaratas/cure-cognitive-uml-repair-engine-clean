# Shared Repair Benchmark

## Scope

The current repair evaluation uses one shared benchmark of 50 invalid PlantUML
class-diagram scenarios (`S01`-`S50`). The deterministic backend repair layer
and the real LLM-based `/api/autonomous-repair` endpoint are evaluated on the
same cases.

This shared benchmark remains the main repair-evaluation basis for the current
paper revision. A separate PURE-derived external pilot is included only as a
small supplementary check.

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
backend/evaluation/repair_benchmark_utils.py
backend/evaluation/shared_benchmark_deterministic_experiment.py
backend/evaluation/shared_benchmark_llm_experiment.py
backend/evaluation/pure_external_repair_cases.py
backend/evaluation/pure_external_metrics.py
backend/evaluation/pure_external_deterministic_experiment.py
backend/evaluation/pure_external_llm_experiment.py
backend/evaluation/results/shared_benchmark_deterministic_experiment.csv
backend/evaluation/results/shared_benchmark_deterministic_experiment.json
backend/evaluation/results/shared_benchmark_deterministic_experiment.md
backend/evaluation/results/shared_benchmark_llm_experiment.csv
backend/evaluation/results/shared_benchmark_llm_experiment.json
backend/evaluation/results/shared_benchmark_llm_experiment.md
backend/evaluation/results/pure_external_deterministic_experiment.csv
backend/evaluation/results/pure_external_deterministic_experiment.json
backend/evaluation/results/pure_external_deterministic_experiment.md
backend/evaluation/results/pure_external_llm_experiment.csv
backend/evaluation/results/pure_external_llm_experiment.json
backend/evaluation/results/pure_external_llm_experiment.md
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

## PURE-Derived External Pilot

The preliminary PURE-derived pilot uses 10 selected PURE requirement excerpts,
curated reference UML models, and controlled injected PlantUML defects. It does
not replace the S01-S50 benchmark.

| Pilot repair mode | Cases | Structurally valid repairs | Success rate | Mean class F1 | Mean relationship F1 |
|---|---:|---:|---:|---:|---:|
| Deterministic backend repair | 10 | 7 | 70.0% | 1.000 | 1.000 |
| LLM autonomous repair (`gpt-4o-mini`) | 10 | 10 | 100.0% | 0.773 | 0.845 |

The LLM pilot result should be interpreted as structural repair success plus a
separate graph-level semantic-preservation check. The F1 values show that final
structural validity does not imply perfect preservation of the curated reference
UML graph.

Reproduce the pilot:

```bash
python backend/evaluation/pure_external_deterministic_experiment.py
$env:OPENAI_API_KEY="sk-..."
python backend/evaluation/pure_external_llm_experiment.py --max-iterations 3
```

## Failure Cases

The final LLM run failed on three cases:

| Case | Category |
|---|---|
| S09 | only_start_token |
| S34 | missing_end_truncated_relation |
| S50 | complex_mixed_defect |
