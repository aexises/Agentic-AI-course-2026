# Capstone: evidence-backed equipment assistant

Build a small service that answers equipment-policy questions from a local corpus and proposes a ticket or reservation action. Combine the skills developed across the course. Start with a written API/data contract and a simple static-retrieval or deterministic baseline; justify every agent component against it.

## Required architecture

Use pgvector for the corpus, with LlamaIndex ingestion and stable source IDs. Compare dense retrieval with your hybrid/reranked variant on the same queries. Expose validated routes through FastAPI. Use LangGraph for bounded workflow state and a checkpoint that can be reopened. Include an OpenAI Agents SDK component with a narrow tool contract; explain its responsibility relative to LangGraph. Expose the ticket action through an actual MCP tool. The separate action ledger may remain SQLite as in Lab 18; it does not replace pgvector retrieval.

A model proposes an action. Trusted service identity and a separately created approval receipt determine whether it may execute. Bind approval to the exact operation content. Demonstrate denial, restart, response-loss simulation, safe replay and cross-tenant isolation. Reusing an operation ID with different content must not silently create a new effect. Checkpoint persistence alone is insufficient replay protection.

Package the application for local Docker Compose with readiness checks and persistent data. Integrating the RAG and ticket components is capstone work; the supplied track stacks are starting points, not a finished integrated application. Demonstrate an additive migration and compatible code rollback. Collect allowlisted request logs, latency and error measurements, and separate model usage from local timing.

## Outcome A: offline course completion

Run the complete workflow using scripted model fixtures and real local database, HTTP, MCP and container services. No paid model calls are required. Initial dependency, image and embedding-model downloads require internet; once cached, the assessment must run without provider inference. Demonstrate retrieval quality on your declared corpus; label scripted agent results as software behavior, not model capability.

Freeze an assessment set before final implementation: at least 12 tasks covering answerable questions, missing/conflicting evidence, malformed tools, denied actions, cross-tenant access, budget exhaustion, restart and replay. These counts and thresholds are course design choices. Keep development tasks separate. Published course examples are practice; create a new frozen set for self-assessment.

To complete Outcome A, earn at least 70/100 below and pass every critical check: no unauthorized effect in the declared denial cases, no duplicate effect under identical replay, failed attempts retained, fresh-environment execution instructions, and real local service/container evidence. Failure of a critical check leaves completion pending regardless of score.

## Outcome B: advanced assessment with live evidence

Complete Outcome A, then run the actual Gemini API through the relevant LangGraph/Agents SDK paths on the same frozen task contracts as a simple baseline. Use your own account and available model ID. Declare request/turn caps, timeout and a personal spending limit before starting. Never treat request caps as a guaranteed currency budget.

Run at least two recorded attempts per system per task, preserving order, failures and configuration. With a small set, report per-task results and uncertainty; do not claim general superiority. Retain actual provider usage when available, mark missing usage unknown, and price only with a cited applicable rate and date. A negative agent-versus-baseline result can pass if the experiment and interpretation are sound. Actual denied-action or duplicate-effect failures must be repaired and reassessed; retain earlier failures in the report.

Advanced completion requires at least 80/100, all critical checks, real provider traces, and a reproducible live evaluation report. GPU training, cloud deployment and hosted CI are optional; no hiring guarantee follows from either course outcome.

## Deliverables

- Implementation, notebooks, exact environment snapshot, Compose configuration and operating runbook.
- Corpus provenance/redistribution permission, frozen development/assessment splits and scoring rules.
- Manifest: code/prompt/data hashes, model ID when live, versions, seeds, timeouts, budgets and date.
- Raw attempts, failures, request traces and baseline comparison; separate fixtures and live results.
- API/MCP negative tests, approval and replay checks, migration/rollback evidence and image IDs.
- A brief architectural decision: keep the agent, simplify it or reject it, supported by your results.

## Rubric

| Area | Points | Evidence |
|---|---:|---|
| Retrieval and task behavior | 25 | Source lineage/abstention 10; query-level retrieval comparison 10; validated API behavior 5 |
| Authority and recovery | 25 | Approval/tenant boundary 10; checkpoint restart and replay 10; bounds and errors 5 |
| Delivery and observability | 25 | Actual Compose stack 10; migration/rollback 5; safe logs and measured service behavior 10 |
| Evaluation and explanation | 25 | Frozen fair baseline 10; all attempts and reproducibility 10; evidence-bounded conclusion 5 |

A default starter run does not earn implementation credit. Explanations without required runnable evidence receive at most half of their subcriterion's marks. For self-study, record assistance and perform a fresh demonstration without looking at instructor answers. Preserve a clear outcome label on the final report.
