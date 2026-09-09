# 10. Advanced Reasoning and Planning

> Reasoning strategies trade inference compute for exploration, correction, or structure; the correct strategy depends on task difficulty and verifiability.

## Learning objectives

- Compare linear, sampled, searched, and reflective reasoning
- Choose a planning strategy
- Explain test-time compute scaling
- Recognize overthinking and faithfulness limits

## Core notes

### A single chain is useful but commits early

Chain-of-thought provides one linear path. It can make intermediate work inspectable, but a greedy chain has no exploration or recovery and its verbalized explanation is not guaranteed to be a faithful record of internal computation.

- Compare a direct baseline with explicit reasoning on the task.
- Verify outputs externally where possible.
- Do not treat stated reasoning as ground truth.

### Self-consistency widens exploration by sampling

Self-consistency samples multiple reasoning paths and aggregates their answers. Separately sampled outputs may share systematic errors. Measure whether voting improves the target task under a declared budget.

- Cost grows roughly with the number of samples.
- Voting requires an answer that can be aggregated.
- Measure shared errors rather than assuming independence.

### Tree- and Graph-of-Thoughts add explicit search

Tree-of-Thoughts generates candidate partial states, evaluates them, and expands promising branches using a search strategy, enabling lookahead and backtracking. Graph-of-Thoughts also merges and refines ideas rather than keeping a strict tree.

- Search needs a useful evaluator.
- Branching can grow exponentially.
- Graphs support aggregation and refinement loops.
- Use search when alternatives and dead ends matter.

### Reflection improves one path over time

Reflexion converts evaluation into a verbal lesson stored for another attempt. Self-Refine repeats critique and revision. Reflection deepens one trajectory, whereas search widens across trajectories.

- A test or grounded critic makes reflection reliable.
- Vague self-critique can reinforce errors.
- Revision loops need quality and cost stops.

### Planning changes when and how decisions are made

ReAct decides step by step and suits short uncertain tasks. Plan-and-execute decomposes first and can reduce repeated planning on long tasks. Re-planning repairs a plan after new evidence. DAG planning runs independent steps in parallel.

- Reactive plans adapt but can be myopic.
- Up-front plans add global structure but can become stale.
- Parallel plans lower latency only when dependencies permit.
- Every planner needs execution feedback.

### Reasoning models internalize deliberate inference

RL-trained reasoning models generate extended internal deliberation and spend test-time compute according to task difficulty. Strong models can serve as planners or orchestrators while cheaper models handle routine extraction, routing, and tool calls.

- More thinking raises latency and cost.
- Easy problems can suffer from overthinking.
- Beyond a point, additional compute may reduce accuracy.
- Escalate selectively instead of using maximum reasoning everywhere.

### Reasoning strategies require controlled comparisons

Compare a direct baseline with sampling or review under a declared resource budget. Separate samples can share systematic errors. Counterfactual prompt edits test a behavioral claim without establishing a complete account of internal computation.

- Choose a scorer before inspecting answers.
- Keep held-out cases out of prompt development.
- Report when extra reasoning fails to help.

## Exam-ready summary

- Self-consistency samples; search branches; reflection revises.
- ReAct, plan-and-execute, re-planning, and DAG execution solve different control problems.
- Reasoning compute should be allocated by difficulty.
- Verbal reasoning is a scaffold, not proof of correctness.

## Self-test

1. Compare chain-of-thought and self-consistency.
2. What are generate, evaluate, and search in Tree-of-Thoughts?
3. How does Graph-of-Thoughts extend a tree?
4. Compare reflection with search.
5. When should an agent use ReAct, plan-and-execute, or parallel planning?
6. What evidence would justify spending more inference on a reasoning strategy?

## Assessed practice

Use Lab 7's paired inputs to test a prediction about a misleading cue. Propose an equal-budget comparison with voting and identify a shared-error failure case.

**Acceptance check:** Keep predictions, observations, and interpretations separate. State the limits of a small experiment.

**Lab:** labs/07_agents_sdk_evaluation.ipynb

## Reading and evidence

- **P3** [Would this change your answer?](https://arxiv.org/abs/2608.16747). Anthropic/Fellows preprint, arXiv v1, 2026-08-17. CHIVE tests counterfactual prompt changes. Generated explanations remain hypotheses. Official post: August 21.
- **R1** [Patterns and problems in emerging multiagent systems](https://www.anthropic.com/research/multiagent-systems). Anthropic research post, 2026-08-13. Controlled coordination experiments. Compare scope and budgets before interpreting the findings.

## Source basis

The original structure follows `10-reasoning-planning.pdf`. The 2026-09-09 edition adds the readings above, protocol clarifications, and assessed practice. Research findings and classroom exercises have different scopes.
