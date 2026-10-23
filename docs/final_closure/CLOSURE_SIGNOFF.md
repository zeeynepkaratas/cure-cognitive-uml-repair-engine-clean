# Final software/evidence closure sign-off

**RESEARCH_ARTIFACT_CLOSED_WITH_LIMITATIONS**

`REVIEWER_CONCERNS_ALL_CLOSED = false`. This is automated research-artifact verification, not a human expert/reviewer endorsement. No manuscript or anonymous publication has been approved.

|Decision|Status|Scope/evidence|
|---|---|---|
|SOFTWARE_HANDOFF|PASS|Fresh environment, 186 passed tests, lint/build/live checks, safe verifier and documented restricted local use|
|V4_EVIDENCE_FREEZE|PASS|4660 protected hashes, unchanged baseline sources/tags; full 2800-design numeric checks and external-copy replay|
|QUALIFIED_MANUSCRIPT_REVISION|READY_WITH_LIMITATIONS|Author can revise using full table inventory and negative results; manuscript itself unchanged|
|BLIND_SUBMISSION_READINESS|PENDING|Human contextual review and actual independent anonymous hosting/journal check absent|
|EXTERNAL_SEMANTIC_VALIDITY|PENDING|Independent expert annotations/source-diverse sealed validation not performed|
|PUBLIC_DEPLOYMENT_READINESS|PENDING|Docker/auth/quotas/isolation/load/cancellation/privacy checks not performed|

Actually observed tests: **186passed,2skipped**, plus13 independent evidence checks,4 live JVM fixtures and4 local HTTP checks. Fresh Python lock install/pipcheck, Ruff, fresh offline npmci/lint/build passed. Full2800design/7936responses,1,400 primary F1 evaluations,2830declaredhashes,312 McNemar/Holm and208pairedsemantic comparisons verified.4,660 protectedfiles byte-identical; prior audited tracked files unchanged except the explicitly updated ARTIFACT_README.md. Historical source/protocol/tags preserved.

All38original rows retain previous status (8COMPLETE,25PARTIAL,4OPEN,1NOT TESTABLE). They are individually disposed of plus newF33safe-output guard: `{'EXTERNAL_ACTION_REQUIRED': 5, 'CLOSED_WITH_DISCLOSED_LIMITATION': 24, 'VERIFIED_COMPLETE': 9, 'NOT_TESTED': 1}`. CLOSED_WITH_DISCLOSED_LIMITATION is not technical verification and does not convert a semantic OPEN defect into a fix. See the CSV for every actual result, remaining limitation and owner.

Accepted v4 limitations: M11_2WeatherStation accepted 5/5 (F1=8/9); other restricted structural deviations; shared-template/co-authored gold; low selected-corpus project specificity; source/repetition dependence and unadjusted semantic p-values; C2post-test exploratory; historicalPUREfilter unknown; lexical-vs-embedding adaptation; restrictedparser; no fullSDKrequestarchive; nonanonymous publichistory; trusted-only CLI; API not production-certified. New research method, new benchmark, paid replication and post-test metric tuning were not performed.

External expert/hosting/publication/deployment owners and concrete completion evidence remain PENDING in EXTERNAL_ACTIONS.md. These do not prevent handing off the internally consistent local v4 artifact with limited claims. Any future broad claim requires its own evidence.

Source/audit anchor: `0aaf7dfe11eb4a726b7caeb22073ab464fe7d38e`; closure branch `closure/v4-final-artifact`. FINAL_EVIDENCE_MANIFEST.json records exact historical/new hashes and identity scope. The final containing commit cannot embed its own hash; after local commit, a detached receipt outside the checkout records finalHEAD, manifestSHA and clean status. No GitHub push, release/tag, anonymous upload or deployment occurred.
