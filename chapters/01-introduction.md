# 01. From Language Models to Agents

> Agency appears when an LLM is placed inside a bounded loop with tools, memory, and control logic.

## Learning objectives

- Define classical and LLM-based agents
- Distinguish chatbots, workflows, and agents
- Explain the perceive-reason-act loop
- Choose the least autonomy that solves a task

## Core notes

### The composition changed, not the model paradigm

A classifier maps text to a label and a chatbot maps conversation to a reply. An agent maps a goal to a sequence of actions in an environment and chooses those actions as the task unfolds. The practical shift is the composition LLM + tools + loop + memory.

- Instruction following and function calling make outputs executable.
- Explicit reasoning helps choose and order actions.
- Context and retrieval carry task state and external evidence.

### Classical agency still supplies the core definition

An agent perceives an environment through sensors and acts through actuators. A rational agent selects actions expected to maximize a performance measure given its percepts and knowledge. LLM agents replace a hand-written or learned policy with in-context natural-language reasoning.

- Properties: autonomy, reactivity, pro-activeness, social ability.
- Hard environments are partially observable, stochastic, dynamic, and sequential.
- LLM agents gain generality but inherit reliability, cost, and evaluation problems.

### Four components recur in every implementation

The profile defines identity, constraints, tools, and output protocol. Memory supplies short- and long-term state. Planning turns goals into steps. Action exposes controlled effects through tools. Frameworks mainly differ in how they wire and persist these parts.

- Profile is the behavioral contract.
- Memory is information re-supplied to a stateless model.
- Planning selects the next step or an explicit plan.
- Action is mediated by a validating runtime.

### Agency is a loop, not a single forward pass

The agent observes the goal and environment, reasons about the next step, acts through a tool, receives a new observation, and repeats until completion or a budget limit. The loop turns model output into state-changing behavior.

- Observe: user goal, tool results, environment state.
- Reason: choose the next action from current evidence.
- Act: request a tool call through the runtime.
- Stop: final answer, step cap, cost cap, time cap, or human escalation.

### Control flow separates chatbots, workflows, and agents

A chatbot produces a reply without actions. A workflow follows code-defined paths that may contain LLM calls and tools. An agent lets the model dynamically direct process and tool use. This is a spectrum rather than a binary label.

- Workflows are more predictable, testable, and economical.
- Agents are more flexible when the correct path cannot be written in advance.
- Moving toward autonomy raises variance, latency, cost, and safety surface.

### The engineering rule is minimum sufficient autonomy

Start with a single call or fixed workflow and add model-directed decisions only when the task requires them. Narrow scope, explicit evaluation, and human checkpoints are more reliable than an open-ended agent that can do anything.

- Use execution-grounded tasks where success can be checked.
- Bound long horizons because errors compound.
- Treat the production agent as a stack: model, tools, state, orchestration, eval, and guardrails.

### A baseline makes autonomy a testable choice

Choose a small task with observable success before building an agent. Compare a fixed workflow with a model-directed loop on the same inputs. Treat the decision to add autonomy as an engineering hypothesis.

- Write expected outputs before implementation.
- Keep task inputs and resource limits comparable.
- Retain the simpler design when it meets the requirements.

## Exam-ready summary

- Agent = LLM reasoning core + tools + loop + memory.
- Profile, memory, planning, and action are the reusable anatomy.
- Autonomy is a design variable; choose the leftmost workable point.
- Reliability comes from the system around the model.

## Self-test

1. Give the classical definition of an agent and reframe it for an LLM system.
2. Why is an agent a composition rather than a new model paradigm?
3. Compare chatbot, workflow, and agent by control flow and tool use.
4. Name the four agent components and the responsibility of each.
5. Why are typical LLM-agent environments difficult?
6. How would you test whether a fixed workflow is sufficient for a task?

## Assessed practice

Choose a catalog lookup or arithmetic task. Write six cases, including empty input and an unknown item. Define a pass condition and a call limit. Explain what dynamic decision, if any, needs a model.

**Acceptance check:** Submit the cases and an architecture choice before running a model. Credit follows the evidence, including a decision to keep a fixed workflow.

**Lab:** labs/05_gemini_bounded_tools.ipynb

## Reading and evidence

Use the classroom baseline and its explicit acceptance tests. This activity is a teaching design.

## Source basis

The original structure follows `01-introduction.pdf`. The 2026-09-09 edition adds the readings above, protocol clarifications, and assessed practice. Research findings and classroom exercises have different scopes.
