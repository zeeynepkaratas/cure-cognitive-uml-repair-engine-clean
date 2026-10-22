# Revision report v4

## Completed frozen evaluation

The manuscript has not been edited. All2800 registered main-test case-runs completed: C0–C2 once on100 cases, C3–C7 five times on the same100 cases. The100 inputs comprise50 shared,10 PURE and40 semantic test cases. The800 development case-runs, two-case provider pilot and both earlier300-case non-LLM runs are also retained separately (4202 recorded case-runs in total, not a pooled independent sample). No finished failed case was selectively retried.

Generation code and protocol were frozen at1ead72ff7071e1f6de5867aaa250b0483d91431f before the main test. The final English revision is v4.1; legacy C5/C6 prompts remain unchanged. Subsequent changes were analysis/documentation/index publication only. tools/finalize_v4.py verified every registered condition/case/repetition, raw hashes, unchanged generation/validator sources and independent recomputation of all derived numbers.

Main-test agent-error cases: 0. Returned model observations: {'gpt-4o-mini-2024-07-18': 7936}. The exact per-call responses, usage, request metadata, seed, timings and intermediate diagrams are preserved.

| Dataset | Condition | Cases per repetition | Repetitions | Compiler % mean +/- SD | Project % mean +/- SD | Class F1 mean +/- SD | Typed rel F1 mean +/- SD | End-to-end seconds mean | Agent-error cases |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| shared | C0 | 50 | 1 | 24.0000 +/- 0.0000 | 0.0000 +/- 0.0000 | N/A | N/A | 0.0115 | 0 |
| shared | C1 | 50 | 1 | 82.0000 +/- 0.0000 | 62.0000 +/- 0.0000 | N/A | N/A | 0.3970 | 0 |
| shared | C2 | 50 | 1 | 100.0000 +/- 0.0000 | 100.0000 +/- 0.0000 | N/A | N/A | 0.5435 | 0 |
| shared | C3 | 50 | 5 | 100.0000 +/- 0.0000 | 94.0000 +/- 0.0000 | N/A | N/A | 1.8916 | 0 |
| shared | C4 | 50 | 5 | 100.0000 +/- 0.0000 | 100.0000 +/- 0.0000 | N/A | N/A | 1.7625 | 0 |
| shared | C5 | 50 | 5 | 44.8000 +/- 5.0200 | 95.2000 +/- 2.2804 | N/A | N/A | 15.0282 | 0 |
| shared | C6 | 50 | 5 | 76.4000 +/- 1.6733 | 73.6000 +/- 2.1909 | N/A | N/A | 4.6569 | 0 |
| shared | C7 | 50 | 5 | 100.0000 +/- 0.0000 | 99.6000 +/- 0.8944 | N/A | N/A | 5.3246 | 0 |
| pure | C0 | 10 | 1 | 20.0000 +/- 0.0000 | 0.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 0.0038 | 0 |
| pure | C1 | 10 | 1 | 100.0000 +/- 0.0000 | 70.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 0.3375 | 0 |
| pure | C2 | 10 | 1 | 100.0000 +/- 0.0000 | 100.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 0.6392 | 0 |
| pure | C3 | 10 | 5 | 100.0000 +/- 0.0000 | 100.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 2.0808 | 0 |
| pure | C4 | 10 | 5 | 100.0000 +/- 0.0000 | 100.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 2.0174 | 0 |
| pure | C5 | 10 | 5 | 64.0000 +/- 11.4018 | 80.0000 +/- 0.0000 | 0.8401 +/- 0.0187 | 0.8768 +/- 0.0175 | 16.7762 | 0 |
| pure | C6 | 10 | 5 | 52.0000 +/- 8.3666 | 52.0000 +/- 8.3666 | 0.9945 +/- 0.0122 | 0.9278 +/- 0.0153 | 5.6306 | 0 |
| pure | C7 | 10 | 5 | 100.0000 +/- 0.0000 | 100.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 0.9867 +/- 0.0183 | 4.7510 | 0 |
| semantic | C0 | 40 | 1 | 90.0000 +/- 0.0000 | 80.0000 +/- 0.0000 | 0.9496 +/- 0.0000 | 0.8301 +/- 0.0000 | 0.0316 | 0 |
| semantic | C1 | 40 | 1 | 100.0000 +/- 0.0000 | 90.0000 +/- 0.0000 | 0.9496 +/- 0.0000 | 0.8301 +/- 0.0000 | 0.1321 | 0 |
| semantic | C2 | 40 | 1 | 100.0000 +/- 0.0000 | 100.0000 +/- 0.0000 | 0.9496 +/- 0.0000 | 0.8301 +/- 0.0000 | 0.3509 | 0 |
| semantic | C3 | 40 | 5 | 100.0000 +/- 0.0000 | 100.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 0.9388 +/- 0.0116 | 3.0844 | 0 |
| semantic | C4 | 40 | 5 | 100.0000 +/- 0.0000 | 100.0000 +/- 0.0000 | 1.0000 +/- 0.0000 | 0.9609 +/- 0.0080 | 3.0209 | 0 |
| semantic | C5 | 40 | 5 | 64.5000 +/- 4.1079 | 100.0000 +/- 0.0000 | 0.7712 +/- 0.0059 | 0.7136 +/- 0.0060 | 20.5718 | 0 |
| semantic | C6 | 40 | 5 | 99.5000 +/- 1.1180 | 100.0000 +/- 0.0000 | 0.9928 +/- 0.0058 | 0.8721 +/- 0.0157 | 14.2930 | 0 |
| semantic | C7 | 40 | 5 | 100.0000 +/- 0.0000 | 100.0000 +/- 0.0000 | 0.9972 +/- 0.0000 | 0.9412 +/- 0.0138 | 6.2640 | 0 |

