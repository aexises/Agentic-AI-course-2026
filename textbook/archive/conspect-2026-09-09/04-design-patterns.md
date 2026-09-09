# 04. Agentic Design Patterns

> The best architecture keeps control in code when possible and hands decisions to models only where dynamic judgment adds value.

## Learning objectives

- Recognize five workflow patterns
- Compare workflow and agentic control
- Compose patterns into a system
- Estimate reliability and cost trade-offs

## Core notes

### The augmented LLM is the reusable building block

Retrieval, tools, and memory turn a plain model call into an augmented LLM. Design patterns connect one or more augmented LLMs with control flow. The central design question is whether code or the model decides what happens next.

- Code-directed workflows are predictable and testable.
- Model-directed agents are flexible but variable.
- Add autonomy only when decisions cannot be enumerated reliably.

### Chaining and routing encode known structure

Prompt chaining applies fixed ordered steps and can place validation gates between them. Routing classifies an input and selects a specialized handler. Both retain explicit control paths.

- Chaining fits outline-draft-polish style sequences.
- Gates can check schema, rules, or quality.
- Routing needs calibrated accuracy and a fallback lane.
- Hard or low-confidence cases can escalate.

### Parallelization trades compute for speed or reliability

Sectioning divides independent work and aggregates results, reducing wall-clock time. Voting runs the same task several times and aggregates answers, increasing cost in exchange for robustness.

- Parallelize only independent subtasks.
- Aggregation is a distinct step that can fail.
- Reserve voting for decisions where redundancy is worth the cost.

### Orchestrator-workers creates subtasks dynamically

An orchestrator decomposes the current input, dispatches variable subtasks to workers, and synthesizes their outputs. Unlike a chain, the exact work plan is not known in advance.

- Workers may be prompts, tools, or complete agents.
- The orchestrator must track state and integrate results.
- Dynamic decomposition increases flexibility and evaluation burden.

### Evaluator-optimizer and reflection require grounded criteria

A generator produces an attempt, an evaluator checks it, and feedback drives revision. The loop improves reliably when criteria are externally verifiable, such as tests, schemas, calculations, rubrics, or reference answers.

- Vague 'is this good?' critics may rubber-stamp outputs.
- Tool-grounded critics can verify objective properties.
- Every refinement loop needs a stop and cost budget.

### Patterns compose, so failure controls must compose too

A router can select an agent, an orchestrator can dispatch ReAct workers, and an evaluator can check the synthesis. Humans can approve, correct, or receive escalations at consequential boundaries.

- Anti-patterns: agent where workflow suffices, too many tools, unbounded loops.
- Each additional model call increases cost and failure opportunity.
- Use the simplest pattern whose control assumptions match the task.

### An extra stage must justify its cost

A reviewer or worker adds another opportunity to help and another opportunity to fail. Use identical cases to compare a baseline with the proposed composition. Count review and coordination calls when evaluating the whole system.

- Use a fixed baseline before changing the architecture.
- Score outcomes and failures with the same rules.
- Account for overhead even when review leaves the answer unchanged.

## Exam-ready summary

- Patterns connect augmented LLMs with different control structures.
- Chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer are workflows.
- Tool use, reflection, planning, and multi-agent systems hand more control to models.
- Ground checks and budgets at every loop boundary.

## Self-test

1. What distinguishes a workflow from an agent?
2. Compare prompt chaining and orchestrator-workers.
3. Name the two forms of parallelization and their goals.
4. Why do evaluator-optimizer loops need verifiable criteria?
5. Give a valid composition of three patterns.
6. How can a reviewer increase cost without increasing correctness?

## Assessed practice

Compare a single catalog agent with an objective evidence check. Specify when an LLM reviewer would add information that the objective check lacks.

**Acceptance check:** Include a case where review adds no value and one where it changes an incorrect proposal. Count all calls in the live variant.

**Lab:** labs/07_agents_sdk_evaluation.ipynb

## Reading and evidence

- **R1** [Patterns and problems in emerging multiagent systems](https://www.anthropic.com/research/multiagent-systems). Anthropic research post, 2026-08-13. Controlled coordination experiments. Compare scope and budgets before interpreting the findings.

## Source basis

The original structure follows `04-design-patterns.pdf`. The 2026-09-09 edition adds the readings above, protocol clarifications, and assessed practice. Research findings and classroom exercises have different scopes.
