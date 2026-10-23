# JAIDA manuscript handoff — project closure only

No manuscript, submission table, journal template or referee response was edited. `RESEARCH_ARTIFACT_CLOSED_WITH_LIMITATIONS` is a software/evidence decision, not paper acceptance or reviewer clearance. **Every new outcome/comparison table must label revised C2 POST-TEST EXPLORATORY, retain the initial shared49/50 result, and never overwrite frozen publication inputs.**

## K1–K6 disposition for the author

| Concern | Project evidence | What author must preserve / external action |
|---|---|---|
|K1 anonymity|Local scan/export tools and genuine Git verification|Public account/history and commit/source breadcrumbs are linkable; human contextual review and actual independent hosting remain pending|
|K2 claims|This handoff, claim-boundary audit and exact result manifest|Rewrite manuscript separately; unused UMLGenerator/Judge architecture must not be presented as measured online components|
|K3 controls/repetitions|C0–C7 complete, repeated LLM matrix and paired tests|No isolated Critic necessity/superiority: multiple joint changes; revised C2 exploratory|
|K4 semantics|Controlled corruptions, reference F1, missing/spurious deviations|Shared graph template/co-authored gold, near-ceiling inputs and missing independent experts limit external validity|
|K5 Critic loop|Compiler feedback, explicit exhaustion/acceptance, raw traces|M11_2 remains accepted with unsupported WeatherStation5/5; three-way gating is not semantic proof|
|K6 validity|Compiler primary for syntax, separate project/Critic/reference metrics|Selected-corpus compiler agreement is not semantic accuracy or production error rate|

## Design and all-condition summary

100 different input diagrams but70different SRS texts: shared50inputs/40SRS, PURE10/10, semantic40corruptions/20scenarios. C0–C2 once, C3–C7 five times,2,800 case-runs and7,936 returned model calls. There are not2800independentexamples. All observed model names are `gpt-4o-mini-2024-07-18`; requestedtemperature0, seed1729+rep, modernpromptv4.1 and legacyC5/C6 templates. Seed honouring/determinism is not independently verified. Dev800 and retained older/pilot runs are not extra main-test repetitions. Generation/protocolfreeze `1ead72ff7071e1f6de5867aaa250b0483d91431f`.

C0=no repair; C1=minimal deterministic; C2=extended deterministic **post-test exploratory revision**; C3=one Healer call with SRS; C4=Healer-only with feedback/up to3repairs; C5=lexical adaptation of old Critic–Healer/rules; C6=C5without rules; C7=improved Critic–Healer with SRS/rules/feedback. C3vsC4 changes feedback+budget, C4vsC7 adds Critic+rules, C7vsC6 changes several components. C5/C6 are not bit-identical historical FAISS/OpenAI-embedding workflows.

Rates below are means across repetitions; F1 uses all outputs, including noncompilers. Shared F1 is N/A because there is no independent gold. Deterministic one repetition does not estimate stochastic stability. Frozen `numbers.json` holds SD, medians, effects, compiling-only sensitivity and full paired results; this compact table must not replace them selectively.

