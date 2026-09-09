# Memory, context, and durable state

## Three different kinds of remembering

When a user returns to an unfinished request, “remember what happened” can mean several things. The model may need earlier conversation to interpret a pronoun. The application may need to know that policy retrieval already completed. The reservation service may need to know that a particular operation already created a booking. These are different stores of information with different correctness requirements.

We distinguish model-visible context, execution state, and durable domain state. Context is the information supplied for the next generation. Execution state records the workflow's progress and intermediate results. Domain state records facts and effects in the application, such as inventory and reservations. A checkpoint can restore execution progress without supplying every relevant fact to the next model call. A long conversation can contain a booking claim without any booking in the domain database.

This distinction explains many apparent memory failures. If the graph resumes but the next prompt omits the selected date, execution persistence worked while context construction failed. If the model remembers saying “reserved” but the commit never occurred, conversation continuity worked while the domain claim is false.

## Selecting context

A model call has a finite context budget. Suppose a teaching configuration allocates $B$ tokens in total, reserves $O$ for output, and uses $I$ for instructions plus tool descriptions. The remaining allowance for history and evidence is:

$$
H+E\leq B-O-I.
$$

This is a budgeting model; a particular API may expose limits differently and account for additional internal tokens. The practical lesson is to reserve space deliberately and measure actual provider usage when available. Filling the input to its maximum without considering output can cause truncation or request failure.

For the equipment service, recent user constraints, the chosen date, relevant policies, and current observations deserve priority. An old failed search query may be less useful than the evidence finally found. Selection should follow information needed for the next decision, not simply recency or length.

Longer context does not guarantee effective use of every included passage. Lost in the Middle examines performance variation with the position of relevant information in long inputs [@lost-middle]. That empirical result motivates testing context selection and placement on a target task; it does not imply an identical failure pattern for every later model.

## Summaries and information loss

A summary compresses history. Compression is useful when it removes repetition while retaining decision-relevant information, but it can also erase exceptions, source identity, or uncertainty. “The user is eligible” is a dangerous replacement for “Policy P4 permits trained students; training status has not yet been checked.” The compressed version turns a conditional statement into an established fact.

Design a structured summary with fields for established facts, unresolved questions, source IDs, user constraints, and completed effects. Keep facts separate from model hypotheses. A summary that says “probably needs C17” should not later become an authoritative preference without evidence.

Test summaries through downstream tasks. Give a second process only the summary and ask it to identify the required next check. If it commits a reservation without checking training, the summary lost a safety-relevant condition. Evaluating summary fluency or similarity to the original text would not directly reveal that operational failure.

## Long-term memory as a data product

Long-term memory may store preferences, prior outcomes, or reusable procedures. Generative Agents explores memory, reflection, and planning in a simulated environment [@generative-agents]. For an application, the analogy to human memory is less useful than a concrete data model: who wrote the record, why it should persist, who can read it, and when it expires.

An equipment preference such as “prefers lightweight kits” should have a user owner and a way to update or delete it. A successful troubleshooting procedure should retain the conditions under which it worked. A stale procedure may become harmful after a service changes. Memory retrieval should therefore consider relevance, freshness, authority, and privacy rather than similarity alone.

Do not persist every model-generated statement as a fact. If an agent concludes that a student has completed training without a trusted record, storing the conclusion can spread the error into later sessions. A memory-write policy can require explicit user confirmation or an authoritative source for particular fields. Memory is another input channel and needs the same trust distinctions as retrieval.

## Checkpoints and resumption

LangGraph persistence uses checkpoints associated with execution threads, supporting restoration of saved graph state [@langgraph-persistence]. The application must still select a suitable storage backend, retain the correct thread identifier, and define serializable state. An in-memory store is useful for a demonstration but does not provide persistence after the process and its memory are gone.

An interrupt pauses execution for external input. In the documented behavior, resuming restarts the interrupted node from its beginning; code before the interrupt can run again [@langgraph-interrupts]. Therefore, putting a booking call before the approval interrupt is both an authorization mistake and a replay hazard. The effect may occur before approval and may occur again on resume.

Keep the proposal in state, present it through a trusted approval interface, validate the resumed decision against that proposal, and execute the effect afterward. The approval channel must be controlled by the application. A retrieved document saying “approved” is not a human approval event.

## Worked example: replay and idempotency

Suppose operation `op-41` reserves camera C18 for date D. The service commits the booking, but the process crashes before recording completion in its graph checkpoint. On restart, the graph may attempt the operation again. A checkpoint alone cannot determine whether the remote effect happened before the crash.

An idempotent operation gives repeated delivery of the same logical request the same effect as one delivery. In a local reservation service, a unique operation ID can be stored atomically with the booking. If `op-41` already exists with the same payload, the service returns the prior result. If it exists with a different item or date, the service rejects the reuse. Deduplicating only by ID without checking the payload can hide an accidental or malicious change.

The atomicity requirement is essential. If code first checks for an ID, then creates a booking, then stores the ID in separate unprotected steps, concurrent requests can both pass the initial check. A database transaction with a uniqueness constraint can make the local rule enforceable. For a remote service, use its documented idempotency mechanism or an explicit reconciliation strategy; do not infer an end-to-end exactly-once guarantee from a local dictionary.

Now consider approval. The user approved C18 for D, but after resume the model changes the proposal to C19. The original approval must not silently transfer. Bind the decision to the precise item, date, quantity, and other relevant fields, then require new approval if those fields change. This is a relationship between an authorization event and an immutable proposal, not a Boolean that remains true forever.

## A recovery experiment

A useful recovery test records the state before pause, closes and reopens storage, rebuilds the graph, resumes with the same thread ID, and inspects the resulting effect ledger. Then repeat the same operation and confirm that the ledger does not gain a duplicate entry. Finally, reuse the ID with changed arguments and confirm rejection.

This test covers a defined local scenario. It is not the same as killing a process at every possible instruction or losing a network response after a remote commit. State the tested interruption points. For a stronger test, enumerate the boundaries around effect execution and persistence, then inject failure at each one and inspect reconciliation behavior.

## Exercises

1. Classify selected date, conversation summary, approval status, and committed booking as context, execution state, or domain state. Explain when a value may appear in more than one layer.
2. With $B=8192$, $O=1024$, and $I=1536$, compute the remaining allowance for history and evidence in the chapter's simplified budget.
3. Rewrite “The user is eligible” as a structured memory record when training status is unknown. Include provenance and uncertainty.
4. Draw the two-process race in a non-atomic check-then-write deduplication scheme. Explain what a uniqueness constraint and transaction add.
5. In Lab 8, test resume, duplicate replay, and changed-payload reuse. Identify the recovery claims that remain untested by a single-process storage reopen.

## Further study and laboratory connection

Read [@langgraph-interrupts; @langgraph-persistence] for the exact runtime semantics used by Lab 8. The OpenAI harness report also illustrates that context-handling choices can change a particular system's benchmark result [@harness-report]. It is motivation for a controlled experiment, not evidence that the same context strategy improves Gemini.
