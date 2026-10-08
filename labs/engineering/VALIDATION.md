# Validation — 8 October 2026

Environment: Python 3.12.14 on macOS arm64. Direct pins and the resolved host environment are recorded in requirements.txt and requirements-lock.txt. Dependency compatibility check passed. Docker engine: 28.4.0. Other host platforms were not tested.

## Executed checks

- Ten reference tests passed: authorization; transaction/replay/conflict; actual HTTP plus MCP stdio; additive migration; release decisions; measurement contracts; actual HTTP timing; trace allowlist; concurrent duplicates; request-schema and approval-content binding.
- Six notebooks passed fresh-kernel execution. Three student copies run setup with exercises disabled; three instructor copies execute their checks. This does not mean an unfinished student submission passes.
- Actual Docker build and local Compose startup passed in an isolated temporary context containing the instructor implementation as submission.py. Approved creation, denial before approval, identical replay, repeated additive migration, container replacement, code rollback, existing-row replay and a new insert after rollback passed.
- A real response request ID matched a JSON log event using the route template. Public agent/reviewer key strings were absent from the inspected logs.

See [notebook results](validation/notebook-results.json), [Docker results](validation/docker-results.json), and [Docker build/run log](validation/docker-validation.log). The validation stack was stopped; its separately named validation volume was retained. Student starter files were not replaced with answers.

The v1/v2 validation images use the same business implementation with changed release metadata. This checks image replacement and compatibility with the migrated database, not rollback of an arbitrary breaking schema change. The release-gate contract was tested separately; no deliberately broken application image was deployed. Students must perform their own controlled broken-change exercise.

## Limits

No paid model inference, GPU training, remote MCP OAuth, cloud deployment, hosted CI or distributed telemetry collector was run. Local public teaching keys are not a production identity system. HTTP measurements target a local health endpoint and include client construction; they do not establish RAG quality, model latency or production capacity. Initial package/image/model downloads require internet.

Notebook structure, code, outputs and links were inspected. Full visual layout in the learner's notebook editor was not reviewed. No learner pilot has yet established timings or learning outcomes. Guided TODOs deliberately raise NotImplementedError until solved; only the instructor path provides completed reference behavior.
