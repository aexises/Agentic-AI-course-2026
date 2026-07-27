# 13. Production, Economics, and the Frontier

> Production success is determined by the versioned, observable, economical, and secure system around the model rather than a one-off demo.

## Learning objectives

- Close the prototype-to-production gap
- Engineer cost, latency, and reliability
- Explain AgentOps and safe rollout
- Connect current successes to open problems

## Core notes

### A product must work repeatedly under constraints

A prototype needs one successful demonstration; a production service must work safely, reliably, economically, and at scale. Prompts, tools, models, retrieval, memory, policies, and evals become versioned system components.

- Reliability includes retries, timeouts, fallbacks, and idempotency.
- Compliance and security join functional correctness.
- Most engineering effort surrounds the model.

### Cost and latency compound across agent steps

Agent loops make multiple model and tool calls, so per-token and per-call costs accumulate. Routing sends ordinary work to cheaper models and hard work to stronger reasoning models. Caching, smaller models, fine-tuning, and bounded loops reduce spend.

- Cache embeddings, retrievals, results, and prompt prefixes.
- Parallelize independent steps.
- Stream progress to reduce perceived latency.
- Set token, step, time, and spend budgets.

### AgentOps combines service operations with LLM-specific controls

Production agents need traces, dashboards, alerts, prompt and model versioning, evaluation gates, guardrails, and human checkpoints in addition to normal service reliability patterns.

- Trace model, tool, retrieval, memory, and agent spans.
- Monitor quality, cost, latency, error, and safety metrics.
- Use circuit breakers and fallbacks for unstable dependencies.
- Preserve reproducibility across silent model or tool changes.

### Rollout should be reversible

Agents can ship as services, batch workers, or embedded assistants. Canary releases, feature flags, gradual traffic, evaluation gates, and rapid rollback reduce the impact of behavioral regressions.

- Test on representative and adversarial tasks before deployment.
- Require approval for consequential actions.
- Keep a human-owned escalation path.
- Audit actions after deployment.

### Execution-grounded domains reveal the clearest wins

Coding agents can inspect repositories, edit files, and run tests; their Agent-Computer Interface exposes compact actions and concise feedback. Computer-use agents generalize to GUIs through screenshots or accessibility trees but remain more brittle.

- Interface design can matter as much as the base model.
- Execution tests make coding outcomes verifiable.
- Human review remains essential.
- High benchmark scores do not guarantee open-world reliability.

### The frontier and the open problems advance together

Reasoning models, longer autonomous horizons, computer use, multimodality, MCP, and A2A expand capability. Reliability over long horizons, evaluation leakage, prompt injection, cost, accountability, labor impact, and misuse remain unresolved constraints.

- Clear ownership is required for deployed agents.
- Audit trails document what happened and why.
- Economics differ from fixed-cost traditional software.
- Launch only the least autonomous system that passes eval and safety gates.

## Exam-ready summary

- Production is disciplined engineering around the model.
- Routing, caching, bounds, and parallelism control cost and latency.
- AgentOps versions, evaluates, traces, guards, and rolls back the whole system.
- Frontier capability does not remove reliability, security, or accountability limits.

## Self-test

1. What distinguishes an agent demo from a production product?
2. Give four methods for reducing cost and four for reducing latency.
3. What artifacts must be versioned for reproducibility?
4. What does AgentOps add to ordinary service operations?
5. Why are coding agents comparatively successful?
6. Create a production launch checklist for an autonomous agent.

## Source basis

This chapter reorganizes and explains material from `13-production-frontier.pdf`. It adds study structure and design implications, but introduces no external factual sources.
