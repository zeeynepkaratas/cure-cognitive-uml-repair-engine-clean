# CURE Cognitive UML Repair Engine

CURE repairs PlantUML class diagrams. Revision v4 separates real compilation,
project-defined checks, Critic decisions, and reference-model agreement.
A project-only pass is not proof of successful compilation or semantic correctness.

## Install and run

Use Python 3.12 and Node.js 22 or newer. The lock file records the measured
environment; loose requirement files are kept for development.

```sh
python -m venv .venv
# Activate the environment for your shell.
pip install -r requirements.lock.txt -r requirements-dev.txt
bash tools/setup_plantuml.sh "$PWD/tools/plantuml.jar"
export PLANTUML_JAR="$PWD/tools/plantuml.jar"
uvicorn backend.src.api.endpoints:app --host 127.0.0.1 --port 8000
```

In frontend/, run npm ci and npm run dev. Configure browser origins using
CURE_CORS_ORIGINS. Keep model credentials in the local OPENAI_API_KEY environment
variable; never commit them. Docker includes a JRE, Graphviz and the pinned JAR.

## Validate

```sh
python -m pytest
python -m ruff check .
cd frontend
npm run lint
npm run build
```

Scripted fake responses test control flow without network; they never produce
experimental results. Compiler-dependent tests skip when Java/JAR is absent.

## Reproduce

Read docs/evaluation-protocol-v4.md before any run. All conditions use identical
inputs. Semantic development and test scenarios are disjoint; legacy S/P sets
are test-only. New measurements go exclusively into results_v4/<run_id>/.

```sh
python -m backend.evaluation.run_matrix --dry-run --reps 5
python -m backend.evaluation.run_matrix --conditions C0 C1 C2
python -m backend.evaluation.analyze_v4 --run-dir backend/evaluation/results_v4/RUN_ID
python tools/check_numbers.py --run-dir backend/evaluation/results_v4/RUN_ID
```

Paid runs require explicit call/cost limits. Every run records protocol and Git
commits, package versions, JAR hash, exact returned model metadata, prompt hashes,
tokens, timings and iteration traces. Generated paper_inputs/numbers.json and
tables derive from raw cases. See docs/revision-report.md for actual execution
status: a script's presence does not establish that its experiment was run.

## Historical evidence and limitations

Retained shared results: deterministic project 31/50, compilation 41/50;
LLM 49/50 and 40/50. PURE deterministic 7/10 and 10/10; LLM 9/10 and 9/10.
The later no-repair audit compiled 12/50 shared and 2/10 PURE inputs. These are
historical v2/v3 observations, not v4 results. Original files are hash-manifested;
only verified identity redaction is permitted. Superseded environment notices
and legacy results are explained in docs/evidence-status.md.

Compilation does not establish requirement fidelity. Reference metrics cover
selected model elements, not full UML/OCL semantics. New gold models are
author-created operational references and require independent expert review.
No LLM superiority or causal component contribution is claimed without the
frozen repeated test matrix. Missing conditions are never filled with mock data.

Existing tags are preserved; this revision creates no new submission tag.
The public hosting account and Git history remain identifying. For blind review,
upload the identity-scanned export described in ARTIFACT_README.md to an
independent anonymous service. A placeholder URL does not mean a mirror exists.

## License and PURE

Original CURE code is MIT licensed; see LICENSE and NOTICE. PURE citation target:
v1.0, DOI 10.5281/zenodo.1414117; current v2.0: 10.5281/zenodo.7118517.
Both DOI registrations declare CC BY 4.0, while v2 curators disclaim knowledge
of licence agreements or intellectual property rights in source requirements.
Keep upstream attribution and disclose changes; this metadata is not clearance
of every original document. See data_pipeline/datasets/README.md. The historical consumed archive version remains NOT RECORDED. The new v4 pipeline
independently downloads the official v1 XML subset and aligns P01–P10 to
XMLZIPFile/0000 - cctns.xml, distinguishing verbatim text from paraphrases.
It produces7017 rows from18 XML documents; the retained7219-row CSV is unchanged.
The executed local384-dimensional index contains7162 chunks; see
data_pipeline/vector_db/execution_status.json. This new reconstruction does not
prove the original34268-to7219 filtering procedure.
