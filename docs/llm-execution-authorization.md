# LLM execution authorization

On 2026-10-22 the human explicitly authorized real LLM experiments without a USD budget ceiling and configured an API key locally using the hidden PowerShell prompt. The credential is stored in the Windows user environment and is never included in source, reports or chat output.

The finite registered workload remains bounded by case count, repetitions, maximum iterations, completion-token limits, timeouts and retries. CLI safety caps of USD 1000 per run are operator guardrails under this authorization, not claimed human cost estimates. Spending is still measured and reported. No unnecessary or unregistered paid work is authorized by this note.

An explicit development-only pilot checks provider access, structured-output compatibility and approximate latency. Pilot observations are retained separately and never pooled as extra repetitions in the test matrix. Permanent provider authentication/access/model errors stop the run and preserve the failed record. A model substitution requires an explicit decision and a new protocol revision; the runner never changes models automatically.
