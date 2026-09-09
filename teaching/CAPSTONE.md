# Capstone: a bounded, evidence-backed agent

Build a small research-assistance workflow over a supplied local corpus. Use LangGraph for explicit state and stopping conditions, the Gemini API for optional model inference, and the OpenAI Agents SDK for a tool-using component. Explain the boundaries between these components. Do not add workers merely to include more framework features. The offline path must remain executable without a key.

The system should retrieve evidence with stable source IDs, call an allowlisted tool through validated arguments, abstain when evidence is insufficient, and pause before a simulated external effect. Persist and reopen the checkpoint. Replaying the same approved action must not duplicate the local effect. A SQLite checkpoint alone does not make an arbitrary remote service idempotent; explain what the external service would need to guarantee.

Compare the agent against a simple deterministic or static-retrieval baseline on the same tasks. Keep development tasks separate from a lecturer-supplied unseen assessment set. Freeze prompts, configuration, and scoring before opening that set. Include misleading evidence, missing sources, conflicting sources, malformed arguments, tool failures, exhausted budgets, and restart/replay cases. Report every attempted run, failed run, and unattempted task, with clear denominators.

## Submission

- Student notebook or a small Python package, with entry-point instructions and dependency snapshot.
- Data and scoring rules, with provenance and permission to distribute the chosen corpus.
- Configuration manifest: exact model ID for live runs, prompt/data hashes, package versions, request and turn caps, timeout, run date, and randomness settings.
- Raw run records plus a table comparing baseline and agent outcomes, latency, requests, and provider-reported usage where available. Label fixture results separately. Do not invent token usage or infer dollar cost without applicable pricing.
- Negative and replay tests, plus a runbook explaining stop conditions, recovery, credential setup, and known limitations.
- A short decision: retain the agent, simplify it, or reject the design, justified by observed evidence.

## Rubric (100 points)

| Area | Points | Full-credit evidence |
|---|---:|---|
| Functional correctness | 30 | Retrieval and tool execution satisfy specified tasks (10); source lineage and abstention work (10); state and stopping behavior match the contract (10) |
| Failure and recovery | 25 | Malformed inputs and tool failures handled (10); checkpoint reopen and duplicate-effect prevention demonstrated (10); budget exhaustion terminates (5) |
| Evaluation and evidence | 25 | Fair baseline and frozen assessment protocol (10); all attempts and failures retained (10); conclusions limited to measured scope (5) |
| Reproducibility and explanation | 20 | Fresh-environment offline rerun (10); model/configuration/data provenance (5); operating limits and justified framework choices (5) |

Award each subcriterion in proportion to independently reproducible evidence. A plausible explanation without runnable evidence receives at most half of that subcriterion's marks. Score model-independent behavior even when students lack paid API access; an explicitly labeled fixture-only report can earn full marks for a well-designed experiment protocol, but must not claim empirical model performance. The lecturer can require a shared live run separately if equitable access has been arranged. These weights and scoring rules are course design choices, not research findings.
