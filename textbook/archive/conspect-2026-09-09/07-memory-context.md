# 07. Memory, State, and Context Engineering

> Memory is an engineered system that curates a bounded context, persists selected experience, and governs recall, expiry, and access.

## Learning objectives

- Classify agent memory
- Manage short-term context
- Design deliberate long-term writes and reads
- Evaluate memory quality and governance

## Core notes

### Stateless models require explicit state engineering

An LLM knows only the current context. Long tasks and multiple sessions therefore need a system that decides what stays in the window, what moves to external storage, and what is retrieved later.

- The context is bounded, costly, and imperfectly used.
- Nothing persists across calls unless the application stores it.
- Memory architecture is a set of selection policies.

### Short-term and long-term memory have different mechanics

Short-term memory is working context: instructions, tools, evidence, and recent trace. Long-term memory is external and can hold episodic events, semantic facts, and procedural knowledge across sessions.

- Episodic: past interactions and outcomes.
- Semantic: facts and stable preferences.
- Procedural: instructions or learned methods.
- Long-term storage is useful only if recall is selective.

### Short-term memory must be actively compressed

Truncation drops old turns, summaries compress them, selective recall retrieves only relevant history, and a structured scratchpad keeps the plan and current state visible. These mechanisms can be combined.

- Rolling summaries preserve gist but may drift.
- Recent detail can remain verbatim.
- Conversation retrieval is RAG over history.
- A scratchpad reduces repeated reasoning and goal loss.

### Long-term memory needs write and read policies

Store durable signal rather than every event. Writes can occur on explicit request, at task completion, through reflection, or continuously for changing state. Reads can use keys, recency, or semantic similarity.

- Prefer stable preferences, durable facts, outcomes, and lessons.
- Deduplicate and resolve contradictions.
- Attach timestamps, provenance, and expiry.
- Reflective consolidation turns noisy episodes into higher-level memories.

### Context engineering treats tokens as scarce capacity

More context is not automatically better. Low-relevance history raises cost and latency and can create context rot. Long-context models provide more room but do not create cross-session persistence, selective recall, consent, or governance.

- Relevance beats volume.
- Place critical instructions and evidence deliberately.
- Virtual-context architectures page information between window and store.
- Retrieval-based architectures recall memories by relevance.

### Memory is also a privacy and security system

Persistent data requires consent, minimization, retention limits, deletion, and access control. Memory can become stale, contradictory, poisoned, or unbounded, so it needs evaluation and maintenance.

- Recall: retrieve the right memory at the right time.
- Faithfulness: use the memory correctly.
- Forgetting: expire stale or irrelevant items.
- Security: prevent unauthorized access and malicious persistence.

### Execution state and model context serve different purposes

A checkpoint stores workflow state for resumption. A context policy chooses what the next model call can see. Test these mechanisms separately. OpenAI's harness experiment motivates recording context settings as part of the evaluated system.

- Reopen a checkpoint before resuming approval.
- Keep side effects after the approval boundary.
- Compare context policies without changing the task set.

## Exam-ready summary

- Memory is context plus external stores and policies.
- Short-term memory is curated; long-term memory is deliberate.
- Long context complements but does not replace memory.
- Recall, consolidation, expiry, consent, and access control are first-class.

## Self-test

1. Why does an LLM need an application-level memory system?
2. Compare episodic, semantic, and procedural memory.
3. What are four ways to manage a full context window?
4. When should an agent write a long-term memory?
5. Why does a million-token context not eliminate memory architecture?
6. How can a workflow resume correctly while its next model call still lacks needed context?

## Assessed practice

Complete Lab 8's checkpoint test. As an extension, compare a fixed recent-history window with a structured task summary on the same lookup tasks.

**Acceptance check:** Show the pending state before resume and one committed effect after a retry. Do not generalize a context-policy result across providers.

**Lab:** labs/08_langgraph_approval_security.ipynb

## Reading and evidence

- **S3** [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts). LangChain documentation, accessed, 2026-09-09. Resume restarts the interrupted node. Put effects after approval and make replay safe.
- **R2** [How enabling two settings tripled our scores on the ARC-AGI-3 benchmark](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/). OpenAI research post, 2026-07-29. A specific harness experiment. Its result does not estimate the effect of context changes in Gemini.

## Source basis

The original structure follows `07-memory-context.pdf`. The 2026-09-09 edition adds the readings above, protocol clarifications, and assessed practice. Research findings and classroom exercises have different scopes.
