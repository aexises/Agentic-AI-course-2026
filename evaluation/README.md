# Evaluation runner

Run from the course root in the lab environment:

```bash
python -m evaluation.run --output evaluation/results/dev-fixture
python -m evaluation.run --inject-failure --output evaluation/results/failure-fixture
```

Each output directory must be new, preserving earlier evidence. Choose a new directory name when replaying the delivered fixture commands. Outputs include a manifest, an fsynced attempt-start journal, completed/failed JSONL records, and a summary. A caught cancellation retains the attempted row. After an uncatchable process kill, reconcile starts in `attempts.jsonl` with `runs.jsonl`; the summary may be absent or incomplete. Process-kill behavior has not been executed here. Requests have a global cap. A timeout or budget exception remains a failed attempted case; cases not reached are recorded as unattempted. Infrastructure failures and wrong completed answers remain distinguishable. The baseline receives the explicit product field and uses direct lookup. An agent is not needed for this task; identifying that is a valid outcome.

The small published `heldout` split supports a teaching workflow, not a secret benchmark. Instructors should create an additional undisclosed set before final assessment. Development prompts must not be tuned on final-assessment cases. The fixture runs check the harness without making a claim about Gemini. Unit tests validate data schemas, the injected failure path, and budget exhaustion.

For a locally configured Gemini account, choose a supported model and acknowledge its API costs:

```bash
python -m evaluation.run --mode live --model MODEL_ID --split heldout --repeats 2 --max-requests 48 --acknowledge-api-cost --output evaluation/results/heldout-live
```

Set `GEMINI_API_KEY` outside files and logs. This command permits at most 48 model requests, uses `max_tokens=1024`, disables client HTTP retries, and applies a 45-second outer timeout per agent run. A timeout can leave a provider request billed; the runner counts attempted requests. Request/token settings do not guarantee a dollar ceiling. Check the chosen model's current pricing and configure account-side controls before running. Live behavior has not been validated as part of the fixture tests.

The runner fails fast on invalid setup, does not overwrite output directories, and logs exception class names rather than raw provider exception text. It performs no automatic model substitution. Call counts include tools' model continuation, but the local dictionary tool itself makes no model request. An empty summary has null rates rather than claiming zero measured performance.
