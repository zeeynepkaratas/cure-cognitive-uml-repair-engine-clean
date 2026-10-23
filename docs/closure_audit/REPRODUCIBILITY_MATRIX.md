# Reproducibility matrix

Commands below start at the genuine repository root. Audit only consumes existing responses. `RUN_CHECKS.txt` records executed outcomes; future/provider/container commands are instructions, not claims they were executed here. Do not rerun writers in historical evidence directories.

## Dependencies and clean environment

Python3.12.14; `requirements.lock.txt` plus `requirements-dev.txt` pinned and actually installed into a fresh environment. Separate `requirements-index.lock.txt` is for offline BGE index rebuilding, not needed for main result analysis. Node/package-lock exact dependency resolution retained, Node/Java versions and lock hashes in `RUNTIME_INVENTORY.json`. External JAR1.2026.6 checksum in `LIVE_RUNTIME_CHECKS.json`. Docker and standalone Graphviz executable on PATH: **BULUNAMADI** in this environment. Successful live class-diagram checks do not prove arbitrary layouts or container portability.

```powershell
python -m venv ../closure-clean-env
../closure-clean-env/Scripts/python.exe -m pip --isolated install --index-url https://pypi.org/simple -r requirements.lock.txt -r requirements-dev.txt
$env:OPENAI_API_KEY=$null
$env:TEMP=(Resolve-Path '../closure-temp').Path
$env:TMP=$env:TEMP
../closure-clean-env/Scripts/python.exe -m pip check
../closure-clean-env/Scripts/python.exe -m pytest -q
../closure-clean-env/Scripts/python.exe -m ruff check .
# From frontend/: npm ci ; npm run lint ; npm run build (run separately)
```

Actual fresh Python install/check/tests passed. Frontend lint/build ran on the existing dependency tree; fresh `npm ci` was not claimed. Linux/Windows temp permissions and Java execution restrictions differ: sandboxed Java can hang; successful live checks used an authorized local JVM environment with a dedicated temporary directory. No timeout was counted as pass.

## Experimental claims and exact evidence path

