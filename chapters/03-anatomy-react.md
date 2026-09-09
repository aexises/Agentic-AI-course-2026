# Agent anatomy and the execution loop

## Why a loop is needed

The equipment assistant does not know whether a requested item is available until it queries inventory. The inventory response may reveal that the only matching camera is already booked. A second decision is then required: search alternatives, ask whether the date can change, or end with an unavailable result. A single model response cannot observe the outcome of a tool that has not yet run.

ReAct interleaves model-generated reasoning and actions with observations returned from an environment [@react]. The architectural idea is that later decisions can incorporate newly obtained evidence. In a deployed system, we need to make this loop explicit enough that software can verify what was proposed, what actually executed, and why the run stopped.

We will use a simplified trace. The model requests `inventory_lookup` for an item and date. The runtime validates the request and calls the tool. The tool returns a structured unavailable result. The runtime appends that observation to the conversation. The model can then request a different lookup or give an honest final answer. The observation must come from the actual tool execution; a model-generated sentence beginning “Observation:” is not a substitute.

## Components and responsibilities

An agent profile includes task instructions, available tool descriptions, output requirements, and relevant limits. The model uses this profile and current context to propose a next step. A dispatcher maps an allowed tool name to an implementation. The implementation accesses the environment. A state manager records conversation and execution state. A controller decides whether to continue, stop, request input, or escalate.

These responsibilities should be visible even when a framework packages them together. A failure in the tool implementation is not fixed by changing the model's role description. A missing observation is not fixed by improving retrieval ranking. Separating components lets us test each boundary with controlled inputs.

For example, a dispatcher should use the registry passed to it. If a test injects a fake inventory tool but dispatch still reaches a global production registry, the test cannot isolate the behavior. Dependency injection means supplying the dependency explicitly so that a test can replace it. It is an architectural property, not merely a testing convenience.

## Text protocols and structured tool calls

A historical teaching loop might parse strings such as `Action: lookup[C17]`. This is easy to inspect but has ambiguity: a reply can contain several action markers, malformed brackets, or a fabricated final answer after an action. A parser must define which forms are accepted and reject ambiguous combinations. A stop sequence can help control generation format where the provider supports it, but it does not validate arguments or enforce permissions.

Structured function calling gives the runtime a more explicit request representation. A tool declaration describes a name and argument schema. The returned request is still only a proposal. The runtime checks the requested tool, validates arguments, performs any authorization, and constructs the corresponding tool result. Google's documentation describes this request/result cycle for Gemini; preserving the returned model content and tool-call correspondence is important to the protocol [@gemini-tools].

A useful mental model is a correspondence table: request identifier, tool name, arguments, execution status, and result. When a response contains multiple calls, each result must be attached to its matching request. Reordering results without preserving that relationship can cause a correct calculator value to be interpreted as an inventory answer.

## A bounded controller

The following is pseudocode. It specifies behavior without claiming to implement a particular SDK.

```text
state = initial_request_and_instructions
while model_requests < request_limit and before_deadline:
    reply = ask_model(state)
    record(reply)
    if reply contains a valid final response and no pending calls:
        return validate_final(reply)
    calls = parse_and_validate_requests(reply)
    if calls are empty:
        return failure("no usable response")
    for call in calls:
        if tool_budget_exhausted:
            return failure("tool budget")
        result = authorized_dispatch(call)
        state = append_matching_result(state, call, result)
return failure("request limit or deadline")
```

The pseudocode deliberately separates model requests from tool calls. One model response may contain several tool requests; conversely, a model request may produce no tool call. A request limit of four therefore does not imply a tool-call limit of four. A practical controller tracks both, as well as elapsed time and output size.

The controller must decide what to do when a call fails. An unknown tool is a validation failure. A network timeout is an infrastructure failure. An unavailable item is a valid domain result. Returning the same generic “error” for all three removes information the next decision needs. Error records should be structured, bounded, and free of secrets.

## Worked example: a complete tool round-trip

Suppose the model proposes request `r1`: look up camera C17 for date D. The dispatcher verifies that the item identifier and date are valid and that the authenticated user may read this inventory. The tool returns `available = false`. This result is stored with request ID `r1`. The next model input contains the original request, the proposed call, and its actual result.

The model then proposes `r2`: look up camera C18 for D. That tool returns `available = true`. The model's final answer recommends C18 and explains that availability was observed, while the booking remains uncommitted. We can now assess both the final answer and its trajectory: two inventory calls, no reservation effect, and two matching observations.

Consider an incorrect implementation that runs the first tool and prints its result, then ends. A human reading the notebook may infer the next step, but the model has not received the result. The implementation has demonstrated dispatch, not a complete model–tool–model cycle. This distinction is why Lab 5 asserts properties of the second model request rather than merely checking printed output.

Now consider a response containing three calls when only two tool calls remain. The runtime needs an explicit policy. It can reject the batch before execution, or execute a permitted prefix and return a budget stop. Either choice must be documented; silently executing all three violates the stated budget. For operations with effects, partial execution also requires a record of exactly which operations occurred.

## Invariants and termination

An invariant is a condition that must remain true across state transitions. For a tool loop, useful invariants include: every executed call passed validation; every recorded successful result corresponds to an actual execution; every result matches an issued request; and no call executes after its budget is exhausted.

Termination also needs an invariant about progress or resources. “Repeat until the model is satisfied” is not a bound. A hard counter can ensure that the loop eventually stops, provided individual operations also terminate or time out. An iteration cap alone cannot stop a single blocking network request. Bounded loops and bounded operations solve different problems.

A successful terminal state should not conceal unresolved calls. If the model returns both a final answer and pending actions, the controller needs a deterministic rule rather than accepting whichever part appears first. The repaired text loop chooses strict parsing; the native loop follows the provider protocol and explicit application limits. The exact rule can vary, but ambiguity must not decide execution.

## Testing without a model account

A scripted fake model can return a call on its first invocation and inspect the observation on its second. This tests that the application constructs the correct next request. A fake tool can return unavailable, raise a timeout, or reject an invalid argument. These fixtures exercise the state machine without relying on live sampling.

Such tests establish the behavior of the controller under the scripted inputs. They do not establish how often Gemini chooses a valid tool or how it behaves on unseen requests. Live tests are a separate layer. Confusing these layers would make a perfect fixture pass rate look like model accuracy.

## Exercises

1. Draw the sequence for two inventory calls followed by a final answer. Mark the author of each message: user, model, runtime, or tool.
2. A model response requests five tools and the request cap is three. Explain why the model-request cap alone does not prevent five executions.
3. Define terminal statuses for malformed output, unavailable inventory, timeout, permission denial, and successful completion. Which are valid task outcomes?
4. Write a fake-model test that fails if the second model request omits the first tool result. Add an unknown-tool case and a zero-budget case.
5. Explain how a loop with a finite iteration count can still hang. Specify the additional bound required.

## Further study and laboratory connection

Read the architecture in [@react], then work through the repaired ReAct foundation and Lab 5. The lab's native protocol is a modern implementation exercise, not a reproduction of the original paper's benchmark. In your report, include one successful trace, one infrastructure failure, and one budget stop, with no invented observations.
