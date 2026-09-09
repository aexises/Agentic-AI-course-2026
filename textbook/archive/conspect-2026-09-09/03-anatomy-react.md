# 03. Agent Anatomy and ReAct

> ReAct operationalizes agency as a bounded Thought-Action-Observation cycle whose evidence comes from the runtime, not the model.

## Learning objectives

- Engineer the four agent components
- Trace a ReAct episode
- Implement safe parsing and termination
- Recognize horizon and format failures

## Core notes

### The profile is an executable contract

The system prompt defines role, objective, tool menu, output protocol, constraints, stopping behavior, and escalation. It should read like a precise specification for a careful colleague, with examples where the protocol is easy to misunderstand.

- State success before listing implementation details.
- Give each tool a description and example call.
- Specify an exact output protocol and stopping condition.
- Add guardrails and human escalation rules.

### Memory turns a stateless model into a stateful system

Short-term memory is the running context; long-term memory is an external store read and written through tools. The transcript is the immediate state of ReAct because each next decision depends on prior actions and observations.

- The application or provider must carry the bounded conversation state.
- Long-term memory is scalable but requires explicit retrieval.
- Only re-supplied information can influence the next model call.

### Planning ranges from next-step choice to search

Decomposition creates subgoals, reasoning chooses actions, reflection critiques progress, and search explores alternatives. ReAct uses the simplest planner: decide only the next action from current evidence.

- Reactive planning adapts quickly to observations.
- One-step lookahead is efficient but myopic.
- Reflection and plan-and-execute address longer horizons.

### The runtime owns the action boundary

The model proposes a tool and arguments. The runtime parses or receives the structured call, validates types and policy, authorizes it, executes the tool, and appends the real result as an observation. The model must never fabricate the observation.

- Use supported stop sequences as format controls in text protocols.
- Prefer native tool calling in production when available.
- Sandbox, scope permissions, and confirm consequential actions.

### ReAct interleaves deliberation and grounding

Each iteration contains a Thought from the model, an Action from the model, and an Observation from the environment. Acting grounds later reasoning in evidence, while reasoning improves tool selection compared with an act-only policy.

- Thought chooses the next step.
- Action names and parameterizes a tool.
- Observation records the runtime result.
- Final Answer ends the episode.

### A correct loop is bounded and observable

Termination must include a final-answer condition plus hard step, token, cost, or time budgets. The trace should be captured so evaluators can inspect tool choice, observations, errors, efficiency, and whether the final claim is grounded.

- Common failures: format drift, greedy parsing, fabricated observations.
- Long horizons compound errors and can make the agent lose the goal.
- No backtracking means a bad line may persist.
- Native schemas reduce format drift but not reasoning errors.

### A complete tool cycle returns observed results

A native tool request is only part of the protocol. After validation, the runtime returns each result with the matching call identity and continues the model exchange. Preserve the provider's complete response content and cap the loop.

- Dispatch through the supplied tool registry.
- Keep model rounds and tool calls as separate budgets.
- Test empty responses and multiple calls.

## Exam-ready summary

- The model proposes actions; the runtime validates and executes.
- ReAct alternates Thought, Action, and real Observation.
- Validate the complete protocol and enforce runtime budgets.
- Tracing reveals both outcome and trajectory failures.

## Self-test

1. What belongs in a robust agent profile?
2. Who produces each part of Thought-Action-Observation?
3. What can a supported stop sequence prevent, and what must the runtime still check?
4. Compare text parsing with native function calling.
5. List the required termination conditions for a safe loop.
6. Which state must survive the model, tool, and model round-trip?

## Assessed practice

Complete Lab 5. Demonstrate that the second model request contains the executed tool result and its matching ID. Replace the registry with a fake and prove that the replacement runs.

**Acceptance check:** The offline round-trip and replacement-registry tests pass. A missing result or exhausted budget yields an explicit stop reason.

**Lab:** labs/05_gemini_bounded_tools.ipynb

## Reading and evidence

- **S1** [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling). Google documentation, accessed, 2026-09-09. Check model support and preserve complete model content when returning function responses.

## Source basis

The original structure follows `03-anatomy-react.pdf`. The 2026-09-09 edition adds the readings above, protocol clarifications, and assessed practice. Research findings and classroom exercises have different scopes.