Rates and F1 in this table summarize repetitions, not pooled independent case-runs. All-output metrics include non-compiling diagrams. Compiling-only metrics, per-case missing/spurious elements, reference sizes, defect-group summaries, iteration counts, regressions, exhaustion, per-repetition paired exact McNemar/Holm and scenario-cluster Wilcoxon/bootstrap results are in paper_inputs/numbers.json and tables/. Zero SD for deterministic methods reflects one observed repetition, not estimated stochastic stability. Shared class/relationship F1 is N/A because the S-set has no independent gold diagram.

The final compiler-agreement audit covers2353 unique diagram hashes: TP1917, FP303, FN34, TN99, unavailable0, sensitivity0.9825730394669401, specificity0.2462686567164179. It includes retained outputs, all new inputs/final/intermediate diagrams and reference models. Exact-hash compiler measurements from the same pinned JAR were reused with provenance; missing/conflicting checks were compiled afresh. This is agreement on a selected corpus, not semantic-validator accuracy. Source: validator-audit-final-20261022/audit.json and finalization.json.

Usage-derived main-test estimate: {"attempts": 7936, "caveat": "Subtotal excludes unknown provider usage; not a complete bill. Includes incomplete rows present in results.json; archived attempts reported separately.", "estimated_known_usage_subtotal_usd": 0.8116431, "known_usage_attempts": 7936, "unknown_usage_attempts": 0}. Archived partial-attempt usage is separately recorded in finalization.json; it is not silently dropped. Provider invoices may differ from these estimates.

Observed semantic-test means: C3 class F1=1.0000, typed relationship F1=0.9388; C4 class F1=1.0000, typed relationship F1=0.9609; C7 class F1=0.9972, typed relationship F1=0.9412. C7 does not have the highest observed class or typed-relationship F1: C4 has the highest typed-relationship mean among these modern LLM conditions. This is a descriptive comparison; use the paired tables for inference. C2, C3, C4 and C7 all compile every main-test output. A Critic is therefore not shown necessary for compilation on this benchmark.