| Claim / artifact | Read-only command or procedure | Units / fixed settings | Actual verification and limits |
|---|---|---|---|
| Complete main design, every field/hash | `python tools/closure_audit_v4.py` | S50/P10/Mtest40, C0–C2 once; C3–C7 reps1–5 |13 checks pass,2800 records;100 different inputs,70SRS; no independent replication |
| All derived figures/tables/numbers | `python tools/check_numbers.py --run-dir backend/evaluation/results_v4/test-frozen-20261022` | Immutable raw rows and `paper_inputs/numbers.json` |Recomputation passed2800; raw flags are not all recompiled here |
| Primary class/typed F1 | independent `tools/closure_audit_v4.py` |gold-structural-v2, English normalization, both-emptysetsF1=1; all and compiling subsets |1400 reparses match; narrow fixture parser, secondary attribute/multiplicity semantics not independently reparsed |
| McNemar/Holm |same independent script |paircasewithinrep; deterministicrow reused only for pairing; family dataset/rep |312 comparisons; gains/losses/effectdiff included; source clustering assumptions remain |
| Wilcoxon/bootstrap |same script |scenario mean pairs;10000draws,seed1729,20semantic test clusters |208 contrasts, numerical tolerance2e-12; original semantic p-values unadjusted, retrospective Holm column separate |
| Semantic false acceptance and deviations |`python tools/closure_evidence_v4.py`; `pytest -q tests/test_closure_regressions.py` |exactclass+typed sets, Criticnull separate |CSV every deviation; M11_2 failure5/5 preserved, no human semantic truth inferred |
| True compiler audit |read `results_v4/validator-audit-final-20261022/audit.json` and independent recount |2353uniquehashes; selected retained/input/intermediate/gold corpus |TP1917 FP303 FN34 TN99; measured same-JAR checks reused, not2353new subprocesses in closure |
| Original finalizer |copy run into a **new** temporary results_v4 directory, invoke `python tools/finalize_v4.py --help`, use `--run-dir` and `--audit-dir` from help |sourcefreeze1ead..., exactrawcopy |Actually replayed successfully before guard edit; copy/audit moved outside repository; see REPLAY_FINALIZATION.json. Never run against protected original |
| Retained v2/v3 neutrality |`python tools/verify_retained_evidence.py --output docs/closure_audit/RETAINED_NUMERIC_NEUTRALITY.json` |originalPUREcontent plus51protectedretainedfiles |PASS; independent preaudit4660file snapshot also unchanged |
| Source/protocol/ancestry |`python tools/closure_evidence_v4.py`; `git merge-base --is-ancestor COMMIT BASE` |actual.git, no invented history |all required old/freeze/final commits ancestral; ZIP-onlyUNVERIFIABLE_FROM_ZIP; recorded clocks not external proof |
| Prompt provenance |compare initial templates +SRS/input/initialvalidator/ruleIDs to tracehash |v4.1modern,C5/C6legacy; all2500LLMcase-runs |2500initialhashmatches; raw intermediate SDKrequest bodies BULUNAMADI |
| Live compiler and HTTP |set pinnedPLANTUML_JAR; `python tools/closure_live_checks.py` |sameJAR; API-onlySANDBOX+JVMlocaleEnglish |4compilerfixtures+4localHTTPchecks pass; newAPIprofileisnotfrozenresearchruntime; no provider calls |
| Offline PUREpipeline/index |commands in `docs/pure-pipeline-v4.md`; verify archive+CSV+index hashes |DOIv1,18XML,new7017rows,7162chunks,d384,BGErevision5c38... |existingbuiltindex preserved; did not redownloadmodel/rebuild during closure; historical7219filter OPEN |
| License/provenance |GET `https://zenodo.org/api/records/1414117` and `/7118517`; compare `data_pipeline/datasets/pure_archive_manifest.json` |v1.0/v2.0,CCBY4.0,officialarchiveMD5 |API metadata verified during closure; v2page timeout was not a metadata failure; curator rights caveat remains |
| Anonymous export |`python tools/export_anonymous.py --output ../cure-closure-audit-anonymous.zip` from staged actual checkout; `python tools/closure_zip_audit.py ../cure-closure-audit-anonymous.zip --output ../closure-logs/zip-final.json` |trackedexport excludes.git,internalnotes,secrets; independentpypdf6.10.0 |local ZIP only; contextual/human review+independenthosting OPEN; no proof of unlinkability |
| Container |`docker build -f backend/Dockerfile -t cure-closure .` |JRE/Graphviz/pinnedJAR,Pythonlock |NOT TESTABLE:Docker BULUNAMADI; instruction only |
| Provider replay |**not executed**; checkout originalfreeze and choose a NEW run directory, command below |exactsnapshot,temp0,seed1729+rep,max2048,timeout45,retries2,workers6 |same responses not guaranteed; seed request !=determinism; explicit fresh authorization/budget needed |

The finalizer CLI is verified from its source/help; its replay source list includes the computational copy. Copies are never counted as experiments. New guard now covers runner and all agent/validator dependencies; runtime-only API changes are outside that frozen path list.

## Preserved historical vs exploratory C2

|Dataset|C0 compiler/project|C1 compiler/project|Initial C2 compiler/project|Revised C2 compiler/project — **post-test exploratory**|
|---|---|---|---|---|
|Shared50|12/0|41/31|49/50|50/50|
|PURE10|2/0|10/7|10/10|10/10|
|Semantic40|36/32|40/36|40/40|40/40|

Raw roots `nonllm-20261022`, `nonllm-sourcefix-20261022`, and main test are separate. Source missing-arrow S33 fix followed the first non-LLM test, before paid LLM evaluation. The main C2 uses that revised baseline. Frozen publication input tables retain this value without the qualification in each row: **PARTIAL; publication owner must fix future presentation, not rewrite history**.

## Future provider command — NOT RUN in closure

Original source freeze `1ead72ff7071e1f6de5867aaa250b0483d91431f`, S/Ptestonly, M11–M30, promptv4.1 for C3/C4/C7, originalTurkishC5/C6, model `gpt-4o-mini-2024-07-18`, temperature0, seed1729+rep. Snapshot availability may have changed; no automatic substitute. Never overwrite `test-frozen-20261022`:

```sh
python -m backend.evaluation.run_matrix --conditions C0 C1 C2 C3 C4 C5 C6 C7 --split test --prompt-revision v4.1 --reps 5 --workers 6 --max-calls 37500 --max-cost-usd 1000 --run-dir backend/evaluation/results_v4/NEW_AUTHORIZED_REPLICATION_ID
```

This instruction is a repeatability recipe, not new spending authorization, preregistration or independent confirmation. C5/C6 are lexical legacy adaptations; C3vsC4 changes feedback+budget; C4vsC7 addsCritic+rules; C7vsC6 changesseveralcomponents. Baseline/repetitions do not by themselves isolate each component.
