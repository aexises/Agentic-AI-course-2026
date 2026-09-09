# From language models to agents

## A problem before an architecture

Suppose a student asks the equipment service for a camera. A text model can produce a plausible recommendation from the words in the question. That response may be useful, but it does not establish that the camera exists in the university catalog, is available on the requested date, or may be borrowed by this student. These are facts about an environment. The model needs a way to observe that environment, and the application needs rules governing what it may change.

Start by separating the user's intention from a successful outcome. “Help with a camera” expresses an intention. “Return an available item identifier, cite the applicable loan policy, and prepare an uncommitted reservation proposal” is an operational specification. The second statement allows a reviewer to inspect completion. It also prevents the application from interpreting helpfulness as permission to commit a reservation.

An architecture should follow this specification. If every request consists of an exact item identifier and a date, ordinary database lookup may solve the task. If requests are expressed informally, a model may be useful for extracting fields. If the next query depends on information discovered during execution, a model-directed loop may be justified. Autonomy is a design choice about who selects the next operation, not a quality score.

## State, observation, action, and policy

We use four terms precisely. **State** is information relevant to the system at a particular time. **Observation** is information received from the environment. **Action** is an operation the system attempts. **Policy** is a rule for selecting actions from available information. In an LLM application, the model can implement part of the action-selection policy, while application code enforces the allowed action set.

Let $s_t$ represent the application's recorded state after step $t$, and let $a_t$ be its proposed next action. A simplified loop is:

$$
a_t \sim \pi_{\theta}(\cdot\mid s_t),\qquad o_{t+1}=\operatorname{execute}(a_t),\qquad s_{t+1}=\operatorname{update}(s_t,a_t,o_{t+1}).
$$

The symbol $\pi_{\theta}$ denotes the model-dependent policy, with parameters $\theta$. The symbol $\sim$ means that the action is drawn from a distribution. This notation does not say that the model knows the true state of the world. The recorded state might contain an inventory observation from ten minutes ago. It might omit another department's reservations. A more complete model would distinguish hidden environmental state from the application's information about it.

That distinction matters operationally. If an inventory lookup says “one camera available,” the system has observed availability at the time and scope of that lookup. It has not secured the camera. Another user may reserve it before the next action. The reservation service must check availability again when it commits a booking. Reasoning with a recent observation cannot replace transactional validation.

## Chatbots, workflows, and agents

These categories describe control, and real applications can combine them. A reply-only chatbot produces a response. A workflow follows transitions selected by application code. A model-directed agent can choose its next operation from a permitted set based on the evolving task state. Anthropic's engineering account distinguishes predefined workflows from systems in which models direct their own process and tool use; it recommends beginning with simple implementations [@effective-agents].

Consider three equipment applications. The first answers policy questions from text pasted into the conversation. The second always extracts a date, retrieves matching catalog items, checks inventory, and formats a result. The third can decide to clarify an ambiguous date, inspect a different policy, or search another catalog after observing an empty result. The third has more adaptive control, but also more possible trajectories that require testing.

A workflow can contain a model-directed subtask. For example, the overall reservation process may always end at an approval gate, while a bounded search component chooses which catalog query to try next. Describing this as a hybrid is often more useful than arguing whether the whole system deserves the label “agent.” A control-flow diagram should show which transitions are deterministic and which depend on model proposals.

## Turning a goal into a contract

A useful task contract specifies inputs, acceptable outputs, permitted effects, stopping conditions, and uncertainty behavior. For our service, the input includes the user's request and authenticated identity. The output includes candidate items, source references, and a reservation proposal. Read-only catalog access is permitted. A committed reservation requires a separate authorization decision. The run ends on completion, lack of evidence, an unresolved ambiguity, a denied action, or exhausted resources.

Notice that “ask for clarification” and “cannot establish availability” can both be correct terminal outcomes. A system that always returns a confident item name may score well on superficial fluency while violating the real task. Success criteria should reward appropriate abstention when the information needed for a valid decision is missing.

We can represent a design objective as:

$$
\max_{\pi}\;\mathbb{E}[U]\quad\text{subject to}\quad C\leq B,\quad T\leq D,\quad a_t\in\mathcal{A}(s_t).
$$

Here $U$ is task utility, $C$ is cost, $B$ is a cost budget, $T$ is elapsed time, $D$ is a deadline, and $\mathcal{A}(s_t)$ is the set of actions allowed in state $s_t$. The expectation averages over uncertain outcomes. This is a conceptual specification, not an optimization algorithm supplied by the SDK. It helps us see why maximizing answer quality alone is incomplete: a highly capable trajectory can still exceed the budget or attempt an unauthorized action.

## Worked example: choosing the minimum sufficient system

Imagine a teaching dataset of twenty requests. Twelve contain exact item identifiers; five describe a use case without an identifier; three omit the date. These counts are invented for the example. A database baseline handles the twelve exact lookups. A model extraction stage may interpret the five descriptions. The three missing-date requests must return a clarification request before availability can be established.

A reasonable first design therefore has a deterministic validation stage, an optional language interpretation stage, and a deterministic inventory query. It does not need an open-ended planning loop. We evaluate whether that design returns the right item, asks for missing dates, and preserves the distinction between proposal and booking. Only failures requiring adaptive search motivate adding a loop.

Suppose the model-directed alternative succeeds on one extra descriptive request but makes six more model calls per request. The extra success may justify the cost for some tasks. It does not establish that the agent is universally better. We need the cost of the additional calls, the harm of incorrect matches, the frequency of that request type, and the performance of a cheaper targeted repair.

The example teaches a general method: identify a concrete failure of the simpler system, add a component that could address it, and measure whether the component changes that failure. Adding autonomy without such a hypothesis makes both evaluation and debugging harder.

## What makes these environments difficult?

An equipment task can be partially observed, because availability and eligibility come from different services. It can be dynamic, because inventory changes during execution. It can be stochastic from the application's perspective, because model output and network behavior vary. It can involve other decision-makers, because students and coordinators compete for shared resources. These properties are separate: a deterministic tool can operate on changing data, and a fixed dataset can still receive stochastic model answers.

Each property suggests a different response. Partial information calls for explicit uncertainty and targeted observation. Dynamic state calls for timestamps and validation at commitment. Stochastic behavior calls for repeated evaluation and bounded retries. Shared resources call for concurrency control and ownership. The phrase “agents are unpredictable” is too broad to guide implementation; naming the source of uncertainty turns it into an engineering question.

## Exercises

1. Write a task contract for an assistant that recommends readings for a student but cannot enroll the student in a course. Identify two correct non-answer outcomes.
2. Classify an application that uses a model to extract fields and then follows a fixed database transaction. Explain which component, if any, chooses its next operation dynamically.
3. In the equipment example, explain why a successful inventory read cannot authorize a booking. Describe the check required at commit time.
4. Design five evaluation cases for a baseline equipment assistant. Include an ambiguous request, a missing date, and an unavailable item. Define success for each before writing a prompt.
5. Extension: propose one adaptive search behavior that could improve the baseline. State the specific failure it addresses and the extra resources it consumes.

## Further study and laboratory connection

Read the short workflow/agent distinction in [@effective-agents], then inspect the model–action–observation structure introduced by ReAct [@react]. The reading establishes architectural ideas, not a performance estimate for this course's service. Before Lab 5, submit the task contract and baseline cases from this chapter. They will later determine whether a tool loop does useful work.
