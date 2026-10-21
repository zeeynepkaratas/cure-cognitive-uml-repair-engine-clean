# Evaluation protocol v4 — frozen before test-split LLM execution

This protocol is committed before new test-split LLM calls. Its Git commit and SHA-256 are recorded in every run manifest. No v4 test-split LLM experiment has run at this point. No result-driven prompt/rule tuning is permitted. Any development changes require a new protocol revision and new run identifiers before testing.

## Hypotheses and scope

H1: repair improves real compilation over no repair on the syntactic shared/PURE sets. H2: the improved loop may improve gold-model structural F1 and delta-F1 over simple alternatives on semantic defects. H2 is an empirical hypothesis, not a promised result. Negative or equivalent outcomes must be reported. No claim of formal OCL verification, independent expert-validated gold semantics, component superiority or general semantic correctness is permitted from project validation alone.

## Inputs and split

Shared S01–S50 and PURE P01–P10 are test only, retained unchanged. New semantic scenarios M01–M10 (20 cases) are development only; M11–M30 (40 cases) are test only. Splits are scenario-disjoint and frozen in semantic_benchmark/split.json. The test matrix has 100 cases per condition/repetition. The semantic set is a curated controlled benchmark with a shared graph template, English construction bias and pending independent expert review. Its first ten development scenarios are PURE-inspired extensions, not external PURE gold labels. The PURE pilot references remain manually curated.

## Conditions

| ID | Condition | Maximum model calls, before retries |
|---|---|---:|
| C0 | Unchanged input | 0 |
| C1 | Original deterministic minimal repair | 0 |
| C2 | Extended deterministic structural repair, without SRS or gold oracle | 0 |
| C3 | Single Healer call with SRS; no Critic/rules/compiler feedback | 1 |
| C4 | Healer only, SRS and real project/compiler feedback, up to three repairs | 3 |
| C5 | Legacy Critic–Healer prompts and early-acceptance control flow, original four domain rules | 7 |
| C6 | C5 without retrieved rules | 7 |
| C7 | Improved Critic–Healer with guarded local rules, SRS and real validator/compiler feedback | 7 |

C5 adaptation: the instrumented matrix uses deterministic cached lexical ranking of the four original rules. Original FAISS/OpenAI-embedding behaviour remains reachable in the explicit legacy class, but is not automatically invoked by the matrix. C5 therefore reproduces original prompt text and loop logic, not the full historical retrieval distribution. This limits the interpretation of C5-vs-C7 and historical comparisons. C6 shares the same instrumentation. No hidden embedding API calls occur in the matrix.

All LLM cases are forced through their assigned condition, including already-compiling semantic inputs. C5/C6 keep legacy Critic-only stopping. C7 accepts only Critic + project + compiler validity. Single-pass and Healer-only acceptance uses project + compiler validity. Raw final output is the primary experimental observation. Reverting a compiler regression to the original input is a separate reported policy; API users receive that safe policy. Both raw and reverted diagrams/metrics are preserved.

## Models, repetition, budget and environment

Default explicit snapshot for both roles: gpt-4o-mini-2024-07-18; temperature 0, seed 1729 + repetition index (1–5), max completion tokens 2048, timeout 45 seconds, two retries with bounded exponential backoff. The snapshot is marked deprecated in current official documentation: availability must be checked by an authorized run, and failure must be recorded. No automatic alias/model substitution is permitted. Distinct role models are configurable in the agent; the matrix currently enforces gpt-4o-mini pricing bounds.

Run five LLM repetitions; deterministic conditions run once. Maximum test API attempts including retries: 37,500 across C3–C7; development maximum: 7,500. These are conservative upper bounds, not estimated actual usage. A human USD budget and local OPENAI_API_KEY are required. Budget reservation happens before dispatch and is persisted; UTF-8 byte upper bounds plus 4096 framing/schema tokens and the output token cap use $0.15 input / $0.60 output per million tokens (official model page checked 2026-10-22). Reservations are conservative and never refunded. Billing is estimated from returned usage and reported separately. No paid run is authorized without an explicit positive call and USD cap.

PlantUML 1.2026.6 SHA-256: 89948F14C93756C7A3FB7B69078FF37E8489FD79DD430C582B931E2F65358690. The same local Java/JAR -tsvg -checkonly file invocation is used for every unique diagram. Repeated identical diagrams may reuse a process-local compiler check, explicitly recorded. Repair-loop timing includes its validation requests and cache reuse; it is not a clean isolated model-inference latency estimate. Package versions, platform, prompt hashes, input hashes, model metadata, request identifiers, usage, traces and output hashes are recorded. Compiler unavailability is null and must not count as a pass.

## Outcomes and statistics

Primary syntactic outcome: real compiler pass. Primary semantic outcomes: class F1 and directed typed-relationship F1, plus paired output-minus-input delta-F1. Also report undirected and directed endpoints, multiplicity-strict relationships and attributes, reference sizes, missing/spurious elements, normalized-name collisions and macro mean/sample SD/median, with all outputs and compiling outputs separately. The versioned normalization policy is in reference_metrics.py; source heuristic scores are secondary structural proxies only.

Report Wilson 95% intervals, exact two-sided McNemar discordant counts for each condition vs C0 and C7 vs C1–C5 (no pseudo-replication). Pair by case within each repetition; replicate the deterministic outcome for pairing only, never treat it as independent repeated evidence. Holm correction is across all pre-specified comparisons within a dataset/repetition. Report each repetition's result and mean/sample SD, per-case run disagreement. Use paired Wilcoxon for delta-F1 and scenario-cluster paired bootstrap intervals (seed 1729, 10,000 draws); report degenerate all-zero differences explicitly. Defect-group cells with n < 10 are descriptive only. Report API/parse/timeout failures separately, budget-stopped incomplete cases separately, compiler regressions, three-way Critic/compiler/project counts, exhaustion, first-valid iteration, timing mean/median/P95 using linear interpolation, tokens and usage-derived cost. Missing usage remains unknown, not zero.

## Inclusion, failures and reporting

Retain every attempt, including unsuccessful model/API calls. No selective retries across run IDs or output-based exclusions. Finished errored cases are not silently re-run by resume. Budget interruption produces an explicit incomplete record and must not be presented as a completed five-repetition experiment. Resume requires matching code/protocol/prompt/model/input configuration. Compiler failures remain in primary semantic averages; a compiling-only sensitivity table is additional. Never fill missing paid runs with retained v2 outputs, fake models or zeros.

## Release and manuscript handoff

Historical results retain their v2/v3 identifiers. The intended future paper artifact is the fully audited v4 commit after actual experiment completion; no v4 tag is created here. The revision report records the current code/protocol commit and execution status. A final immutable tag must be chosen after remaining experiments and independent checks, without moving earlier tags. The manuscript is outside this revision task.
