# Minimum safe reviewer reproduction — existing responses only

Run from the actual repository root with Python3.12.14 (Python3.12 supported), Git, locked requirements and no model credentials. A ZIP can reproduce stored numbers, but historical ancestry is UNVERIFIABLE_FROM_ZIP; source-order verification needs the real Git checkout. `verify_v4_artifact.py` includes Git/tag checks and therefore requires a genuine checkout. Do not fabricate .git or run the complete Git-dependent verifier in a ZIP-only tree.

## Install and verify without an API

```sh
python -m venv .venv
# Activate for your OS: Windows .venv/Scripts/Activate.ps1; Linux source .venv/bin/activate
python -m pip install -r requirements.lock.txt -r requirements-dev.txt
python -m pip check
python tools/verify_v4_artifact.py --help
python tools/verify_v4_artifact.py --output docs/final_closure/reviewer-check-UNIQUE
python tools/check_numbers.py --run-dir backend/evaluation/results_v4/test-frozen-20261022
python -m pytest -q
python -m ruff check .
```

Use a NEW empty output directory. The safe entry point redirects original independent audit outputs to that directory, retains the metric/analysis implementation unchanged, verifies source/protocol/tag/protected-file preservation and makes no model calls. It refuses historical checkout output paths and nonempty output directories. The direct `check_numbers` command is read-only. Unit tests remove model credentials and prohibit network access; two compiler tests may skip without JAR/Java. Four live JVM fixtures and four local HTTP smoke checks actually passed separately in the final execution logs.

For a ZIP-only numeric check, use the read-only `check_numbers.py` command above; do not claim it proves Git provenance or rerun Git-dependent tools by manufacturing history. For deeper standalone numeric verification, a real checkout plus safe entry point is the tested path. No model-provider availability is required to recompute stored statistics. Dependencies must already exist or be installed with separately authorized package access.

Windows: remove OPENAI_API_KEY with `$env:OPENAI_API_KEY=$null`; POSIX: `unset OPENAI_API_KEY`. Configure a writable TEMP/TMP directory if needed. Set PLANTUML_JAR to your local1.2026.6binary and verify SHA256 `89948f14c93756c7a3fb7b69078ff37e8489fd79dd430c582b931e2f65358690` before live rendering. It is not bundled. API-only sandbox and English JVM locale are separate from the frozen trusted research runtime.

Never invoke historical `analyze_v4`, `run_matrix` or `finalize_v4` writers against original evidence. The finalizer was replayed on an identified copy outside the checkout: original algorithm, redirected I/O root and real-checkout Git guard; measured exact-hash compiler results reused. Computational copies are not new experiments. The two skipped optional pytest compiler tests are not evidence of live compilation; see the distinct live result JSON.

## Frontend (actually tested with a fresh npm ci)

From `frontend/`, run separately:

```sh
npm ci
npm run lint
npm run build
```

Final closure actually used `npm ci --offline --no-audit --no-fund` successfully from the lock, then lint/build. Node22.12.0 was tested. Offline install requires cached packages; no fresh-network npm install claim is made.

## Optional Docker procedure — NOT EXECUTED here

Docker executable was BULUNAMADI; container readiness remains NOT_TESTED. These are copy-ready proposed commands from repository root, not fabricated validation:

```sh
docker build -f backend/Dockerfile -t cure-v4-local .
docker run --rm -d --name cure-v4-local -p 127.0.0.1:8000:8000 cure-v4-local
docker exec cure-v4-local java -version
docker exec cure-v4-local dot -V
docker exec cure-v4-local sha256sum /opt/plantuml/plantuml.jar
curl --fail http://127.0.0.1:8000/health
curl --fail -H "Content-Type: application/json" --data '{"plantuml_kodu": "@startuml\nclass A {}\n@enduml"}' http://127.0.0.1:8000/api/render
docker stop cure-v4-local
```

Use curl.exe in Windows PowerShell if curl aliases another command; adapt JSON quoting for the shell. Confirm response compiler_valid=true and a nonempty sanitized SVG; png_is_placeholder=true is a compatibility pixel, never UMLPNGsuccess. Record actual image digest/runtime/JARhash and no credentials. Dockerfile base/OSpackages are not digest pinned, so future image bits may differ. Local API bounds are not public multi-tenant security; do not expose legacy HTTP or trusted CLI rendering publicly.

## Fresh provider experiments — NOT EXECUTED / separate authorization required

Existing results use gpt-4o-mini-2024-07-18, temperature0,requestedseed1729+rep, modernv4.1/legacyC5C6prompts. Snapshot availability and seed honouring were not queried in closure. A fresh paid replication needs explicit authorization, budget, real response traces and a NEW run ID; no model substitution or overwriting frozen runs. This guide authorizes no provider calls, new benchmark, GitHub publication or hosting.