On PURE, structured reference F1 is already1.0 in C0 despite syntax defects. C1/C2/C3/C4 preserve that model agreement, while C7 typed-relationship F1 averages0.9866666666666667. Repair can therefore preserve or degrade content; compilation gains alone cannot support semantic superiority. C5 is the disclosed lexical adaptation of legacy prompt/control flow, not a bit-identical historical replication.

No overall superiority or isolated causal contribution is inferred from a multi-agent design. The per-repetition paired comparisons must support any claim. C7 changes several components jointly; C3-vs-C4 changes feedback and repair budget, and C4-vs-C7 adds Critic/rules together. The C5-vs-C6 rule ablation applies to the legacy lexical adaptation. Structural model agreement does not establish natural-language semantic correctness.

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
| F1 | Healer lacked SRS; unrelated rules encouraged drift | Improved English prompts include SRS; relevance guards; original prompts retained | ai_core/prompts/, ai_core/src/ai/repair_agent.py, rag/local_rules.py | test_repair_agent.py | Five-repetition semantic/PURE metrics in the completed main matrix; no universal drift-reduction claim |
| F2 | Critic acceptance disagreed with compiler; no feedback | Improved acceptance requires Critic + project + compiler; real feedback and trace | repair_agent.py | valid-Critic/failed-compiler test | Observed three-way Critic/compiler/project counts and acceptance/exhaustion in main numbers.json |
| F3 | Project-only gating and compiler regressions | Force-repair option; compiler-aware gating; raw and reverted outcomes separate | endpoints.py, repair_agent.py | test_api_safety.py, test_repair_agent.py | Reversion policy tested; new deterministic regressions0 |
| F4 | No semantic-defect benchmark | 30 explicit scenarios, 60 seeded cases, D1–D10 and combined defects | semantic_benchmark/, defect-taxonomy.md | test_semantic_benchmark.py | 20 dev / 40 test, scenario-disjoint; independent review pending |
| F5 | No simple LLM baselines/ablations or stronger deterministic baseline | Eight-condition runner and logged extended deterministic repair | run_matrix.py, repair/deterministic.py | test_run_matrix.py, test_deterministic_repair.py | All C0–C7 completed,2800 main case-runs |
| F6 | Circular primary validity metric | Real compiler primary on syntax sets; gold metrics on semantic sets; separate rule severity audit | validator_audit.py, reference_metrics.py | test_validator_audit.py | Initial audit below retained; expanded final unique-diagram audit in completed evaluation section |
| F7 | Single run, missing traces/snapshot/usage/cost | Five-repetition plan, explicit snapshot, every-call metadata/timing/token trace, durable budgets and exact paired analysis | run_matrix.py, analyze_v4.py | test_run_matrix.py, test_analysis_v4.py | Five repetitions per LLM condition, all raw traces/metadata/usage retained |
| F8 | Free relationship credit and poor source extraction | Frozen legacy reproduces S02=.25; modern proxy drops absent relation term and returns N/A if no entities; shared stop words | semantic_eval.py, entity_rules.py, docs/metrics.md | test_semantic_proxy.py | S02 modern score0, legacy.25; proxy is not semantic correctness |
| F9 | Weak reference matching; missing SD/model sizes | Explicit normalization; undirected/directed/typed/multiplicity relations, attributes, missing/spurious elements; all vs compiling-only summaries | reference_metrics.py, analyze_v4.py | test_reference_metrics.py | Derived tables include macro mean, sample SD, median and reference sizes |
| F10 | Missing raw pipeline/index and pilot provenance | Verified v1 archive; XML/HTML/Punkt processing; new CSV+document manifest; local index builder | data_pipeline/, docs/pure-pipeline-v4.md | test_pure_pipeline.py | 18 XML documents, 7017 new rows vs retained7219; executed7162-chunk384-d index (F26) |
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

