# Designing control flow

## Decomposition as an engineering decision

A large instruction such as “handle this equipment request” combines several kinds of work: interpretation, evidence retrieval, eligibility checking, availability lookup, and communication. Decomposition separates these responsibilities so that each can have a clear input, output, and failure condition. It is useful even when every component uses the same model.

The central question is not how many prompts to create. It is where intermediate results need validation and which decisions should be adaptive. If eligibility is an exact database rule, asking a model to judge it introduces uncertainty into a deterministic step. If the user's description is ambiguous, a language component may be useful before the rule can run.

Anthropic's engineering discussion organizes common workflows as chaining, routing, parallelization, orchestration, and evaluator–optimizer loops [@effective-agents]. We use those names as a vocabulary, then derive their behavior through the equipment case. These patterns describe arrangements of components rather than guaranteed improvements.

## Chains and intermediate contracts

In a chain, the output of one stage becomes input to the next. Our first chain could be interpretation, retrieval, validation, and answer composition. Each transition should have a contract. Interpretation returns a normalized date and requested properties. Retrieval returns records with identifiers and provenance. Validation returns eligible candidates or a structured reason for failure. Composition produces an answer from the validated result.

Intermediate contracts prevent one stage from silently inventing what the next stage needs. If interpretation cannot resolve “next Tuesday,” it returns an unresolved-date status. It does not guess a date to keep the chain moving. A later inventory stage must reject unresolved inputs rather than reinterpret them independently.

A chain creates failure propagation. If the date is wrong, every later operation may be internally correct and still answer the wrong question. Under a deliberately simplified assumption that $k$ stages succeed independently with probabilities $p_1,\ldots,p_k$, complete success has probability:

$$
P(\text{all stages succeed})=\prod_{i=1}^{k}p_i.
$$

For four stages with success probability 0.95 each, the product is approximately 0.8145. Independence is an assumption for this calculation, not a claim about model errors. In practice, a single misinterpreted request can correlate failures across stages. The calculation illustrates why evaluating components separately cannot replace end-to-end evaluation.

## Routing and fallback

A router selects a path based on the request. An exact catalog identifier can go to a lookup path. A policy question can go to retrieval. A request missing required information can go to clarification. Routing is valuable when the paths have genuinely different requirements; otherwise it may add a classification problem without removing much work.

A router needs an explicit fallback. If it must choose among “lookup” and “policy,” a mixed request may be forced into the wrong category. Adding “mixed” is one option. Decomposing the request into independently validated subrequests is another. Asking for clarification may be appropriate when the ambiguity changes the allowed action.

Measure routing mistakes by their consequences. Sending a simple lookup through a slower path wastes resources. Sending a write request through a read-only path might fail harmlessly. Sending a read request into an automatically committing path could cause an unwanted effect. A confusion matrix tells us which labels were confused; a task-specific cost model tells us why the confusion matters.

## Parallel work and joins

Some operations do not depend on each other's outputs. Once the item and date are resolved, policy retrieval and inventory lookup may run in parallel. The join stage waits for the required results and combines them. If each branch has latency $L_i$, a simplified serial latency is $\sum_i L_i$, while ideal parallel latency is $\max_i L_i$ plus coordination overhead.

Parallel execution does not automatically reduce total work. The same two service calls still occur. It may also increase contention or exceed a provider concurrency limit. If one branch fails, the join must decide whether to wait, cancel other branches, produce a partial answer, or fail the request. “Run concurrently” specifies scheduling; it does not specify failure semantics.

A dependency graph makes these choices visible. Interpretation precedes both policy and inventory queries. Eligibility checking depends on policy and identity. Proposal construction depends on eligibility and inventory. An edge means that a result is required, not merely that one box was drawn before another. Removing an edge to make a diagram faster can change the meaning of the task.

## Worked example: the critical path

