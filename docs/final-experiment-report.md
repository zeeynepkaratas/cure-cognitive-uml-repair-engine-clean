# CURE Final Experiment Report

This report records the final experiment readiness check for the `fix/validation-and-metrics` branch.
No paper, figure, table, or benchmark-case files were modified during this check.

## 1. Final Experiment Commit

- Repository: `zeeynepkaratas/cure-cognitive-uml-repair-engine-clean`
- Branch: `fix/validation-and-metrics`
- Expected starting commit: `665d20ca8ba5a88e1db541de6fe2d48f2d5f2052`
- Verified experiment code commit: `665d20ca8ba5a88e1db541de6fe2d48f2d5f2052`
- Local branch and remote branch: matched at the verified commit.
- Working tree before readiness checks: clean.

Recorded startup commands:

```text
git branch --show-current
fix/validation-and-metrics

git rev-parse HEAD
665d20ca8ba5a88e1db541de6fe2d48f2d5f2052

git status --short
<empty>

git log -5 --oneline
665d20c Regenerate fallback results with runtime separation
77d5aa5 Fix PURE deterministic result compile metadata
b5df0f2 Separate fallback and PlantUML validation metrics
ef981f5 Regenerate results after validation fixes
d18c96d Add PlantUML runtime and structured validation fixes
```

## 2. Environment

- Python used for available checks: `Python 3.12.13`
- Platform: `Windows-11-10.0.26200-SP0`
- Clean `.venv` creation was attempted.
- Package installation could not be completed because network access was blocked by the execution environment.
- As a result, the clean `.venv` did not contain the required project packages.

Required import check in the clean `.venv`:

```text
fastapi: MISSING
pydantic: MISSING
langgraph: MISSING
langchain: MISSING
langchain_openai: MISSING
faiss: MISSING
pandas: MISSING
pytest: MISSING
```

The bundled Codex Python runtime contained `pydantic` and `pandas`, but did not contain `fastapi`, `langgraph`, `langchain`, `langchain_openai`, `faiss`, or `pytest`.

Important interpretation: FastAPI exists as a project dependency and is imported by the project code, but it was not installed in the available Python runtime used for this check.

## 3. Java and PlantUML Runtime

Java was available:

```text
java version "23" 2024-09-17
Java(TM) SE Runtime Environment (build 23+37-2369)
Java HotSpot(TM) 64-Bit Server VM (build 23+37-2369, mixed mode, sharing)
```

PlantUML runtime was not available:

- `PLANTUML_JAR`: not set
- `PLANTUML_CMD`: not set
- `plantuml` command on `PATH`: not found
- Local `*plantuml*.jar` search under the repository: no JAR found
- PlantUML version: not available
- PlantUML JAR SHA-256: not available
- PlantUML runtime available: `false`

Because the real PlantUML runtime was unavailable, PlantUML-validated benchmark results were not generated.

## 4. PlantUML Integration-Test Results

The required real PlantUML integration test was not run.

Reason: no accessible PlantUML runtime was configured. The protocol requires a real PlantUML JAR or command before the benchmark experiments. Mock output, fallback SVG, or project-defined lightweight validation cannot replace this integration test.

Expected valid-case and invalid-case runtime checks therefore remain blocked until `PLANTUML_JAR` or `PLANTUML_CMD` is configured.

## 5. Test-Suite Results

Available dependency-light tests were run with the bundled Python runtime.

```text
backend/tests/test_validation_infrastructure.py: 11/11 passed
backend/tests/test_plantuml_normalizer.py: 3/3 passed
backend/tests/test_validation_benchmark.py: 5/5 passed
backend/tests/test_full.py: 20/20 passed
```

API contract test:

```text
backend/tests/test_api_contracts.py
SKIP: fastapi paketi bu ortamda kurulu degil; requirements.txt ile kurulunca API kontrat testi calisir.
```

Summary for runnable checks:

- Passed runnable tests: `39`
- Failed runnable tests: `0`
- Skipped tests/files: `1` API contract test file, because FastAPI was not installed in the available runtime

Because the API contract test was skipped, the full pre-experiment test gate was not satisfied.

## 6. Shared Deterministic S01-S50 Results

Final benchmark was not rerun in this check.

Reason: the required real PlantUML runtime integration test failed at the environment-readiness stage because no PlantUML runtime was available.

Existing canonical files remain in `backend/evaluation/results/`, but they were not regenerated as final results in this run.

## 7. PURE Deterministic P01-P10 Results

Final benchmark was not rerun in this check.

Reason: the required real PlantUML runtime integration test failed at the environment-readiness stage because no PlantUML runtime was available.

Existing canonical files remain in `backend/evaluation/results/`, but they were not regenerated as final results in this run.

## 8. Shared LLM S01-S50 Results

Final LLM benchmark was not run.

Reasons:

- `OPENAI_API_KEY` was not set in the environment.
- `OPENAI_MODEL` was not set.
- `OPENAI_TEMPERATURE` was not set.
- Required LLM dependencies were not installed in the clean `.venv`.
- Real PlantUML runtime was not available.

No synthetic LLM result was produced.
No legacy LLM result was reused as a new result.

## 9. PURE LLM P01-P10 Results

Final LLM pilot benchmark was not run.

Reasons:

- `OPENAI_API_KEY` was not set in the environment.
- `OPENAI_MODEL` was not set.
- `OPENAI_TEMPERATURE` was not set.
- Required LLM dependencies were not installed in the clean `.venv`.
- Real PlantUML runtime was not available.

No synthetic LLM result was produced.
No legacy LLM result was reused as a new result.

## 10. Critic Terminal-State Analysis

No new LLM run was completed, so no new Critic terminal-state counts were generated in this check.

