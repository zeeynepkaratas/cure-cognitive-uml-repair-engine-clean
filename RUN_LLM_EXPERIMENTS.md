# Real LLM evaluation — execution and reproduction

Paid experiments were explicitly authorized; the API key remains local and is never included in this artifact. The provider pilot and all800 development case-runs completed. The exact gpt-4o-mini-2024-07-18 snapshot returned responses. All failed development calls are retained; no outputs were selectively re-run. Development selection is recorded in docs/development-prompt-selection-v4.json. The final English prompt revision is v4.1; legacy C5/C6 prompts are unchanged.

## Frozen main test

Source and protocol freeze:1ead72ff7071e1f6de5867aaa250b0483d91431f. The running test is backend/evaluation/results_v4/test-frozen-20261022. It contains100 fixed cases: shared50, PURE10, semantic test40. C0–C2 run once; C3–C7 run five repetitions each, totaling2800 case-runs and2500 paid case-runs. The conservative37500-call maximum includes retries. USD1000 is a finite operator guardrail under no-ceiling user authorization, not predicted spend.

Configure OPENAI_API_KEY locally, the pinned PLANTUML_JAR, Python lock and Java/Graphviz. Never paste a key into chat or commit it. From the recorded source revision:

```sh
python -m backend.evaluation.run_matrix --conditions C0 C1 C2 C3 C4 C5 C6 C7 --split test --prompt-revision v4.1 --reps 5 --workers 6 --max-calls 37500 --max-cost-usd 1000 --run-dir backend/evaluation/results_v4/test-frozen-20261022
```

Use --dry-run for a zero-call plan. To resume an interrupted run, use the exact recorded source/protocol/configuration and append --resume. Preserve/copy the unmodified run directory into that checkout if necessary; do not change historical manifests to match a newer HEAD. Completed API-error records are skipped rather than retried. Budget-partial records are archived before continuation. Pending/in-flight/error counts must be reported if execution is incomplete.

Six case workers share a thread-safe durable budget; at most two compiler subprocesses run concurrently. Task order is seeded and its SHA is recorded. SDK connections are reused within a case and closed afterwards. New end_to_end_seconds includes worker-dispatch through final validation/metrics, excluding queue wait and serialization; elapsed_seconds remains the repair-loop measurement. Compiler caching/concurrency can affect timings.

After the run has completed:

```sh
python -m backend.evaluation.analyze_v4 --run-dir backend/evaluation/results_v4/test-frozen-20261022
python tools/check_numbers.py --run-dir backend/evaluation/results_v4/test-frozen-20261022
```

All conditions now share one main-test manifest, so no protocol-mismatched merge with the earlier non-LLM runs is needed. Earlier nonllm-20261022 and nonllm-sourcefix-20261022 remain separate evidence, including the disclosed post-test exploratory C2 fix. C5 reproduces original prompt/control flow with cached lexical retrieval of four original rules, not the historical embedding-retrieval distribution. Final execution counts and limitations belong in docs/revision-report.md; do not describe a running experiment as completed.
