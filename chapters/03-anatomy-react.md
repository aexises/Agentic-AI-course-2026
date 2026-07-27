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

- Short-term memory is automatic but bounded.
- Long-term memory is scalable but requires explicit retrieval.
- Only re-supplied information can influence the next model call.

### Planning ranges from next-step choice to search

Decomposition creates subgoals, reasoning chooses actions, reflection critiques progress, and search explores alternatives. ReAct uses the simplest planner: decide only the next action from current evidence.

- Reactive planning adapts quickly to observations.
- One-step lookahead is efficient but myopic.
- Reflection and plan-and-execute address longer horizons.

### The runtime owns the action boundary

The model proposes a tool and arguments. The runtime parses or receives the structured call, validates types and policy, authorizes it, executes the tool, and appends the real result as an observation. The model must never fabricate the observation.

- Use stop sequences in a text protocol.
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

## Exam-ready summary

- The model proposes actions; the runtime validates and executes.
- ReAct alternates Thought, Action, and real Observation.
- Stop sequences and budgets are correctness features.
- Tracing reveals both outcome and trajectory failures.

## Self-test

1. What belongs in a robust agent profile?
2. Who produces each part of Thought-Action-Observation?
3. Why is a stop sequence needed in text ReAct?
4. Compare text parsing with native function calling.
5. List the required termination conditions for a safe loop.
6. Why does ReAct reduce hallucination yet remain myopic?

## Source basis

This chapter reorganizes and explains material from `03-anatomy-react.pdf`. It adds study structure and design implications, but introduces no external factual sources.
