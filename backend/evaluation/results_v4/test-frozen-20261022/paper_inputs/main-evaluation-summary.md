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
