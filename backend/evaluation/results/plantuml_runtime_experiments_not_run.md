# PlantUML Runtime Experiments Not Run

No new real PlantUML-runtime benchmark result was generated in this execution
environment.

## Execution Metadata

- Commit SHA used for this check: `77d5aa5`
- Date: `2026-07-29`
- Python: `3.12.13 (main, Mar  3 2026, 15:01:35) [MSC v.1944 64 bit (AMD64)]`
- Platform: `Windows-11-10.0.26200-SP0`
- Model: `none`
- Temperature: `none`
- Max iterations: `3`

## Reason

Java is available, but no PlantUML command or PlantUML JAR was found locally.
The code now supports real PlantUML validation/rendering through one of these
configuration options:

- `PLANTUML_JAR`
- `PLANTUML_CMD`
- a `plantuml` executable discoverable on `PATH`

Because no runtime was available, newly generated deterministic benchmark
outputs report project-defined fallback validation separately from
PlantUML-runtime-validated success. The real PlantUML-validated result fields
remain `null` / `not run` until the runtime is installed and the experiments
are rerun.
