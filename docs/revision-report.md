# Revision report v4

## Status at the pre-LLM code freeze

The project has been revised on `revision/v4`; the manuscript has not been edited. Real non-LLM measurements are complete: two separately retained 300-case runs (C0–C2 on 100 inputs). LLM runs are authorized without a human USD ceiling, and a key is configured locally; provider availability and real experiments are still pending at this commit. Presence of code/fake-client tests is not LLM evidence. Subsequent run manifests and execution addenda must identify what actually completed.

## Measured non-LLM results

| Dataset | n | C0 compilation/project | C1 compilation/project | Initial C2 compilation/project | Revised C2 compilation/project |
|---|---:|---:|---:|---:|---:|
| Shared | 50 | 12 / 0 | 41 / 31 | 49 / 50 | 50 / 50 |
| PURE pilot | 10 | 2 / 0 | 10 / 7 | 10 / 10 | 10 / 10 |
| Semantic test | 40 | 36 / 32 | 40 / 36 | 40 / 40 | 40 / 40 |

Sources: `backend/evaluation/results_v4/nonllm-20261022/` and `nonllm-sourcefix-20261022/`, each with raw per-case JSON, aggregate JSON/CSV, immutable source/protocol identifiers and derived `paper_inputs/numbers.json`. The revised C2 is explicitly post-test/exploratory (F22); the first run is not replaced. Shared C0-vs-C1 compiler discordants are 29 gains/0 losses, exact two-sided p=3.725290298461914e-9. The revised C0-vs-C2 discordants are 38/0, p=7.275957614183426e-12; interpret this under the post-test qualification. Holm-adjusted p-values and all paired counts are in numbers.json.

Compilation is not semantic repair: mean class F1 on the 40 semantic test cases remains 0.9496031746031746 for C0, C1 and both C2 versions. Deterministic methods do not restore the injected semantic content. The curated scenarios share a graph template and await independent expert review; the relatively high starting F1 must not be presented as independent external validity.

The compiler-grounded validator audit covers 248 unique diagrams (2,656 recorded occurrences) across both new runs and four retained final result sets: TP159, FP12, FN24, TN53, sensitivity0.8688524590163934, specificity0.8153846153846154. This is operational agreement on a selected corpus, not semantic-validator accuracy. Source: `results_v4/validator-audit-20261022/audit.json`.

## Finding-by-finding changes

