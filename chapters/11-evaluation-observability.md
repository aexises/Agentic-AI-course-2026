# 11. Evaluation and Observability

> Agent quality requires systematic measurement of both final outcomes and the trajectories that produced them, supported by complete traces.

## Learning objectives

- Design outcome and trajectory metrics
- Read benchmarks critically
- Use LLM judges with safeguards
- Build offline, online, and CI evaluation

## Core notes

### Agent evaluation is difficult for structural reasons

Runs are non-deterministic, outputs are open-ended, tasks are multi-step, and correctness, cost, latency, and safety can conflict. Models, tools, and prompts also change, so anecdotal testing cannot distinguish progress from regression.

- Use repeated runs where variance matters.
- Define several metrics rather than one headline score.
- Version the complete system under evaluation.

### Outcome and trajectory answer different questions

Outcome evaluation asks whether the final answer or task result is correct. Trajectory evaluation asks whether the agent used appropriate tools, safe actions, efficient steps, and acceptable time and cost.

- Exact match suits unambiguous answers.
- Execution tests suit code and queries.
- Trajectory metrics localize the failing step.
- Safety and policy adherence belong in trajectory evaluation.

### Objective scorers are preferable where available

Execution-based and exact scoring are easier to reproduce than reference similarity or an LLM judge. For RAG, retrieval and generation need separate metrics; for memory and multi-agent systems, evaluate recall, handoffs, agent-specific errors, and total cost.

- RAG: retrieval recall/precision/MRR plus faithfulness and relevance.
- Memory: right item, right time, correct use, appropriate forgetting.
- Multi-agent: handoff quality, ownership, synthesis, and call budget.

### Benchmarks measure systems, not just base models

GAIA tests multi-step assistant behavior, SWE-bench Verified tests repository issue resolution through execution, and tool-dialogue benchmarks test policy adherence. Scores depend on the model, prompt, tools, interface, scaffold, and evaluation harness.

- Watch for training-data contamination.
- Weak tests may accept incorrect solutions.
- Benchmark tasks may not match production distribution.
- Ask whose system produced the number.

### LLM-as-judge is flexible but biased

A judge model can score open-ended work at scale, but may favor position, verbosity, style, or its own outputs. Explicit rubrics, pairwise comparisons, swapped order, calibration against humans, and multiple judges reduce these risks.

- Prefer checkable criteria over a vague quality score.
- Blind the judge to irrelevant identity information.
- Audit disagreements and drift.

### Tracing turns evaluation into engineering

A run trace is a tree of spans for model calls, tools, retrieval, and agents. Each span records inputs, outputs, timing, tokens, cost, errors, and relevant metadata. Offline eval protects releases; online eval monitors live behavior; CI gates block regressions.

- Build representative tasks with expected outcomes.
- Include hard, edge, adversarial, and safety cases.
- Run the same set on prompt, model, tool, or dependency changes.
- Alert on quality, latency, cost, and safety drift.

### A run manifest makes comparisons reviewable

Record the complete setup and every attempted run. A completed answer can be wrong, and an infrastructure failure is a different outcome. Fixed cases and explicit denominators make a comparison inspectable.

- Store model ID, prompt hash, and dependency versions.
- Record attempted and completed runs separately.
- Keep outcome scoring separate from resource use.

## Exam-ready summary

- Evaluation is continuous system steering, not a final phase.
- Measure both task success and the path taken.
- Treat benchmark scores as scaffold-dependent evidence.
- Trace every model, tool, retrieval, and agent step.

## Self-test

1. Why is agent evaluation harder than single-answer evaluation?
2. Give four outcome metrics and four trajectory metrics.
3. What makes execution-based evaluation strong?
4. How can benchmark contamination and weak tests mislead?
5. What biases affect LLM-as-judge?
6. How should an evaluation distinguish a wrong answer from an API failure?

## Assessed practice

Run the offline evaluation command, inspect its JSONL records, and test the failure path. For live inference, predeclare a model and budget before using the held-out split.

**Acceptance check:** A fresh rerun produces a manifest and one record per attempted case. Interrupted or failed requests do not disappear from the denominator.

**Lab:** labs/07_agents_sdk_evaluation.ipynb

## Reading and evidence

- **P3** [Would this change your answer?](https://arxiv.org/abs/2608.16747). Anthropic/Fellows preprint, arXiv v1, 2026-08-17. CHIVE tests counterfactual prompt changes. Generated explanations remain hypotheses. Official post: August 21.
- **R2** [How enabling two settings tripled our scores on the ARC-AGI-3 benchmark](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/). OpenAI research post, 2026-07-29. A specific harness experiment. Its result does not estimate the effect of context changes in Gemini.

## Source basis

The original structure follows `11-evaluation-observability.pdf`. The 2026-09-09 edition adds the readings above, protocol clarifications, and assessed practice. Research findings and classroom exercises have different scopes.