Suppose interpretation takes 1 second, policy lookup 2 seconds, inventory lookup 3 seconds, and final composition 1 second. Ignore overhead for this invented example. A serial chain takes $1+2+3+1=7$ seconds. If policy and inventory are independent after interpretation, parallel execution takes $1+\max(2,3)+1=5$ seconds.

Now suppose inventory lookup requires a location selected from the policy. The two branches are no longer independent. The 5-second estimate is invalid because it starts inventory before its input exists. The correct sequence returns to 7 seconds under the same durations.

If a third independent branch takes 8 seconds, adding it raises the critical path even though other branches finish early. A fast average branch does not imply a fast join. For user-facing latency, inspect which branch determines completion and whether that branch is essential to the answer.

## Orchestrators and workers

An orchestrator chooses subtasks dynamically and assigns them to workers. In our service, a complex field expedition might require cameras, audio equipment, and power supplies. A coordinator could create separate research tasks after interpreting the request. Each worker should return a bounded result with evidence, unresolved issues, and resource use.

The coordinator owns synthesis. It must detect incompatible assumptions: one worker may interpret the trip as three days while another uses five. Merely concatenating their outputs produces a document with hidden contradictions. A shared task specification should identify dates, locations, eligibility assumptions, and the meaning of completion.

Dynamic decomposition requires bounds on the number of workers and their budgets. A worker should not recursively delegate forever. If each of $b$ workers creates $b$ more workers for $d$ levels, the number of worker nodes grows as a geometric sum. Even a shallow hierarchy can multiply work. Chapter 8 examines the additional information and authority problems created by this structure.

## Review loops and the value of feedback

A reviewer can inspect a proposal and request revision. The useful question is what information allows the reviewer to detect a mistake. A deterministic validator can reject an unknown catalog ID. An independent inventory read can discover stale availability. A second model reading exactly the same incomplete evidence may repeat the same misconception.

Separate **critique generation** from **acceptance authority**. A critique may suggest that the policy citation is weak; a source check determines whether the cited passage actually supports the claim. A revision loop should end when its acceptance criteria pass, its budget expires, or no justified improvement is available. It should not keep rewriting an already correct response solely to sound more polished.

One way to reason about review is to compare expected benefit with overhead. Let $q$ be the probability that the current answer contains a relevant error, $r$ the reviewer's probability of detecting and correcting it, and $h$ the value of avoiding that error. A rough benefit term is $qrh$. This is only a model for planning: the quantities require measurement and the reviewer may introduce new errors. Include that possibility and the extra cost before claiming the loop is beneficial.

## Mapping patterns to LangGraph

A graph representation records nodes, state, and transitions explicitly. In the course implementation, a node performs a bounded piece of work and returns a state update; conditional edges select subsequent work. The framework manages execution, but the application still defines the meaning of state fields and the conditions for completion.

If a retrieval node returns an empty list, the conditional edge can select one repair attempt. If the repaired query also fails, the graph selects abstention. This is an interpretable policy: the repair budget is part of the graph's state, not a vague instruction to “try harder.” Lab 6 implements this pattern, and Chapter 7 adds durable state.

## Exercises

1. Draw a dependency graph for interpreting a request, checking eligibility, checking inventory, and preparing a proposal. Explain every dependency.
2. Recalculate the worked example if policy lookup takes 6 seconds. Give serial and valid parallel latencies, ignoring overhead.
3. Design a router with an explicit fallback for exact lookup, policy question, and mixed request. Describe one costly misroute.
4. A reviewer corrects two answers but breaks one previously correct answer. Explain why counting only corrections overstates its value.
5. Implement a graph that allows at most one query repair. Test an empty first retrieval, an empty second retrieval, and a successful first retrieval.

## Further study and laboratory connection

Use [@effective-agents] to compare pattern names with your control-flow diagram. Lab 6 makes a fixed corrective workflow explicit; Lab 7 examines whether review adds measurable value. Your design report should justify each node by the responsibility it owns and each loop by the failure it can repair.