The code-level structured Critic parser and repair routing behavior were covered by the runnable test suite:

- Structured dict decisions were parsed.
- Legacy `GECERLI.` output remained backward-compatible.
- Repair routing stopped after the configured repair-attempt limit.

## 11. Repair-Attempt Distribution

No new LLM run was completed, so no new repair-attempt distribution was generated in this check.

## 12. Latency Results

No final latency benchmark was rerun in this check.

Existing latency files remain available, but they were not regenerated as final PlantUML-runtime or LLM-inclusive latency evidence during this readiness check.

## 13. P01 Regression Check

The final PURE LLM P01 regression check was not run because the LLM benchmark was blocked by missing `OPENAI_API_KEY`, missing LLM dependencies, and missing PlantUML runtime.

No P01 result is reported as final in this check.

## 14. Old Legacy vs New Results

Legacy results remain preserved under:

```text
backend/evaluation/results/legacy_pre_validation_fix/
```

The legacy files were not moved back into the canonical result location and were not reported as new results.

| Metric | Legacy pre-fix | New project-defined | New PlantUML-validated | Interpretation |
|---|---:|---:|---:|---|
| Shared deterministic S01-S50 | Preserved in legacy folder | Not rerun in this check | Not produced | Blocked by missing PlantUML runtime |
| PURE deterministic P01-P10 | Preserved in legacy folder | Not rerun in this check | Not produced | Blocked by missing PlantUML runtime |
| Shared LLM S01-S50 | Preserved in legacy folder | Not produced | Not produced | Blocked by missing API key, dependencies, and PlantUML runtime |
| PURE LLM P01-P10 | Preserved in legacy folder | Not produced | Not produced | Blocked by missing API key, dependencies, and PlantUML runtime |

## 15. Changed Success Classifications

No new benchmark run was completed, so no changed success classifications were computed.

The existing code distinguishes project-defined lightweight success from PlantUML-validated success, but final PlantUML-validated fields cannot be populated until a real PlantUML runtime is available.

## 16. Metric Limitations

No new metric values are reported from this check.

The current metric design should still be interpreted with the following limitations:

- Project-defined lightweight validation is not equivalent to real PlantUML validation.
- PlantUML-validated success requires an actual PlantUML runtime.
- Relationship F1 is defined as source-target endpoint-pair F1.
- Relationship type, multiplicity values, and relation labels are not scored by the endpoint-pair F1 metric.
- LLM-as-a-Judge style conclusions require separate care because no new LLM run was completed here.

## 17. Technical Failures

The final experiment protocol did not proceed past readiness checks.

Blocking issues:

1. Clean Python environment could not install required packages because network access was blocked.
2. FastAPI was not installed in the available runtime, so API contract test remained skipped.
3. No PlantUML JAR or PlantUML command was available, so real PlantUML integration test could not run.
4. `OPENAI_API_KEY` was not set, so LLM experiments could not run.

No fake results were created.
No legacy results were presented as new final results.

## 18. Exact Reproduction Commands

After installing dependencies and configuring runtime variables, the final experiment protocol should be rerun from the verified branch:

```powershell
cd C:\Users\zeyne\Documents\Codex\2026-07-22\se\outputs\CURE_clean_github_repo
git checkout fix/validation-and-metrics
git status --short

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt -r ai_core\requirements.txt pytest pandas

$env:PLANTUML_JAR="C:\tools\plantuml\plantuml.jar"
$env:OPENAI_API_KEY="<set only in terminal; do not write to files>"
$env:OPENAI_MODEL="gpt-4o-mini"
$env:OPENAI_TEMPERATURE="0"

java -version
java -jar $env:PLANTUML_JAR -version
Get-FileHash $env:PLANTUML_JAR -Algorithm SHA256

python backend\tests\test_validation_infrastructure.py
python backend\tests\test_plantuml_normalizer.py
python backend\tests\test_validation_benchmark.py
python backend\tests\test_full.py
python backend\tests\test_api_contracts.py

python backend\evaluation\shared_benchmark_deterministic_experiment.py
python backend\evaluation\pure_external_deterministic_experiment.py
python backend\evaluation\shared_benchmark_llm_experiment.py --max-iterations 3
python backend\evaluation\pure_external_llm_experiment.py --max-iterations 3
```

## 19. Result File List

Canonical result files currently present but not regenerated in this final readiness check:

```text
backend/evaluation/results/deterministic_analysis_latency_experiment.csv
backend/evaluation/results/deterministic_analysis_latency_experiment.json
backend/evaluation/results/deterministic_analysis_latency_experiment.md
backend/evaluation/results/pure_external_deterministic_experiment.csv
backend/evaluation/results/pure_external_deterministic_experiment.json
backend/evaluation/results/pure_external_deterministic_experiment.md
backend/evaluation/results/shared_benchmark_deterministic_experiment.csv
backend/evaluation/results/shared_benchmark_deterministic_experiment.json
backend/evaluation/results/shared_benchmark_deterministic_experiment.md
backend/evaluation/results/validation_report.md
backend/evaluation/results/validation_results.json
backend/evaluation/results/llm_experiments_not_run.md
backend/evaluation/results/plantuml_runtime_experiments_not_run.md
```

Legacy preserved files:

```text
backend/evaluation/results/legacy_pre_validation_fix/
```

## 20. Final Experiment Commit SHA

`665d20ca8ba5a88e1db541de6fe2d48f2d5f2052`

This SHA identifies the code state checked before attempting final experiment execution.

## 21. Result-Publication Commit SHA

This report is intended to be committed separately from the experiment code commit. The publication commit SHA is recorded in the final delivery message after commit creation.
