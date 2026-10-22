# Historical v2/v3 Experiment Report

This report retains the original single-run measurements. It is not the new v4 evaluation. See docs/revision-report.md and the results_v4 run manifests for current execution status.

## 1. Final Status

All four planned final experiment runs were completed successfully in the configured local environment. Each LLM experiment was executed once, and the obtained result was retained without rerunning to select a preferred outcome.

Final runs:

1. Shared deterministic S01-S50 benchmark
2. PURE-derived deterministic P01-P10 pilot
3. Shared LLM S01-S50 benchmark
4. PURE-derived LLM P01-P10 pilot

No legacy result was presented as a newly generated final result.

## 2. Repository State

- Branch: `fix/validation-and-metrics`
- Experiment run HEAD: `f2689cc2407c0d6f17eaee272f93cd233063cfc7`
- Experiment implementation commit: `665d20ca8ba5a88e1db541de6fe2d48f2d5f2052`
- All four JSON result files record the same run HEAD.
- The worktree was clean immediately before the experiment runs.
- No source-code file was modified during the runs.

## 3. Environment

- Operating system: `Windows-11-10.0.26200-SP0`
- Python: `3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)]`
- Model: `gpt-4o-mini`
- Temperature: `0.0`
- Maximum repair attempts: `3`
- PlantUML runtime available: `True`
- PlantUML version: `1.2026.6`
- PlantUML JAR SHA-256: `89948F14C93756C7A3FB7B69078FF37E8489FD79DD430C582B931E2F65358690`
- GraphViz version: `2.44.1`
- OpenAI API key present during execution: `True`
- OpenAI API key value stored in repository files: `False`

The API key was supplied only through the terminal environment. A repository scan for an OpenAI-style secret pattern returned no matches.

## 4. Verification Tests

```text
backend/tests/test_validation_infrastructure.py: 11/11 passed
backend/tests/test_plantuml_normalizer.py: 3/3 passed
backend/tests/test_validation_benchmark.py: 5/5 passed
backend/tests/test_full.py: 20/20 passed
backend/tests/test_api_contracts.py: 4/4 passed
```

The OpenAI connection test returned `OK`. PlantUML reported that installation and file generation were successful.

## 5. Final Results

| Experiment | Project-defined success | Project-defined Wilson 95% CI | PlantUML-validated success | PlantUML Wilson 95% CI |
|---|---:|---:|---:|---:|
| Shared deterministic S01-S50 | 31/50 (62.0%) | 48.2%-74.1% | 41/50 (82.0%) | 69.2%-90.2% |
| PURE deterministic P01-P10 | 7/10 (70.0%) | 39.7%-89.2% | 10/10 (100.0%) | 72.2%-100.0% |
| Shared LLM S01-S50 | 49/50 (98.0%) | 89.5%-99.6% | 40/50 (80.0%) | 67.0%-88.8% |
| PURE LLM P01-P10 | 9/10 (90.0%) | 59.6%-98.2% | 9/10 (90.0%) | 59.6%-98.2% |

Project-defined lightweight validation and real PlantUML-runtime validation answer different questions and must be reported separately.

## 6. Shared Deterministic S01-S50

- Project-defined success: 31/50 (62.0%)
- PlantUML-validated success: 41/50 (82.0%)
- Initially invalid cases: 50
- Run ID: `d197b2a4-56f9-4a2a-be21-7eb63d4a7506`
- Generated at UTC: `2026-07-30T06:43:51.593543+00:00`

The deterministic layer compiled successfully in PlantUML for more cases than it passed under the repository's stricter lightweight validation.

## 7. PURE Deterministic P01-P10

- Project-defined success: 7/10 (70.0%)
- PlantUML-validated success: 10/10 (100.0%)
- Mean class F1: 1.000
- Mean relationship F1: 1.000
- Run ID: `c9bee787-cc0f-4316-8034-45ab70257ce4`

This is a preliminary controlled pilot using selected PURE excerpts, curated reference UML models, and injected defects. It does not replace the shared S01-S50 benchmark.

## 8. Shared LLM S01-S50

- Project-defined success: 49/50 (98.0%)
- PlantUML-validated success: 40/50 (80.0%)
- Agent terminal-state valid: 4/50
- Final valid and agent-terminal valid: 3/50
- Final valid but agent-terminal invalid: 46/50
- Total recorded wall time: 958.287 seconds
- Run ID: `36d51543-d1a7-4bd6-bb2c-caf1a7dc89e0`

