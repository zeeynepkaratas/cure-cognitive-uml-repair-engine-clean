# Legacy Pre-Validation-Fix Results

This directory preserves the experiment result files that existed before the
`fix/validation-and-metrics` revision.

These files are retained for traceability only. They were produced with the
previous validation pipeline, where PlantUML outputs from LLM components were
not normalized consistently before downstream validation and reporting. New
results generated after this revision must not overwrite or be mixed with these
legacy artifacts.

Use the result files in the parent `backend/evaluation/results/` directory for
post-fix experiments.
