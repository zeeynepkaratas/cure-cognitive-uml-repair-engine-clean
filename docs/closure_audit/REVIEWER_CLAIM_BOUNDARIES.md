# Reviewer claim boundaries — project handoff only

The manuscript and publication tables were not edited. These are requirements for the next publication revision, not a declaration that referee concerns are resolved. Evidence: `INDEPENDENT_STATISTICS.json`, `SEMANTIC_CATEGORIES.json`, frozen raw cases and original protocol.

| Topic | Supported wording | Unsupported wording / required qualification |
|---|---|---|
| Main scope | 100 input cases, 2,800 case-runs, 7,936 returned calls; fixed snapshot; five LLM repetitions | 2,800 independent examples or broad external validation |
| Shared compiler | C0 12/50; C1 41/50; initial C2 49/50; revised exploratory C2 50/50; C3/C4/C7 50/50 in every rep | Critic necessary for compilation; revised C2 untouched confirmatory baseline |
| PURE | C0 already class/typed F1=1; syntax repair can preserve content; C7 typed mean 0.986667 | Semantic gain over the no-repair input on this pilot |
| Semantic means | C4 typed F1=0.960861, C7=0.941212; C4 class=1, C7=0.997222 (descriptive) | Overall C7 superiority or Critic causality inferred from architecture |
| Causal comparisons | C5 vs C6 removes lexical legacy rules within that adaptation | C6 is improved C7 without rules; C4 vs C7 isolates only Critic; C3 vs C4 isolates feedback without budget change |
| Legacy | C5 retains old prompts/control but uses cached lexical retrieval | Bit-identical FAISS/OpenAI-embedding historical replication |
| Validation | Compiler, project and Critic flags are separate; C7 acceptance is their conjunction | Semantic correctness, formal OCL solver verification, behavioural equivalence |
| Compiler audit | Selected 2,353 unique diagrams: TP1917 FP303 FN34 TN99; specificity0.246269 | Semantic-validator accuracy or general deployment error probabilities |
| F1 | Structural set agreement under a restricted parser/normalization policy | Full UML or natural-language meaning; parser completeness |
| M11_2 | Repeated Critic false acceptance is retained, open, now regression-tested | The semantic failure is fixed by a passing regression-observation test |
| Inference | Per-rep paired counts; scenario-cluster semantic bootstrap; effects/intervals and retrospective Holm sensitivity available | Pooling repeated runs as independent; calling audit-only sensitivity preregistered |
| Gold | Controlled co-constructed scenarios with pending independent experts | Expert-validated external gold or representative corpus |
| PURE corpus | v1 official XML SHA verified; 18 docs, new7017 rows /7162 chunks | Reproduced34268-to7219 historical reduction, 19 actual XML docs, ten distinct pilot documents |
| Retrieval | Online repair uses local lexical rule catalogue; BGE/FAISS document index built offline | The 384-d PURE index drove C0–C7 repair or has measured online contribution |
| License | Zenodo v1/v2 metadata declare CC BY4.0; v2 curator caveat preserved | Guaranteed original ownership/redistribution rights for every source document |
| Timing/cost | Dispatch-to-final metrics timing under six workers, caching and two JVM slots; observed usage-derived subtotal | Isolated inference latency, independent speed benchmark, complete provider invoice |
| Requests | Raw response, usage, request ID and prompt hashes retained;2500 initial prompt hashes independently match | Full raw SDK requests or verified provider honouring of the requested seed |
| Security | Versioned API SANDBOX controls tested locally; legacy research runtime trusted-only | Production secure, zero risk, fully isolated public service |
| Anonymity | Export without .git; scans performed; public history/breadcrumb linkage remains open | An anonymous repository/account or confirmed independent anonymous hosting |
| Reproduction | Clean local locked Python tests/build and live pinned JVM pass | Docker build, fresh provider API run or independent laboratory reproduction |

Before manuscript submission, publication owner must carry exploratory C2 labels into **every** derived outcome/comparison table, distinguish source scenarios and repeated runs, disclose unadjusted semantic p-values and assumptions, retain negative results, and resolve or explicitly retain OPEN referee items. No publication text was changed in this task.

Compiler matrix denominator: project flag is the test, real compiler is the comparator. Sensitivity=1917/(1917+34); specificity=99/(99+303). Among project-valid selected diagrams,303/(1917+303)=13.65% fail compilation. Among compiler-negative selected diagrams,303/402=75.37% are project false positives. Those denominators must not be interchanged. Compiler pass itself does not test SRS fidelity. Sampling includes repeated-method intermediate and reference diagrams deduplicated by exact bytes, not a random production population.
