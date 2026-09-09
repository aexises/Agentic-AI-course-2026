# Exam Preparation Guide

## Six comparisons to master

| Compare | Essential distinction |
|---|---|
| Chatbot vs workflow vs agent | Reply-only vs code-directed control vs model-directed control |
| Prompting vs RAG vs fine-tuning | Behavior in context vs external knowledge vs weight adaptation |
| ReAct vs plan-and-execute | Next-step reactive choice vs global plan followed by execution |
| Workflow vs multi-agent | Explicit control paths vs coordinated autonomous roles |
| MCP vs A2A | Agent-to-tool/data integration vs agent-to-agent collaboration |
| Outcome vs trajectory evaluation | Whether the result is correct vs how it was produced |

## Four diagrams to reproduce from memory

1. The perceive-reason-act loop with the runtime at the action boundary.
2. The classic RAG ingestion and query pipeline.
3. The two-layer MCP + A2A architecture.
4. The production loop: build -> eval gate -> guardrails -> deploy -> trace and monitor.

## High-value design rules

- Choose the least autonomy that solves the problem.
- The model proposes; the runtime validates, authorizes, and executes.
- Relevance beats context volume.
- Evaluate retrieval and generation separately.
- Add agents only for measured specialization, modularity, parallelism, or context division.
- Prefer objective and execution-based evaluation.
- You cannot prompt your way out of prompt injection.
- Version prompts, tools, models, policies, data, and evals.

## Practice method

For a coding assessment, submit the input cases, expected results, versioned setup, and observed failures. Compare a simpler baseline before adding autonomy. Distinguish a malformed response, a wrong answer, an API failure, and a denied action. The capstone rubric appears in teaching/CAPSTONE.md.

For every architecture question, answer in four passes: define the components, trace control flow, identify failure modes, then state evaluation and safety controls. This mirrors how the source course develops each topic and prevents answers that describe capability without engineering discipline.
