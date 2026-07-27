# 12. Safety and Security

> Action amplifies model errors and attacks, so safety must be enforced through defense-in-depth at the model-runtime boundary and throughout the lifecycle.

## Learning objectives

- Separate adversarial security from responsible-AI harms
- Explain prompt injection and excessive agency
- Apply defense-in-depth
- Design runtime guardrails and safety evaluation

## Core notes

### Tools change the threat model

A model that only produces text has limited direct effect; an agent can send messages, execute code, modify files, or make transactions. Autonomy may remove per-step review, and untrusted web pages, documents, emails, and tool results enter the same context as instructions.

- The model proposes; the runtime authorizes.
- Real-world effects require stronger controls than content generation.
- Consequential actions need explicit policy and confirmation.

### Security and responsible AI overlap but are distinct

Security addresses adversaries exploiting the agent through prompt injection, tool misuse, data exfiltration, memory poisoning, and excessive agency. Responsible AI addresses harmful, biased, toxic, false, or otherwise unsafe outputs.

- Least privilege and sandboxing reduce adversarial impact.
- Alignment and content filters reduce harmful output.
- A jailbreak can connect the two categories.

### Prompt injection exploits the shared instruction-data channel

Direct injection is supplied by a user. Indirect injection is hidden in content the agent retrieves. Because instructions and data enter the same context, the model may follow malicious text as if it were authorized guidance.

- Indirect attacks require only control of content the agent reads.
- Tool results must never automatically become trusted instructions.
- There is no complete prompt-only fix.

### Excessive agency amplifies every successful exploit

An injected instruction inherits the agent's available tools and credentials. Too many tools, broad scopes, persistent secrets, and unreviewed autonomy increase maximum harm.

- Grant minimum tools and scopes.
- Default to read-only and short-lived credentials.
- Bound actions, time, spend, and network access.
- Require confirmation for destructive or irreversible operations.

### Defense-in-depth must be structural

Input validation, untrusted-content quarantine, tool-call policy, sandboxing, output filtering, monitoring, and human approval provide independent layers. A guardrail prompt or guardrail model can be fooled and therefore cannot be the sole defense.

- Validate before the model and again before tool execution.
- Separate trusted control data from retrieved content.
- Sanitize tool output before execution or rendering.
- Log and detect abnormal trajectories.

### Responsible output needs training-time and runtime controls

Bias and toxicity can originate in web-scale training data; alignment methods such as RLHF and DPO shape preferred behavior. Runtime classifiers and guardrails screen inputs and outputs. Hallucination requires grounding, citations, abstention, and verification.

- Measure toxicity and bias rather than assuming alignment solved them.
- Use RAG and tools for factual grounding.
- Apply safety controls across MCP servers and A2A delegation.
- Include injection and disallowed-action cases in evaluation.

## Exam-ready summary

- Action moves safety enforcement into code and infrastructure.
- Prompt injection cannot be solved by a stronger prompt alone.
- Least privilege limits blast radius.
- Security, responsible AI, evaluation, and observability must work together.

## Self-test

1. Why does agent action raise the stakes compared with a chatbot?
2. Differentiate security risks and responsible-AI harms.
3. Compare direct and indirect prompt injection.
4. What is excessive agency and how is it mitigated?
5. Design a defense-in-depth stack for a tool-using agent.
6. How should hallucination and toxic output be mitigated and tested?

## Source basis

This chapter reorganizes and explains material from `12-safety-security.pdf`. It adds study structure and design implications, but introduces no external factual sources.