| F23 | Pilot lacked Critic rejection details | Raw responses and Critic findings retained before full development | repair_agent.py | raw-trace tests | Original pilot retained without invented rationale |
| F24 | Critic invented composition/inverse demands on dev | Generic notation/source-grounding revision, selected only on dev | prompts/v4.1/, development-prompt-selection-v4.json | template-preservation tests | All800 tuning case-runs retained; no test-driven prompt tuning |
| F25 | Unsafe concurrent budget and ambiguous overall acceptance | Bounded workers, locked reservations, client cleanup, complete failure traces, accepted termination required | run_matrix.py, endpoints.py, RepairPage.jsx | concurrency/resume/API tests | Complete registered matrix verified; raw regression and reversion separate |
| F26 | Missing executed index and limited presentation | CPU FAISS build, paired/repetition metrics, actual figures, complete-matrix and measured-cache audit | finalize_v4.py, analyze_v4.py, validator_audit.py | coverage/audit/analysis tests |7162 chunks,d384; every final number independently recomputed |

| F27 | Improved Critic still accepts a source-unrelated class | Record the held-out failure; no post-test prompt tuning or selective retry | test-frozen-20261022/cases/C7_M11_2_1.json through repetition5 | Actual frozen model observations | WeatherStation retained and Critic-valid in5/5 M11_2 runs; class F1=0.888888888888889 for those outputs |

## Referee concerns and remaining limits

K1: content redaction and an export procedure are provided; the public account/history and linkable retained commit IDs are not anonymous. A genuinely independent anonymous upload and contextual identity review remain necessary. K2: current docs qualify claims; manuscript rewriting is deliberately outside this task. K3: all requested C0–C7 baselines/ablations and five LLM repetitions completed; interpretation remains limited by joint component changes and the benchmark design. K4: semantic defects and structural metrics exist; independently reviewed, structurally diverse gold data remain open. K5: compiler feedback/Critic conjunction are implemented, tested and evaluated in the repeated matrix; individual causal effects are not fully isolated. K6: primary metrics are separated and compiler agreement audited; this does not validate natural-language semantics.

Other open items: Docker image build (Docker unavailable), exact historical34268-to7219 filtering, full historical embedding-retrieval distribution, independent domain-expert validation and anonymous hosting. None is replaced by an invented result. Manuscript ORCIDs/contributions/funding/acknowledgements were not touched.

Automatic approval review rejected deleting the two historical not_run notices and broad rewriting of protected evidence because those conflict with retained-evidence immutability. They remain in the repository, with explicit supersession guidance, and are excluded from anonymous export. Legacy missing-value strings in protected files are likewise retained. No rejected deletion was retried through a workaround.

## Checks and provenance

Offline suite:164passed, two optional compiler tests skipped without runtime configuration. The two compiler smoke tests separately passed with the pinned JAR. Ruff, frontend lint and production build passed. Every derived number in both non-LLM numbers.json files is recomputed by `tools/check_numbers.py`; output hashes cover raw and generated files. The original PURE CSV content is unchanged. `docs/retained-evidence-verification-v4.json` independently verifies JSON numeric/boolean/null values and numeric CSV cells against the v3 baseline. The A1 verification file is the historical stage log, not a claim that its stage-specific hashes describe all later source/doc edits.

Pinned PlantUML1.2026.6 SHA-256:89948F14C93756C7A3FB7B69078FF37E8489FD79DD430C582B931E2F65358690. PURE XML ZIP SHA-256:8b0a36ac34f806d16c0c13d4b28a92b10e3fb353739025b068249b2de95fbbdb. Initial protocol commit0918c974ff8f8d01f82061655096da9be150452b; F22 protocol addendum/code commit5a9a79b7ec7b7ca9687d32ed6adadef173d188c3. No earlier tag was moved and no new submission tag is created by this revision.

## F23 — pilot observability correction

