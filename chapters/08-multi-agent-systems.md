# 08. Multi-Agent Systems

> Multiple agents add specialization, modularity, parallelism, and context division only when coordination costs are explicitly designed.

## Learning objectives

- Decide when multiple agents help
- Design roles, communication, and coordination
- Compare centralized, decentralized, and hierarchical topologies
- Bound multi-agent cost and termination

## Core notes

### More agents are useful only for separable work

A focused role, prompt, tool set, and context can outperform one overloaded agent. Multiple agents also allow modular testing, parallel tasks, and divided context. These gains disappear when work is tightly coupled or one well-equipped agent already succeeds.

- Specialization narrows behavior and tool choice.
- Modularity makes agents independently replaceable.
- Parallelism reduces time only for independent subtasks.
- Context division keeps each working set relevant.

### Coordination is the price of specialization

Each agent adds model calls and communication. Errors can propagate through handoffs, disagreement needs resolution, and someone must decide when the team is done. Multi-agent designs are harder to trace and secure.

- Cost grows with agents, turns, and coordination rounds.
- Messages consume context and can carry errors or injections.
- Termination needs shared budgets and a clear owner.
- Start with a single agent and add roles for measured reasons.

### Design collaboration along four dimensions

Roles define responsibility; communication defines information exchange; coordination selects the next actor and completion rule; evolution determines whether agents adapt through feedback or reflection.

- Give roles distinct objectives and tool scopes.
- Choose shared state or explicit messages deliberately.
- Define handoff contracts and synthesis ownership.
- Keep adaptation separate from uncontrolled drift.

### A runtime supplies identity, lifecycle, and delivery

The application sits on a runtime that creates and retires agent instances, uniquely addresses them, and routes messages. Standalone runtimes are simpler; distributed runtimes add process, machine, language, isolation, and operations concerns.

- Use one process for development and simple applications.
- Distribute only for scale, isolation, or polyglot requirements.
- Persist state intentionally across instance lifecycles.

### Communication can be shared-state or message-based

A blackboard lets agents read and update common state. Direct messaging targets a specific agent. Publish-subscribe decouples publishers from subscribers through topics. Topic scope is also a security boundary.

- Shared state simplifies synthesis but can create coupling.
- Direct messaging makes ownership explicit.
- Pub-sub supports fan-out and looser coupling.
- Partition topics by user, session, or tenant to prevent leakage.

### Topology determines control and failure shape

A centralized supervisor decomposes, routes, and synthesizes with clear accountability but becomes a bottleneck. Peer-to-peer systems remove the single boss but are harder to control. Hierarchies compose teams at scale while multiplying coordination layers.

- Supervisors behave like LLM routers over shared state.
- Peers need negotiation, consensus, and termination rules.
- Hierarchies need bounded delegation at every level.
- Measure handoffs, agent-specific failures, and total call budget.

## Exam-ready summary

- Use multiple agents for genuine specialization or parallelism.
- A runtime provides identity, lifecycle, and messaging.
- Communication and topology determine security and debugging complexity.
- Every team needs an owner of synthesis, budget, and completion.

## Self-test

1. List four benefits and four costs of multi-agent systems.
2. What are the four dimensions of collaboration?
3. Compare shared state, direct messaging, and publish-subscribe.
4. When is a distributed runtime justified?
5. Compare centralized, decentralized, and hierarchical topologies.
6. How does a supervisor pattern terminate safely?

## Source basis

This chapter reorganizes and explains material from `08-multi-agent-systems.pdf`. It adds study structure and design implications, but introduces no external factual sources.
