# Supplementary material

The exact Turkish templates are published in `ai_core/prompts/legacy/`. English translations in this directory are explanatory translations and were not used for the retained experiments. Current English prompts used by the improved conditions are in `ai_core/prompts/v4/`. There is no separate system message in the retained Critic/Healer templates.

The rule catalogue with IDs, severities and domain guards is `ai_core/rules/catalogue.json`. All new scenario requirements and manually specified references are in `backend/evaluation/semantic_benchmark/scenarios.json` and `M01`–`M30/gold.puml`. Exact injections/seeds and split are in `cases.json` and `split.json`. The original pilot reference models remain in `pure_external_repair_cases.py`.

The 13-scenario table copied here is an internal consistency review, not independent expert annotation. New gold models are pending independent expert review. No expert-accuracy or semantic-correctness rate is inferred from this table. The old note in its historical text is superseded by this explicit qualification.

The manifest provides hashes for supplementary sources. No new LLM output or measurements were created by this export.