The first development provider pilot completed two case-runs with eight model calls, using the exact requested snapshot. C3 compiled/project-passed in6.516176200006157s (one call); C7 compiled/project-passed in13.292226699995808s (seven calls), but its final Critic verdict remained false and the repair budget was exhausted. This is a single-case pilot, not performance evidence. Its original trace lacked the Critic response text/error list, so the reason for that rejection is NOT RECORDED. Before the full development matrix, raw response text and Critic findings/categories were added to every call trace and tested. No prompt or rule was tuned from this pilot, and its records are retained separately. The anonymous export scanner also excludes the generic Git author label “CURE Team” from human-identity patterns; no contributor identity is thereby whitelisted.

## F24 — development-only prompt clarification

New explicit v4.1 English templates clarify generic PlantUML endpoint multiplicities and composition, avoid redundant inverse associations, distinguish advisory warnings and require source evidence before accepting a Critic suggestion. This responds to measured development-only semantic drift; no held-out LLM test has run. Original v4 templates and all tuning-run outputs are retained. Modern Healer prompts remain common across C3/C4/C7. The explicit revision is recorded in runner configuration; resume now rejects changes to split/selection/repetitions/revision, and combined analysis rejects mismatched prompt hashes/models/seeds as well as protocols/inputs.

## F25 — final prompt selection and safe concurrent execution

All800 development case-runs are preserved. The final v4.1 selection record explicitly discloses connection failures and does not claim a causal improvement. The runner now uses bounded case concurrency, a two-process compiler semaphore, atomic thread-safe budget reservations, reproducible randomized task order and per-case SDK connection reuse/cleanup. Worker failures retain in-flight outputs and separate error records. End-to-end timing is separate from repair-loop timing. Resume preserves completed errored cases and archives incomplete budget traces. The API/UI overall acceptance now requires an accepted termination as well as compiler/project validity, avoiding a success indication when the Critic still rejects a compiled candidate. Offline tests cover concurrent budget contention, task completeness, resume, failure preservation and retained-evidence path protection.

## F26 — completed local index and analysis presentation

The CPU bge-small-en-v1.5 build completed at immutable model revision5c38ec7c405ec4b44b94cc5a9bb96e735b38267a. The7017-row source CSV produced7162 overlapping chunks and a persisted384-dimensional FAISS index. Source/output hashes and the separate package lock are published. The index was loaded and its dimension/count/normalized-vector self-similarity verified. No embedding API was used, and this document index is not claimed as the rule retriever used in C0–C7.

The analysis now handles development runs without C0, reports paired between-condition semantic differences in addition to delta-vs-input, semantic mean/SD across repetitions and output-hash disagreement. Known-usage cost subtotals preserve unknown-usage counts. Compiler/defect/Critic/iteration figures show actual bars/heatmaps rather than text lists. All-zero scenario means receive a defined Wilcoxon p=1 rather than NaN, including opposing within-scenario case differences. These are analysis-only changes; generation code/prompts remain frozen at1ead72ff7071e1f6de5867aaa250b0483d91431f during the main test.

The local CPU index build overlapped the first2.6 minutes of the main test (index manifest timestamp14:29:24UTC; main start14:26:46UTC). Conditions were assigned in seeded shuffled order. Timing remains a contended local measurement, not isolated model-inference latency; this does not change the compiler/gold-metric definitions.

## Observed held-out semantic failure (F27)

In M11_2 the SRS/gold contains Reader, Loan, LibraryService and Book. C7 retains the injected WeatherStation class in all five repetitions and the Critic accepts each candidate. Precision4/5, recall4/4 and class F1=8/9. This is a concrete false acceptance against the operational gold; compiler validity does not repair it. C3/C4 remove the spurious class. No generation rule or prompt was changed after observing this failure. This open model-behaviour limit must not be described as fully solved.

## Publication status

Existing tags remain unchanged. No new submission tag is created; the manuscript author should tag the final verified publication commit after selecting its citation. The generation freeze and retained historical result/run commits remain distinguishable from later analysis/publication commits. The anonymous export is created with tools/export_anonymous.py; public hosting/history and linkable commit IDs still require independent anonymous hosting and contextual review. No promise of zero risk or immunity to referee criticism is made.