| Finding ID | What was wrong | What changed | Files | Tests | Evidence/number |
|---|---|---|---|---|---|
| F1 | Healer lacked SRS; unrelated rules encouraged drift | Improved English prompts include SRS; relevance guards; original prompts retained | ai_core/prompts/, ai_core/src/ai/repair_agent.py, rag/local_rules.py | test_repair_agent.py | Offline prompt/guard assertions; empirical drift reduction pending |
| F2 | Critic acceptance disagreed with compiler; no feedback | Improved acceptance requires Critic + project + compiler; real feedback and trace | repair_agent.py | valid-Critic/failed-compiler test | Empirical Critic calibration pending |
| F3 | Project-only gating and compiler regressions | Force-repair option; compiler-aware gating; raw and reverted outcomes separate | endpoints.py, repair_agent.py | test_api_safety.py, test_repair_agent.py | Reversion policy tested; new deterministic regressions0 |
| F4 | No semantic-defect benchmark | 30 explicit scenarios, 60 seeded cases, D1–D10 and combined defects | semantic_benchmark/, defect-taxonomy.md | test_semantic_benchmark.py | 20 dev / 40 test, scenario-disjoint; independent review pending |
| F5 | No simple LLM baselines/ablations or stronger deterministic baseline | Eight-condition runner and logged extended deterministic repair | run_matrix.py, repair/deterministic.py | test_run_matrix.py, test_deterministic_repair.py | C0–C2 actually measured; C3–C7 pending at freeze |
| F6 | Circular primary validity metric | Real compiler primary on syntax sets; gold metrics on semantic sets; separate rule severity audit | validator_audit.py, reference_metrics.py | test_validator_audit.py | Audit TP159/FP12/FN24/TN53 |
| F7 | Single run, missing traces/snapshot/usage/cost | Five-repetition plan, explicit snapshot, every-call metadata/timing/token trace, durable budgets and exact paired analysis | run_matrix.py, analyze_v4.py | test_run_matrix.py, test_analysis_v4.py | Repeated LLM evidence pending |
| F8 | Free relationship credit and poor source extraction | Frozen legacy reproduces S02=.25; modern proxy drops absent relation term and returns N/A if no entities; shared stop words | semantic_eval.py, entity_rules.py, docs/metrics.md | test_semantic_proxy.py | S02 modern score0, legacy.25; proxy is not semantic correctness |
| F9 | Weak reference matching; missing SD/model sizes | Explicit normalization; undirected/directed/typed/multiplicity relations, attributes, missing/spurious elements; all vs compiling-only summaries | reference_metrics.py, analyze_v4.py | test_reference_metrics.py | Derived tables include macro mean, sample SD, median and reference sizes |
| F10 | Missing raw pipeline/index and pilot provenance | Verified v1 archive; XML/HTML/Punkt processing; new CSV+document manifest; local index builder | data_pipeline/, docs/pure-pipeline-v4.md | test_pure_pipeline.py | 18 XML documents, 7017 new rows vs retained7219; index not executed |
| F11 | Per-request embedding-index rebuild with four arbitrary rules | Cached deterministic lexical fallback with catalogue/domain guards and logged rule IDs/scores | rag/local_rules.py, rules/catalogue.json | rule-cache/domain-guard tests | No embedding API calls; C5 adaptation below |
| F12 | Silent agent/API errors; unbounded requests | Explicit status/error, timeout/retry/token limits, structured decisions, stop permanent provider failures | repair_agent.py, endpoints.py | parse/API/timeout tests | Error records retained; secrets redacted |
| F13 | basarili had inconsistent meaning | Independent project/compiler/Critic fields across current endpoints and UI; deprecated aliases explained | endpoints.py, frontend/src/ | test_api_safety.py; frontend lint/build | Compiler-unavailable remains null |
| F14 | Divergent parsers, nested braces, missing operators, first-cycle-only and incorrect quantiles | Shared structured parser, all cyclic SCCs, parsed method counts, linear interpolation; legacy routes | plantuml_parser.py, ocl_validator.py, performance.py | 30+ parser tests; cycles/quantiles tests | One intentional retained-class-set difference, F19 |
| F15 | Unpinned environment, no CI/JRE, import-time log configuration, permissive CORS | Clean-env lock; pytest/offline clients; CI; JRE/Graphviz/pinned checksum installer; env origins | requirements.lock.txt, ci.yml, Dockerfile | pytest + ruff + npm lint/build | Docker build pending: Docker executable not installed locally |
| F16 | Contributor paths/names in artifact | Redaction with independent v3 numeric proof; runtime temp-path redaction; anonymous export checker | sanitize_artifact.py, verify_retained_evidence.py, export_anonymous.py | sanitizer/privacy tests | 51 protected files verified; Git hosting/history remain identifying |
| F17 | Contradictory notices/process docs and review note | English current docs, internal archive, supersession status, explicit internal-review qualification | README.md, ARTIFACT_README.md, evidence-status.md | Static checks | Protected not_run notices retained after automatic-review rejection, see below |
| F18 | Unpublished Turkish prompts | Exact original template values, English explanations/translations, current English prompts, rule/reference/split manifest | docs/supplementary/, ai_core/prompts/ | test_legacy_prompt_preservation.py | Exact v3 Critic/Healer literal hashes tested |
| F19 | Legacy class regex crosses a nameless class newline | Modern parser identifies GeneratedDiagram in shared deterministic S46; legacy {class} remains available | parser-regression-differences.md | retained120-output regression test | Only one final class-set difference; historical scores not rewritten |
| F20 | Full historical retrieval distribution cannot be replicated with a no-embedding modern matrix | C5 explicitly uses original prompt/loop plus cached lexical ranking; full old class retained separately | protocol, run manifests | legacy prompt/control tests | C5 is not a bit-identical complete v2 reproduction; limits attribution |
| F21 | Current Zenodo description and XML-subset size differ | Record exactly downloaded contents rather than infer a missing XML file | pure_archive_manifest.json, pure_manifest.csv | XML parsing test | 18 usable XML files; description says19; larger34268 collection not reproduced by subset |
| F22 | Extended repair missed a truncated relation with no source | Add conservative arrow-at-line-start removal and unit tests; retain first run and label revision exploratory | deterministic.py, protocol addendum | three missing-source-arrow tests | Initial shared C2 49/50; revised50/50; post-test change disclosed |

