# Textbook source checks

Checked 9 September 2026. Citations identify external research or interface facts. The equipment examples, exercises, design proposals, and conditional mathematical derivations are original teaching material. No empirical result is inferred from an illustrative number.

The checks are (1) source identity/type/year, (2) support for the narrow attributed method or claim, and (3) scope and interpretation. This is not three independent replications.

## effective-agents

[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — Engineering article, 19 December 2024; 2024.

Checked passage: Workflow/agent distinction and workflow patterns.

Scope: Architecture vocabulary; classroom examples and design choices are original.

Used in: 01-introduction.md, 04-design-patterns.md

## react

[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Research paper; cited by initial arXiv year; 2022.

Checked passage: Abstract and method overview.

Scope: Interleaving reasoning, actions and observations; no imported benchmark rate.

Used in: 01-introduction.md, 03-anatomy-react.md

## transformer

[Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Research paper; cited by initial arXiv year; 2017.

Checked passage: Abstract and method overview.

Scope: Attention architecture and scaled dot-product attention; no claim about a particular current provider architecture.

Used in: 02-llm-reasoning-engine.md

## cot

[Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) — Research paper; cited by initial arXiv year; 2022.

Checked passage: Abstract and method overview.

Scope: Historical prompting method and studied task categories; no universal prompting recommendation.

Used in: 02-llm-reasoning-engine.md

## pal

[PAL: Program-aided Language Models](https://arxiv.org/abs/2211.10435) — Research paper; cited by initial arXiv year; 2022.

Checked passage: Abstract and method overview.

Scope: Delegation of computation to programs; correctness of extracted inputs remains separate.

Used in: 02-llm-reasoning-engine.md

## chive

[Would this change your answer? Evaluating Explanations of LLM Behavior In The Wild with Counterfactual Experiments](https://arxiv.org/abs/2608.16747) — Anthropic/Fellows preprint; arXiv v1, 17 August 2026; 2026.

Checked passage: Abstract and method overview.

Scope: Counterfactual behavioral tests; classroom exercises do not use activation access or reproduce the full pipeline.

Used in: 02-llm-reasoning-engine.md, 10-reasoning-planning.md, 11-evaluation-observability.md

## gemini-tools

[Function calling with the Gemini API](https://ai.google.dev/gemini-api/docs/function-calling) — Mutable API documentation; 2026.

Checked passage: Function calling cycle and function responses.

Scope: Exact tested notebook package versions are separate from mutable documentation; no live-provider validation claim.

Used in: 02-llm-reasoning-engine.md, 03-anatomy-react.md

## gemini-openai

[OpenAI compatibility](https://ai.google.dev/gemini-api/docs/openai) — Mutable API documentation; 2026.

Checked passage: Python client configuration and function calling.

Scope: Compatibility for selected interfaces, not complete feature parity.

Used in: 02-llm-reasoning-engine.md, 05-tools-mcp.md

## toolformer

[Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) — Research paper; cited by initial arXiv year; 2023.

Checked passage: Abstract and method overview.

Scope: Learning API selection/use; does not establish application authorization.

Used in: 05-tools-mcp.md

## agents-models

[Models — OpenAI Agents SDK](https://openai.github.io/openai-agents-python/models/) — Mutable SDK documentation; 2026.

Checked passage: Non-OpenAI models and Chat Completions adapter.

Scope: Model adapter boundary; local tools retain validation responsibilities.

Used in: 05-tools-mcp.md

## mcp-spec

[Model Context Protocol specification, 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) — Versioned protocol specification; 2025.

Checked passage: Architecture and features.

Scope: Dated baseline, not a claim to describe every later protocol version.

Used in: 05-tools-mcp.md, 09-multi-agent-interop.md

## mcp-roots

[Roots, specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/client/roots) — Versioned protocol specification; 2025.

Checked passage: Purpose and security considerations.

Scope: Roots convey filesystem context and do not enforce a sandbox.

Used in: 05-tools-mcp.md

## rag

[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Research paper; cited by initial arXiv year; 2020.

Checked passage: Abstract and method overview.

Scope: Original parametric/nonparametric generation formulation; modern classroom pipeline is not a replication.

Used in: 06-rag-agentic-rag.md

## graphrag

[From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130) — Research paper; cited by initial arXiv year; 2024.

Checked passage: Abstract and method overview.

Scope: Graph-based query-focused summarization; no claim that every graph retriever implements this method.

Used in: 06-rag-agentic-rag.md

## lost-middle

[Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) — Research paper; cited by initial arXiv year; 2023.

Checked passage: Abstract and method overview.

Scope: Position-sensitive behavior in studied long-context tasks; no claim of identical behavior in later models.

Used in: 07-memory-context.md

## generative-agents

[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) — Research paper; cited by initial arXiv year; 2023.

Checked passage: Abstract and method overview.

Scope: Memory, reflection and planning in simulation; application data governance is course design.

Used in: 07-memory-context.md

## langgraph-persistence

[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) — Mutable framework documentation; 2026.

Checked passage: Checkpoints and threads.

Scope: Persistence semantics; local storage does not guarantee remote exactly-once effects.

Used in: 07-memory-context.md

## langgraph-interrupts

[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) — Mutable framework documentation; 2026.

Checked passage: Resuming interrupts; rules for side effects.

Scope: Node restart on resume; course approval binding and idempotency are application design.

Used in: 07-memory-context.md

## harness-report

[How enabling two settings tripled our scores on the ARC-AGI-3 benchmark](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/) — Research/engineering post, 29 July 2026; 2026.

Checked passage: Harness comparison conditions.

Scope: A particular system/harness result; not a Gemini improvement factor.

Used in: 07-memory-context.md, 11-evaluation-observability.md

## multiagent-report

[Patterns and problems in emerging multiagent systems](https://www.anthropic.com/research/multiagent-systems) — Research post, 13 August 2026; 2026.

Checked passage: Coordination, epistemic failures and incompatible goals.

Scope: Controlled settings, not prevalence in production.

Used in: 08-multi-agent-systems.md

## a2a

[Agent2Agent protocol specification, version 1.0.0](https://a2a-protocol.org/v1.0.0/specification/) — Versioned protocol specification; year is access year; 2026.

Checked passage: Agent Card, task/message model and protocol bindings.

Scope: JSON-RPC is the teaching binding; no remote deployment is claimed.

Used in: 09-multi-agent-interop.md

## self-consistency

[Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) — Research paper; cited by initial arXiv year; 2022.

Checked passage: Abstract and method overview.

Scope: Sampling and aggregation method; independent-error calculation is an original conditional teaching example.

Used in: 10-reasoning-planning.md

## tree-thoughts

[Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) — Research paper; cited by initial arXiv year; 2023.

Checked passage: Abstract and method overview.

Scope: Search over intermediate candidates; kit example and tree-count derivation are original.

Used in: 10-reasoning-planning.md

## reflexion

[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) — Research paper; cited by initial arXiv year; 2023.

Checked passage: Abstract and method overview.

Scope: Verbal feedback retained for later attempts; not weight updating in the described method.

Used in: 10-reasoning-planning.md

## self-refine

[Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) — Research paper; cited by initial arXiv year; 2023.

Checked passage: Abstract and method overview.

Scope: Iterative generation, feedback and refinement; no guarantee of improvement.

Used in: 10-reasoning-planning.md

## llm-judge

[Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) — Research paper; cited by initial arXiv year; 2023.

Checked passage: Abstract and method overview.

Scope: Judge bias categories in the studied setting; no claim that mitigations eliminate bias.

Used in: 11-evaluation-observability.md

## swebench

[SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770) — Research paper; cited by initial arXiv year; 2023.

Checked passage: Abstract and method overview.

Scope: Benchmark task identity; no current leaderboard or score claim.

Used in: 11-evaluation-observability.md

## gaia

[GAIA: a benchmark for General AI Assistants](https://arxiv.org/abs/2311.12983) — Research paper; cited by initial arXiv year; 2023.

Checked passage: Abstract and method overview.

Scope: Benchmark task identity; no current leaderboard or score claim.

Used in: 11-evaluation-observability.md

## tau-bench

[tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) — Research paper; cited by initial arXiv year; 2024.

Checked passage: Abstract and method overview.

Scope: Benchmark task identity; no current leaderboard or score claim.

Used in: 11-evaluation-observability.md

## constitutional

[Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) — Research paper; cited by initial arXiv year; 2022.

Checked passage: Abstract and method overview.

Scope: Training with principle-guided AI feedback; not a runtime permission mechanism.

Used in: 12-safety-security.md

## dpo

[Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290) — Research paper; cited by initial arXiv year; 2023.

Checked passage: Abstract and method overview.

Scope: Preference-learning objective; no guarantee for downstream tools.

Used in: 12-safety-security.md

## indirect-injection

[Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) — Research paper; cited by initial arXiv year; 2023.

Checked passage: Abstract and method overview.

Scope: Attacks through retrieved content; course threat model is separately stated.

Used in: 12-safety-security.md

## gpt-red

[GPT-Red: Automated Red Teaming via Self-Play at Scale](https://cdn.openai.com/pdf/gpt-red-automated-red-teaming-via-self-play-at-scale.pdf) — Technical paper; official release 15 July 2026; 2026.

Checked passage: Abstract and sections 3–7.

Scope: Self-play and held-out transfer; classroom policy tests are not training replication or general robustness proof.

Used in: 12-safety-security.md

## scientific-report

[Scientific computing in the age of agentic AI: an exploratory field report](https://cdn.openai.com/pdf/scientific-computing-in-the-age-of-agentic-ai-an-exploratory-field-report.pdf) — Exploratory field report; official release 28 July 2026; 2026.

Checked passage: Abstract and verification/stewardship discussion.

Scope: Case studies, not a randomized estimate of student or general productivity.

Used in: 13-production-frontier.md

## acceleration-report

[Research acceleration: The view inside OpenAI](https://openai.com/index/research-acceleration-view-inside-openai/) — Observational research post, 6 September 2026; 2026.

Checked passage: Measurement and interpretation limitations.

Scope: Activity does not by itself identify causal research progress.

Used in: 13-production-frontier.md