The 98.0% project-defined result must not be reported as real PlantUML success; the real PlantUML-runtime rate was 80.0%.

## 9. PURE LLM P01-P10

- Project-defined success: 9/10 (90.0%)
- PlantUML-validated success: 9/10 (90.0%)
- Mean class F1: 0.864
- Mean relationship F1: 0.914
- Agent terminal-state valid: 2/10
- Final valid and agent-terminal valid: 1/10
- Final valid but agent-terminal invalid: 8/10
- Run ID: `a9c8b39c-1b98-49a5-8de4-5dcef0ccd156`

P04 was the only PURE LLM case that failed both project-defined and PlantUML-runtime validation.

## 10. Runtime and SLA Observations

Shared LLM:

- Mean endpoint time: 16.547 seconds
- Median endpoint time: 16.811 seconds
- Minimum: 4.633 seconds
- Maximum: 24.452 seconds
- At or below 15 seconds: 9/50
- Above 15 seconds: 41/50

PURE LLM:

- Mean endpoint time: 17.200 seconds
- Median endpoint time: 16.682 seconds
- Minimum: 15.527 seconds
- Maximum: 20.286 seconds
- At or below 15 seconds: 0/10
- Above 15 seconds: 10/10

These are observed run timings, not a separately controlled latency benchmark.

## 11. Agent Terminal-State Diagnostic

`agent_is_valid` is a secondary LangGraph terminal-state diagnostic, not the primary repair-success criterion. The difference between final validation and terminal-state validity suggests that the Critic often continued to report problems after the final returned diagram had passed endpoint validation. Retrieval-rule mismatch or over-strict Critic behavior are plausible explanations.

## 12. P01 Regression Check

- Project-defined success: `True`
- PlantUML-validated success: `True`
- Class F1: 1.000
- Relationship F1: 1.000
- Missing classes: []
- Extra classes: []
- Missing relationships: []
- Extra relationships: []

P01 added an `age` attribute and constraint to `User`, although these were absent from the curated reference. The F1 scores remained 1.0 because the current metrics do not score attributes, operations, or constraint text.

## 13. Metric Limitations

- Project-defined validation is not equivalent to real PlantUML validation.
- PlantUML success establishes compilability, not full semantic correctness.
- The PURE pilot includes only 10 selected and curated cases.
- Class F1 scores class-name presence but not attributes, operations, visibility, or constraints.
- Relationship F1 is source-target endpoint-pair F1.
- Relationship type, multiplicity, role names, and labels are not scored.
- The Critic terminal state is not an independent semantic correctness score.
- The LLM experiments used one model configuration and one retained run.
- Temperature 0 does not guarantee identical hosted-model output across time.
- Observed latency includes API, network, and local runtime effects.

## 14. Reproducibility

```text
Branch: fix/validation-and-metrics
Run HEAD: f2689cc2407c0d6f17eaee272f93cd233063cfc7
Experiment implementation commit: 665d20ca8ba5a88e1db541de6fe2d48f2d5f2052
Python: 3.13.5
Model: gpt-4o-mini
Temperature: 0
Maximum repair attempts: 3
PlantUML: 1.2026.6
PlantUML SHA-256: 89948F14C93756C7A3FB7B69078FF37E8489FD79DD430C582B931E2F65358690
GraphViz: 2.44.1
```

Execution order:

```powershell
python backend\evaluation\shared_benchmark_deterministic_experiment.py
python backend\evaluation\pure_external_deterministic_experiment.py
python backend\evaluation\shared_benchmark_llm_experiment.py --max-iterations 3
python backend\evaluation\pure_external_llm_experiment.py --max-iterations 3
```

The final LLM experiments must not be rerun merely to improve the reported outcome.

## 15. Final Artifacts

- `backend/evaluation/results/shared_benchmark_deterministic_experiment.*`
- `backend/evaluation/results/pure_external_deterministic_experiment.*`
- `backend/evaluation/results/shared_benchmark_llm_experiment.*`
- `backend/evaluation/results/pure_external_llm_experiment.*`

Temporary `.partial` checkpoints were moved outside the repository after final files had been generated. Historical `*_not_run.md` files describe an earlier environment-readiness state and must not be interpreted as the final experiment status.