## Referee concerns and remaining limits

K1: content redaction and an export procedure are provided; the public account/history and linkable retained commit IDs are not anonymous. A genuinely independent anonymous upload and contextual identity review remain necessary. K2: current docs qualify claims; manuscript rewriting is deliberately outside this task. K3: infrastructure and actual non-LLM baselines are complete, real repeated LLM baselines/ablations remain pending at freeze. K4: semantic defects and structural metrics exist; independently reviewed, structurally diverse gold data remain open. K5: compiler feedback/Critic conjunction are implemented and tested, empirical effect remains unmeasured. K6: primary metrics are separated and compiler agreement audited; this does not validate natural-language semantics.

Other open items: local bge model/index execution (not installed), Docker image build (Docker unavailable), exact historical34268-to7219 filtering, full historical embedding-retrieval distribution, independent domain-expert validation and anonymous hosting. None is replaced by an invented result. Manuscript ORCIDs/contributions/funding/acknowledgements were not touched.

Automatic approval review rejected deleting the two historical not_run notices and broad rewriting of protected evidence because those conflict with retained-evidence immutability. They remain in the repository, with explicit supersession guidance, and are excluded from anonymous export. Legacy missing-value strings in protected files are likewise retained. No rejected deletion was retried through a workaround.

## Checks and provenance

Offline suite: 153 passed, two optional compiler tests skipped without runtime configuration. The two compiler smoke tests separately passed with the pinned JAR. Ruff, frontend lint and production build passed. Every derived number in both non-LLM numbers.json files is recomputed by `tools/check_numbers.py`; output hashes cover raw and generated files. The original PURE CSV content is unchanged. `docs/retained-evidence-verification-v4.json` independently verifies JSON numeric/boolean/null values and numeric CSV cells against the v3 baseline. The A1 verification file is the historical stage log, not a claim that its stage-specific hashes describe all later source/doc edits.

Pinned PlantUML1.2026.6 SHA-256:89948F14C93756C7A3FB7B69078FF37E8489FD79DD430C582B931E2F65358690. PURE XML ZIP SHA-256:8b0a36ac34f806d16c0c13d4b28a92b10e3fb353739025b068249b2de95fbbdb. Initial protocol commit0918c974ff8f8d01f82061655096da9be150452b; F22 protocol addendum/code commit5a9a79b7ec7b7ca9687d32ed6adadef173d188c3. No earlier tag was moved and no new submission tag is created by this revision.

## F23 — pilot observability correction

The first development provider pilot completed two case-runs with eight model calls, using the exact requested snapshot. C3 compiled/project-passed in6.516176200006157s (one call); C7 compiled/project-passed in13.292226699995808s (seven calls), but its final Critic verdict remained false and the repair budget was exhausted. This is a single-case pilot, not performance evidence. Its original trace lacked the Critic response text/error list, so the reason for that rejection is NOT RECORDED. Before the full development matrix, raw response text and Critic findings/categories were added to every call trace and tested. No prompt or rule was tuned from this pilot, and its records are retained separately. The anonymous export scanner also excludes the generic Git author label “CURE Team” from human-identity patterns; no contributor identity is thereby whitelisted.

## F24 — development-only prompt clarification

New explicit v4.1 English templates clarify generic PlantUML endpoint multiplicities and composition, avoid redundant inverse associations, distinguish advisory warnings and require source evidence before accepting a Critic suggestion. This responds to measured development-only semantic drift; no held-out LLM test has run. Original v4 templates and all tuning-run outputs are retained. Modern Healer prompts remain common across C3/C4/C7. The explicit revision is recorded in runner configuration; resume now rejects changes to split/selection/repetitions/revision, and combined analysis rejects mismatched prompt hashes/models/seeds as well as protocols/inputs.
