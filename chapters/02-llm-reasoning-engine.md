# 02. The LLM as a Reasoning Engine

> Agents inherit the stochastic, token-based nature of LLMs; prompting, structured output, retrieval, and adaptation compensate for different limitations.

## Learning objectives

- Explain next-token prediction and sampling
- Use major prompting strategies appropriately
- Distinguish prompting, RAG, and fine-tuning
- Design machine-readable outputs for control loops

## Core notes

### The engine predicts one token at a time

An autoregressive LLM defines a probability distribution for the next token given previous tokens, samples one, appends it, and repeats. This makes agent behavior stochastic, gives the model no built-in persistent state, and represents plans, actions, and observations as tokens.

- Low temperature favors predictable control-loop behavior.
- Top-p limits sampling to a probability-mass nucleus.
- Input and output tokens both affect latency and cost.

### The context window is a shared budget

System instructions, tool definitions, retrieved evidence, memory, conversation, and generated reasoning all compete for a fixed window. Agent loops resend a growing transcript, so relevance and compression matter.

- Long contexts cost more and take longer.
- Evidence in the middle may be underused.
- The cheapest token is the one the system does not send.

### The prompt programs behavior in context

In-context learning teaches a task through instructions and examples without changing model weights. A robust prompt separates instruction, context, input, and output indicator; an agent profile also includes tool contracts and the protocol the harness parses.

- Zero-shot is fast but can be brittle on edge cases.
- Few-shot demonstrations stabilize task pattern and format.
- Clear output examples reduce parse failures.

### Different reasoning techniques buy different guarantees

Chain-of-thought externalizes intermediate steps. Self-consistency samples several chains and votes. Program-aided language models generate code and delegate exact computation to an interpreter. Reasoning models spend additional test-time compute on difficult problems.

- Use a single chain for ordinary multi-step reasoning.
- Use voting when a clear answer needs robustness.
- Use executable programs when exact computation matters.
- Pay for deliberate reasoning only on hard steps.

### Structured output closes the software loop

Free-form prose is difficult for a runtime to execute safely. Instructed JSON is brittle; constrained decoding enforces a grammar; native function calling produces provider-enforced structured calls. The runtime must still validate and authorize arguments.

- Schema validity is not semantic correctness.
- Tool descriptions steer selection and argument filling.
- The model requests; application code executes.

### Prompting, retrieval, and fine-tuning solve different problems

Prompting changes behavior quickly. RAG injects current or private knowledge at query time. Fine-tuning changes model behavior in weights; LoRA learns small low-rank adapters and QLoRA combines adapters with a quantized base. Alignment methods such as SFT, RLHF, and DPO target preferred behavior.

- Choose prompting for format, role, or rapidly changing behavior.
- Choose RAG for fresh, private, or citable knowledge.
- Choose fine-tuning for stable behavior at sufficient scale.
- Ground hallucination; do not expect prompting alone to remove it.

## Exam-ready summary

- An LLM is stochastic and stateless; the agent harness supplies control and state.
- Prompt structure and examples are the cheapest adaptation lever.
- Structured output and function calling make generations programmable.
- Prompting, RAG, and fine-tuning are complements, not substitutes.

## Self-test

1. How do temperature and top-p affect an agent loop?
2. What competes for space in the context window?
3. Compare zero-shot, few-shot, chain-of-thought, self-consistency, and PAL.
4. Why is valid JSON insufficient as a security guarantee?
5. When should an engineer choose RAG rather than fine-tuning?
6. What do LoRA and QLoRA change about fine-tuning economics?

## Source basis

This chapter reorganizes and explains material from `02-llm-reasoning-engine.pdf`. It adds study structure and design implications, but introduces no external factual sources.
