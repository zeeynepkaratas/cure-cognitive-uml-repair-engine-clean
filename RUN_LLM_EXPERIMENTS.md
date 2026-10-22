# Paid LLM experiments — pending, no fabricated replacement results

Real LLM experiments are now authorized without a human USD ceiling; the key is configured locally. No paid call had occurred when the pre-LLM code freeze was committed. Execution status is recorded in run manifests and the revision report. Do not paste a secret into chat or commit it. The USD1000 CLI caps below are finite operator guardrails, not predicted spend or a human budget limit.

## Before execution

1. Read `docs/evaluation-protocol-v4.md`. Initial protocol commit: `0918c974ff8f8d01f82061655096da9be150452b`; the current F22 addendum is committed at `5a9a79b` (resolve its full SHA with `git log -1 --format=%H -- docs/evaluation-protocol-v4.md`).
2. Configure OPENAI_API_KEY locally using your shell/secret manager. The human authorization and operational guardrails are recorded in docs/llm-execution-authorization.md.
3. The requested gpt-4o-mini-2024-07-18 snapshot is deprecated in current official documentation. Availability is not established by this offline revision. If unavailable, record the error; obtain a model decision and revise/freeze the protocol before substituting a model. Do not silently use a current alias.
4. Use the pinned Python lock, Java/Graphviz and verified PlantUML JAR. Run all checks first.

## PowerShell commands from repository root

The human authorized no USD ceiling; the registered workload remains finite. Configure PLANTUML_JAR to the local checksum-verified JAR.

```powershell
$env:PYTHONHASHSEED='1729'
python -m pytest -q
python -m ruff check .
python -m backend.evaluation.run_matrix --split dev --datasets semantic --conditions C3 C4 C5 C6 C7 --reps 5 --dry-run
python -m backend.evaluation.run_matrix --split dev --datasets semantic --conditions C3 C4 C5 C6 C7 --reps 5 --max-calls 7500 --max-cost-usd 1000 --run-dir backend/evaluation/results_v4/dev-llm-01
```

Development: 20 cases × 5 conditions × 5 repetitions = 500 case-runs; at most 2,500 model calls before retries or 7,500 attempted calls including retries. Review development behaviour, then freeze any changed prompts/rules/configuration in a new protocol commit. All semantic test cases and retained S/P cases stay test only. Do not tune from test outcomes.

```powershell
python -m backend.evaluation.run_matrix --conditions C3 C4 C5 C6 C7 --reps 5 --dry-run
python -m backend.evaluation.run_matrix --conditions C3 C4 C5 C6 C7 --reps 5 --max-calls 37500 --max-cost-usd 1000 --run-dir backend/evaluation/results_v4/test-llm-01
```

Test: 100 cases × 5 conditions × 5 repetitions = 2,500 case-runs; at most 12,500 calls before retries or 37,500 attempted calls including retries. These are upper bounds, not predictions or minimum budget requirements. Durable conservative cost reservations may stop a run earlier than actual usage would.

Resume by repeating the exact same command with `--resume`; do not change models, prompts, code, seeds, dataset or split. Finished error records are retained. A budget-stopped partial case is explicitly incomplete and its partial trace is preserved; it is not a finished experiment. Preserve that run and start a separately labelled continuation if a different budget/configuration is approved. Do not selectively keep the best outputs.

After execution, analyze raw runs, preserving condition/repetition identities. The current non-LLM run is `nonllm-sourcefix-20261022`; new LLM and deterministic results must be assembled through the checked multi-run analysis path using matching protocol/input fingerprints. Never copy old v2 LLM outputs into v4 slots. Report failed/unavailable/incomplete conditions and all runs.

```powershell
python -m backend.evaluation.analyze_v4 --combine backend/evaluation/results_v4/nonllm-sourcefix-20261022 backend/evaluation/results_v4/test-llm-01 --run-dir backend/evaluation/results_v4/combined-test-01
python tools/check_numbers.py --run-dir backend/evaluation/results_v4/combined-test-01
```

The current matrix C5 uses the original prompts/control flow but cached lexical retrieval of the original four rules. It is not a bit-identical reproduction of the historical OpenAI-embedding ranking. Keep this caveat in the comparison report.
