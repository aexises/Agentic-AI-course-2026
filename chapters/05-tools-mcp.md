# 05. Tool Use, MCP, and Frameworks

> Tools are typed prompts at a security boundary; MCP standardizes their integration, while frameworks organize control and state.

## Learning objectives

- Design reliable tool schemas
- Explain the model-runtime-tool cycle
- Describe MCP primitives and transports
- Choose raw APIs or a framework

## Core notes

### A tool is a typed contract, not direct model access

A tool definition names an operation, explains when to use it, and defines typed parameters. The model emits a name and arguments; the runtime validates, authorizes, executes, and returns the result to context.

- The model never directly touches the external API.
- Schema validity must be followed by policy validation.
- Tool results are untrusted inputs to the next model step.

### Tool descriptions are prompts

Models select and fill tools from their specifications, so names, descriptions, examples, parameter types, and error messages directly affect behavior. Good granularity avoids both excessive micro-calls and confusing mega-tools.

- Prefer minimal parameters and enums over unconstrained text.
- Return actionable errors rather than stack traces.
- Make retry-prone operations idempotent.
- Gate destructive or irreversible actions.

### The runtime is the security boundary

Model-generated arguments must be treated as attacker-controlled input. Runtime controls include sanitization, least-privilege credentials, read-only defaults, sandboxing, rate limits, audit logs, and confirmation.

- Do not execute raw model strings with unsafe evaluators.
- Restrict filesystem and network scopes.
- Separate proposing an action from authorizing it.

### MCP replaces bespoke N-by-M integration

Without a standard, every agent must be wired separately to every tool. The Model Context Protocol provides a shared JSON-RPC interface so hosts can connect to reusable servers, changing integration growth from N multiplied by M toward N plus M.

- Tools expose actions with possible side effects.
- Resources expose read-only context.
- Prompts expose reusable interaction templates.

### MCP is bidirectional and transport-independent

Servers expose tools, resources, and prompts; clients can expose sampling, roots, and elicitation. The same protocol messages can flow over local stdio or remote Streamable HTTP sessions.

- Sampling lets a server request host-model generation.
- Roots communicate permitted filesystem scopes.
- Elicitation asks the user for input during a task.
- Transport choice changes deployment and trust assumptions.

### Frameworks package orchestration, not understanding

Frameworks provide loops or state graphs, persistence, streaming, tool integration, observability, memory, and human-in-the-loop hooks. Raw APIs suit simple or highly controlled agents; frameworks help when state and coordination become first-class.

- LangGraph represents nodes, edges, conditional control, and shared state.
- Crew-style systems emphasize role-based multi-agent work.
- Understand prompts and boundaries before adding framework abstraction.
- MCP standardizes tools; A2A standardizes agent-to-agent collaboration.

## Exam-ready summary

- A model requests a tool call; a runtime decides whether to execute it.
- Tool ergonomics strongly influence model reliability.
- MCP standardizes reusable tools, resources, and prompts.
- Frameworks are justified by stateful orchestration needs.

## Self-test

1. Walk through the complete function-call cycle.
2. What makes a tool specification model-friendly?
3. Why must tool results be treated as untrusted?
4. Explain the N-by-M problem and MCP's answer.
5. List server-side and client-side MCP primitives.
6. When is a framework preferable to a raw model API?

## Source basis

This chapter reorganizes and explains material from `05-tools-mcp.pdf`. It adds study structure and design implications, but introduces no external factual sources.