| Dataset | Condition | Cases x reps | Compiler % mean | Project % mean | Class F1 mean | Typed relation F1 mean |
|---|---|---:|---:|---:|---:|---:|
|shared|C0|50 x 1|24.0000|0.0000|N/A|N/A|
|shared|C1|50 x 1|82.0000|62.0000|N/A|N/A|
|shared|C2 **post-test exploratory**|50 x 1|100.0000|100.0000|N/A|N/A|
|shared|C3|50 x 5|100.0000|94.0000|N/A|N/A|
|shared|C4|50 x 5|100.0000|100.0000|N/A|N/A|
|shared|C5|50 x 5|44.8000|95.2000|N/A|N/A|
|shared|C6|50 x 5|76.4000|73.6000|N/A|N/A|
|shared|C7|50 x 5|100.0000|99.6000|N/A|N/A|
|pure|C0|10 x 1|20.0000|0.0000|1.0|1.0|
|pure|C1|10 x 1|100.0000|70.0000|1.0|1.0|
|pure|C2 **post-test exploratory**|10 x 1|100.0000|100.0000|1.0|1.0|
|pure|C3|10 x 5|100.0000|100.0000|1.0|1.0|
|pure|C4|10 x 5|100.0000|100.0000|1.0|1.0|
|pure|C5|10 x 5|64.0000|80.0000|0.8400909090909091|0.8768311688311689|
|pure|C6|10 x 5|52.0000|52.0000|0.9945454545454545|0.9277887667887668|
|pure|C7|10 x 5|100.0000|100.0000|1.0|0.9866666666666667|
|semantic|C0|40 x 1|90.0000|80.0000|0.9496031746031746|0.8300595238095237|
|semantic|C1|40 x 1|100.0000|90.0000|0.9496031746031746|0.8300595238095237|
|semantic|C2 **post-test exploratory**|40 x 1|100.0000|100.0000|0.9496031746031746|0.8300595238095237|
|semantic|C3|40 x 5|100.0000|100.0000|1.0|0.9387777777777778|
|semantic|C4|40 x 5|100.0000|100.0000|1.0|0.9608611111111112|
|semantic|C5|40 x 5|64.5000|100.0000|0.7712402597402598|0.7135963203463204|
|semantic|C6|40 x 5|99.5000|100.0000|0.9927777777777778|0.8721002886002887|
|semantic|C7|40 x 5|100.0000|100.0000|0.9972222222222222|0.9412121212121212|

Initial shared C2 was49/50 compiled; revised post-test exploratory C2 is50/50. Both non-LLM run directories are retained. Shared C2/C3/C4/C7 all compile100%; Critic necessity is unproved. Semantic C4 typed F1 mean0.960861 exceeds C7's0.941212 descriptively; C4class F1=1.0 vs C7=0.997222. No overall superiority claim follows. PURE C0class/typed F1 already1.0; C7typedmean0.986667 does not show semantic gain over unchanged input.

## F1 definition and units

`backend/evaluation/reference_metrics.py` (`gold-structural-v2`) measures normalized set overlap. TP=|reference intersect prediction|, precision=TP/|prediction|, recall=TP/|reference|, F1=2PR/(P+R), or0when P+R=0. Empty prediction gives precision1only ifreferenceempty; emptyreferencegivesrecall1only ifpredictionempty; both empty primarysets giveF1=1. Attributes with no reference are separately not-applicable. Macro average is per case within rep, then rep summaries; SD of reps is distinct from per-case SD.

Class normalization splits English CamelCase/acronyms, strips punctuation/case and singularizes limited suffixes; it has no general synonym understanding. Typed edges are (normalizedsource,target,operationaltype), with selected arrow direction/whole conventions. Labels/multiplicity are excluded from primary typed F1; multiplicity-strict and attribute metrics are secondary and restricted. The frozen parser incorrectly counts `class Ghost` inside a note and omits valid `*-->`; aliases/nesting/unknownoperators are not full UML semantics. All30semantic scenarios share a four-class/four-edge template and co-constructed English SRS/gold. No natural-language/behavioural/formal-OCL correctness is established. Gold is passed only to posthoc metrics in the inspected runner; this does not demonstrate independent gold construction or unknown pretraining exclusion.

M11_2 goldhasReader/Loan/LibraryService/Book, outputalsoWeatherStation. ClassTP4, predicted5, reference4 givesprecision4/5,recall1,F1=8/9. Critic accepts 5/5 withzero repairs. Scientific error remains OPEN. Under class+typed set equality (not human semantics), C7semantic critic-true deviating outputs=53/200;143/200critic-true exact,3critic-false deviating,1critic-false exact. C7PURE has2/50accepted structural deviations. See immutable `docs/closure_audit/SEMANTIC_CATEGORIES.json` and `SEMANTIC_DEVIATIONS.csv` for each case/rep.

## Statistics and compiler audit

13 independent checks passed:1400reference-bearing primaryF1evaluations;84group summaries;312exactMcNemar/Holm comparisons;208 scenario-paired semantic comparisons;2830declared outputhashes. Wilson/McNemar use per-case/per-rep units and do not adjust source/scenario dependence. Semantic bootstrap/Wilcoxon use scenario means (20testsemanticclusters),10000draws,seed1729; original between-condition Wilcoxon p-values are unadjusted. Retrospective auditHolm sensitivity is separate, not preregistered. Report effects/intervals and assumptions, not only selected p-values. Shared repeated SRS and one-document PURE pilot further limit independence.

