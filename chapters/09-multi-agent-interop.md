# 09. Multi-Agent Interoperability

> A2A treats agents as discoverable services with long-running task lifecycles, while MCP connects each agent to tools and data.

## Learning objectives

- Explain the agent interoperability problem
- Describe Agent Cards and A2A task objects
- Separate MCP and A2A responsibilities
- Threat-model cross-agent delegation

## Core notes

### Agent ecosystems recreate the integration problem one layer up

Real agents use different frameworks, vendors, organizations, endpoints, and security domains. Bespoke pairwise integrations do not scale. An interoperable agent must publish capabilities and accept work without exposing its internal reasoning implementation.

- An agent resembles a service with discovery, endpoint, and authentication.
- Unlike a simple API, it reasons and may run for minutes or days.
- The protocol must cover status, streaming, and artifacts.

### A2A builds agent collaboration on web standards

The Agent-to-Agent protocol uses HTTP, JSON-RPC, server-sent events, and standard authentication. Its design supports natural agentic interaction, secure enterprise use, long-running tasks, and multiple modalities.

- HTTP provides transport.
- JSON-RPC structures requests and responses.
- SSE streams task updates.
- Standard authentication lowers integration friction.

### Agent Cards make capabilities discoverable

An Agent Card is a machine-readable manifest containing identity, provider, version, skills, endpoint, and authentication information. Clients can fetch a well-known URL, use a registry, or follow a referral.

- Discovery avoids hard-coding every remote capability.
- Cards should be authenticated or signed before trust.
- Capabilities should be described at agent-level granularity.

### Tasks organize long-running collaboration

A task has a lifecycle such as submitted, working, waiting for input, completed, failed, or canceled. Messages contain parts such as text or files; artifacts are the produced deliverables. Streaming exposes progress without pretending the work is one synchronous call.

- Messages carry conversation turns.
- Parts carry multimodal content.
- Artifacts carry completed outputs.
- Lifecycle state enables pause, input, retry, and completion.

### MCP and A2A form two different layers

MCP connects an agent to schema-defined tools and data sources. A2A connects one autonomous, reasoning agent to another through a task lifecycle. A remote agent may itself use MCP servers to complete delegated work.

- Use MCP for vertical integration with tools and data.
- Use A2A for horizontal collaboration across agent boundaries.
- Do not model a long-running autonomous service as a micro-tool.

### Delegation crosses trust and governance boundaries

Every cross-agent edge raises questions about identity, authorization, prompt injection, over-delegation, data retention, compliance, cost, and audit. Remote outputs must be handled as untrusted content even after authentication.

- Authenticate the agent and verify its card.
- Scope delegated authority by task, spend, action, and time.
- Confirm high-stakes actions with a human.
- Log context leaving the organization and artifacts returning.

## Exam-ready summary

- A2A standardizes discovery and long-running work between agents.
- Agent Cards advertise identity, skills, endpoint, and authentication.
- MCP serves tools and data; A2A serves agent collaboration.
- Cross-agent trust requires authentication, least privilege, bounds, and audit.

## Self-test

1. Why is an agent not equivalent to a simple REST endpoint?
2. What information belongs in an Agent Card?
3. Define task, message, part, and artifact.
4. How does A2A support long-running work?
5. Compare MCP and A2A with a concrete example.
6. Threat-model a delegated task across organizations.

## Source basis

This chapter reorganizes and explains material from `09-multi-agent-interop.pdf`. It adds study structure and design implications, but introduces no external factual sources.
