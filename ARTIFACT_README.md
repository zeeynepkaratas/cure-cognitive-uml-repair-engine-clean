# CURE v4 qualified research artifact

Start with [final sign-off](docs/final_closure/CLOSURE_SIGNOFF.md),
[executed verification](docs/final_closure/VERIFICATION_RUNS.md),
[manuscript handoff](docs/final_closure/PAPER_HANDOFF.md) and
[safe reviewer reproduction](docs/final_closure/REPRODUCE_FOR_REVIEWER.md).
The final source-of-truth files are under `docs/final_closure/`; earlier audit
reports and scientific results are preserved unchanged. No manuscript is edited.

## Verify existing evidence without model credentials

Use Python 3.12 (tested: 3.12.14), the exact Python locks, and a new output directory.
Activate a fresh virtual environment using the commands for your operating system:

```sh
python -m venv .venv
# Activate .venv; Windows: .venv/Scripts/Activate.ps1, Linux: source .venv/bin/activate
python -m pip install -r requirements.lock.txt -r requirements-dev.txt
python -m pip check
python tools/verify_v4_artifact.py --output docs/final_closure/reviewer-check-UNIQUE
python -m pytest -q
python -m ruff check .
```

The reviewer verifier performs no model calls, reads original results and redirects
independent audit outputs. It refuses historical output paths and nonempty output
directories. Remove `OPENAI_API_KEY` from the review shell; never paste credentials.
Do not run historical generation/analysis/finalizer writers on protected directories.
Their final replay was executed only on an identified copy outside this checkout.

Frontend (Node 22.12.0 tested, lockfile retained): from `frontend/` run `npm ci`,
`npm run lint` and `npm run build` separately. A fresh offline `npm ci` was actually
executed in this closure; its exact version/output is recorded in verification logs.
Optional live checks require Java and external PlantUML 1.2026.6, SHA-256
`89948f14c93756c7a3fb7b69078ff37e8489fd79dd430c582b931e2f65358690`.
The binary is not bundled. Docker validation remains unperformed when the executable
is absent; copy-ready optional commands are in the reviewer guide.

## Frozen study and evidence

`backend/evaluation/results_v4/test-frozen-20261022/` contains 100 input diagrams,
70 distinct SRS texts, 2,800 case-runs and 7,936 returned model calls. Shared has 50
inputs, PURE 10, semantic test 40 from 20 scenarios. C0–C2 run once; C3–C7 five times.
Snapshot: `gpt-4o-mini-2024-07-18`; temperature 0, requested seed 1729+rep. Seeds do
not prove provider determinism. Modern prompts are v4.1; C5/C6 retain legacy prompts
with lexical retrieval, not a bit-identical historical embedding replication.

Protocol/source freeze: `1ead72ff7071e1f6de5867aaa250b0483d91431f`.
Raw case/response/manifest hashes, model-reference F1, tables and plots remain
immutable. See `docs/evaluation-protocol-v4.md`, `docs/revision-report.md` and
`docs/final_closure/FINAL_EVIDENCE_MANIFEST.json`. Prior v1/v2/v3 evidence and tags
remain intact. Development runs and computational copies are not extra test samples.
All new summaries must label revised C2 **post-test exploratory**: initial shared
C2 compiled 49/50; the disclosed source fix yielded 50/50.

## Interpretation, runtime and reuse limits

Compilation, project rules and Critic acceptance are different outcomes. F1 measures
restricted structural reference agreement, not full UML/NL semantics or formal OCL
verification. M11_2 retains WeatherStation and is Critic-accepted in 5/5 observations;
passing regression tests document, rather than fix, this known error. Independent
experts, diverse external gold and semantic superiority are not established.
The PURE pilot is from one CCTNS source; P02 is a qualified paraphrase. New 18-document,
7,017-row / 7,162-chunk reconstruction does not reproduce historical 7,219 filtering.
The offline BGE/FAISS document index did not drive the frozen online repair runs.

The legacy CLI/research PlantUML renderer is **trusted-input only**. The API-only
`v5-api-sandbox` profile adds input/resource bounds, JAR verification, SANDBOX, child
environment stripping and SVG filtering; this name does not denote a new research
method or new performance experiment. It is **not public-production certified**.
Authentication, quotas, isolation/load/cancellation/privacy reviews remain external
deployment work. SVG is the actual diagram; `png_is_placeholder=true` identifies the
legacy one-pixel PNG compatibility placeholder and must not be counted as rendering.

Original code is MIT; third-party sources/dependencies keep their own terms.
See `LICENSE`, `NOTICE` and `data_pipeline/datasets/README.md` for PURE attribution,
official CC BY 4.0 declarations and the curators' underlying-rights caveat.
No anonymous hosting or reviewer acceptance is certified. Public Git history,
commit/data breadcrumbs and source quotations can identify the project. A human
contextual review and independent hosting are required before blind submission.
