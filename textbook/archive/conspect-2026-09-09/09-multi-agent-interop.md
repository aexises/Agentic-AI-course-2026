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

### A2A 1.0.0 separates operations from bindings

A2A 1.0.0 defines a task and message model with JSON-RPC, gRPC, and HTTP/REST bindings. This course traces JSON-RPC over HTTP. Select a binding and version explicitly when implementing discovery, streaming, and authentication.

- This course uses the JSON-RPC binding over HTTP.
- Other defined bindings include gRPC and HTTP/REST.
- The JSON-RPC streaming path uses server-sent events.
- The application authenticates and authorizes each caller.

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

### Delegation needs a versioned contract

This chapter uses A2A 1.0.0 and traces its JSON-RPC binding. The specification also defines gRPC and HTTP/REST bindings. Identity, permission, and the validity of a returned artifact remain separate checks.

- Record the protocol version and selected binding.
- Authenticate the caller before assigning authority.
- Treat returned content as untrusted evidence.

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
6. Which responsibilities remain in the application after it adopts an interoperability protocol?

## Assessed practice

Trace a delegated catalog task from discovery to completion. Identify the caller, authorization decision, timeout owner, and artifact validator. No remote service deployment is required.

**Acceptance check:** Use A2A 1.0.0 terminology and distinguish the chosen binding from the abstract task model. Explain what happens after a failed or canceled task.

**Lab:** labs/08_langgraph_approval_security.ipynb

## Reading and evidence

- **S6** [A2A specification 1.0.0](https://a2a-protocol.org/v1.0.0/specification/). Versioned protocol specification, accessed, 2026-09-09. Separates the data model from JSON-RPC, gRPC, and HTTP/REST bindings. The course traces JSON-RPC.

## Source basis

The original structure follows `09-multi-agent-interop.pdf`. The 2026-09-09 edition adds the readings above, protocol clarifications, and assessed practice. Research findings and classroom exercises have different scopes.
