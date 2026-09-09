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

- Compare direct answers and reasoning prompts on the target task.
- Test voting against a baseline with a declared call budget.
- Use executable programs when exact computation matters.
- Pay for deliberate reasoning only on hard steps.

### Structured output closes the software loop

Structured-output support varies by provider, model, and schema. Native function calling supplies a protocol for tool requests. The application must validate arguments, check policy, and handle invalid or incomplete responses.

- Schema validity is not semantic correctness.
- Tool descriptions steer selection and argument filling.
- The model requests; application code executes.

### Prompting, retrieval, and fine-tuning solve different problems

Prompting changes behavior quickly. RAG injects current or private knowledge at query time. Fine-tuning changes model behavior in weights; LoRA learns small low-rank adapters and QLoRA combines adapters with a quantized base. Alignment methods such as SFT, RLHF, and DPO target preferred behavior.

- Choose prompting for format, role, or rapidly changing behavior.
- Choose RAG for fresh, private, or citable knowledge.
- Choose fine-tuning for stable behavior at sufficient scale.
- Ground hallucination; do not expect prompting alone to remove it.

### Behavioral claims need an external check

CHIVE investigates model behavior by editing prompts and measuring the resulting responses. In this course, a plausible explanation is a hypothesis to test. Schema checks, factual checks, and policy checks answer different questions.

- Predict the effect of one prompt edit.
- Score the response with a stated criterion.
- Distinguish measured behavior from a causal explanation.

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
6. Why can a valid schema and a plausible explanation still accompany a wrong answer?

## Assessed practice

Keep a factual task fixed and add one misleading cue. Predict whether the answer will change. Record both conditions and identify which check tests structure, evidence, or policy.

**Acceptance check:** The submission contains paired inputs and a testable prediction. It does not treat verbal reasoning as ground truth.

**Lab:** labs/07_agents_sdk_evaluation.ipynb

## Reading and evidence

- **P3** [Would this change your answer?](https://arxiv.org/abs/2608.16747). Anthropic/Fellows preprint, arXiv v1, 2026-08-17. CHIVE tests counterfactual prompt changes. Generated explanations remain hypotheses. Official post: August 21.
- **S4** [Gemini structured outputs](https://ai.google.dev/gemini-api/docs/structured-output). Google documentation, accessed, 2026-09-09. Supported schemas constrain structure. Application validation must check meaning and policy.

## Source basis

The original structure follows `02-llm-reasoning-engine.pdf`. The 2026-09-09 edition adds the readings above, protocol clarifications, and assessed practice. Research findings and classroom exercises have different scopes.