Selected expanded audit:2353unique bytehashes, TP1917 FP303 FN34 TN99, unavailable0. Sensitivity1917/(1917+34)=0.982573; specificity99/(99+303)=0.246269. A project-valid diagram can fail compilation:303/(1917+303). Compiler negatives falsely project-accepted:303/402. Reference/intermediate/output selection is not representative deployment sampling, and compiler agreement is not semantic accuracy. Replay reuses recorded same-JAR checks by exacthash, not2353new JVM invocations.

## PURE, retrieval, timing and rights

Official v1XMLarchive:18usable XML files; new7017rows,7162chunks,d384. None equals historical7219statements; historical34268-to7219filter remains unverified. P01–P10allderivefrom`XMLZIPFile/0000 - cctns.xml`; P02dropsopt-in qualification and is a paraphrase. Originalsourcearchive actually consumed historically is not recorded. V4 independently uses DOI10.5281/zenodo.1414117 (v1.0); v2.0DOI10.5281/zenodo.7118517 is the current recorded version. Prior official metadata declareCCBY4.0; curator underlying-rights caveat must remain. No new network/license revalidation occurred in this closure. `NOTICE` and datasetREADME preserve attribution; rootMIT does not relicense third-party text.

Offline BGE/FAISS PURE index was built but did not drive online C0–C7 repairs. Online repair uses cached lexical rule catalogue. No online document-RAG contribution is measured. No formal OCL solver runs. Six caseworkers, two compiler slots, reuse/cache contention and timing scope affect latency: dispatch-through-finalmetrics excludesqueue/serialization; repair-loop `elapsed_seconds` and dispatch `end_to_end_seconds` differ. Endpoint alias `sure_saniye` and deterministic historical `elapsed_seconds` must not be replaced by invented `processin_time_seconds`. Usage-derived cost is not a provider invoice. RequestID/rawresponses/usage/prompthashes exist; fullintermediateSDKrequestbodies BULUNAMADI.

## Table inventory — no cherry-picking

Immutable root: `backend/evaluation/results_v4/test-frozen-20261022/paper_inputs/`. `numbers.json` is the full numeric source, and each CSV has MD/TEX companions. Include all conditions/repetitions/error outcomes, distinguish all-output vs compiling-only sensitivity, and carry C2's exploratory label into **every new table**.

|CSV|Data rows|Columns|
|---|---:|---|
|`defects.csv`|1820|`dataset, condition, rep, defect_id, n, descriptive_only, compiler_pass, delta_class_f1, delta_rel_typed_f1`|
|`latency-cost-warnings.csv`|84|`dataset, condition, rep, latency, tokens_in, tokens_out, estimated_cost_usd, warnings_added, warnings_removed`|
|`mcnemar.csv`|312|`dataset, rep, a, b, field, paired_n, a_fail_b_pass, a_pass_b_fail, both_pass, both_fail, p_exact_two_sided, p_holm`|
|`outcomes.csv`|84|`dataset, condition, rep, n, compiler_pass, compiler_rate, project_pass, regressions, estimated_cost_usd`|
|`paired-semantic.csv`|208|`dataset, rep, a, b, metric, difference, n, clusters, wilcoxon_unit, mean_delta, wilcoxon_p, bootstrap_ci, bootstrap_draws, bootstrap_seed, all_zero, all_cluster_means_zero`|
|`reference-metrics.csv`|672|`dataset, condition, rep, metric, subset, n, mean, sd, median, min, max`|
|`repetitions.csv`|24|`dataset, condition, repetitions_observed, compile_rate_across_reps, class_f1_across_reps, typed_rel_f1_across_reps, output_disagreement_rate, case_disagreement_rate, per_case_disagreement`|

Figures: `compile-rate`, `critic-confusion`, `delta-f1-defect`, `iteration-trace` in `paper_inputs/figures/`; use together with denominators/caveats, not as independent evidence. Source hashes, input split/prompt hashes, old references and new handoff hashes: [FINAL_EVIDENCE_MANIFEST.json](FINAL_EVIDENCE_MANIFEST.json). Actual commands/output: [VERIFICATION_RUNS.md](VERIFICATION_RUNS.md). Expert/anonymous/container actions are pending in [EXTERNAL_ACTIONS.md](EXTERNAL_ACTIONS.md).
