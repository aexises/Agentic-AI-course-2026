# Research additions for the course

Research checked on **9 September 2026**. Prioritize the following three papers/reports and three research posts. These were selected for teaching relevance from recent OpenAI and Anthropic material; this is not an exhaustive literature review or a claim that every newest publication was found. Publication type matters: none is described here as peer reviewed without a verified venue.

The course's existing emphasis on bounded autonomy, runtime policy, evidence, and evaluation should remain. The proposed change is to make students test these ideas. Recommendations below are curriculum judgments, not claims that a paper measured learning outcomes.

## Papers and reports

### P1 · GPT-Red: Automated Red Teaming via Self-Play at Scale

**OpenAI; release page dated 15 July 2026. Technical paper.**

The paper trains an attacker against a population of defenders using self-play and evaluates transfer to held-out settings. The useful teaching point is the difference between passing a fixed attack list and resisting an adaptive attacker. **Proposal:** add a threat model, separate development and held-out attack cases, and report authorized-task completion alongside attack outcomes. Use in chapters 11–12 and Lab 8. The lab is a small runtime-policy exercise; it does not reproduce the training procedure or establish model robustness. Avoid importing the paper's attack-success rates into classroom claims.

[Paper, abstract and sections 3–7](https://cdn.openai.com/pdf/gpt-red-automated-red-teaming-via-self-play-at-scale.pdf) · [Official release and date](https://openai.com/index/unlocking-self-improvement-gpt-red/).

### P2 · Scientific computing in the age of agentic AI: an exploratory field report

**OpenAI-affiliated collaboration; release page dated 28 July 2026. Exploratory field report.**

The report examines eight scientific-computing projects and emphasizes verification and stewardship. A case study describes implementation defects despite strong aggregate agreement with reference outputs. **Proposal:** require edge-case tests, reference comparisons, and named maintenance ownership in the capstone. Use in chapters 11 and 13. This is a collection of case studies, not a randomized estimate of agent productivity; do not generalize its speedups to students or other projects.

[Report, abstract and case study G](https://cdn.openai.com/pdf/scientific-computing-in-the-age-of-agentic-ai-an-exploratory-field-report.pdf) · [Official release and date](https://openai.com/index/scientific-computing-agentic-ai/).

### P3 · Would this change your answer? Evaluating Explanations of LLM Behavior In The Wild with Counterfactual Experiments

**Adam Karvonen, Euan Ong, Subhash Kantamneni, Samuel Marks; Anthropic Fellows Program/Anthropic. arXiv v1 dated 17 August 2026; official post dated 21 August 2026. Preprint.**

CHIVE investigates behavior through prompt edits and measured response changes. It separates generated explanations from experimental labels. **Proposal:** students predict the effect of one prompt edit, run paired conditions, and distinguish observed changes from causal explanations. Use in chapters 2, 10–11 and Lab 7. Its negative result for the tested activation-reading tools is specific to the evaluation; it does not prove interpretability is useless. The lab uses the counterfactual method only, without activation access or training.

[Preprint](https://arxiv.org/abs/2608.16747) · [Methods and limitations](https://arxiv.org/html/2608.16747v1) · [Official post](https://alignment.anthropic.com/2026/chive/).

## Recent research posts, separately labeled

### R1 · Patterns and problems in emerging multiagent systems

**Anthropic, 13 August 2026. Research post.**

The reported experiments include coordination, shared-resource conflicts, and information aggregation. In the vulnerability experiment, the coordinating and independent conditions differ in search scope and token use; restricting comparison to core directories changes the interpretation. **Proposal:** students compare single-agent and reviewer designs on the same tasks and budgets, and inspect conflicting evidence instead of equating consensus with truth. Use in chapters 8–9 and Lab 7. These controlled studies do not establish how frequently the behaviors occur in production.

[Official study, “Measuring coordination,” “Epistemic failures,” and “Incompatible goals”](https://www.anthropic.com/research/multiagent-systems).

### R2 · How enabling two settings tripled our scores on the ARC-AGI-3 benchmark

**OpenAI, 29 July 2026. Research/engineering post.**

The reported experiment changes retained reasoning and compaction in the evaluation harness. **Proposal:** add a harness manifest and controlled context-policy comparison to chapters 7 and 11. Lab 6 provides a small setting for comparing retrieval policies. The result concerns the named OpenAI model, public tasks, and harness; it is not a Gemini improvement estimate or a guarantee that summarization helps. The Gemini compatibility path in these labs does not implement OpenAI Responses compaction.

[Official experiment and comparison conditions](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/).

### R3 · Research acceleration: The view inside OpenAI

**OpenAI, 6 September 2026. Internal observational research post.**

The post examines agent use and research-work indicators inside OpenAI. Its methods section notes uncertainty in interpreting code-generation metrics as research progress. **Proposal:** use it as a chapter 13 evidence-critique exercise: separate activity, task success, and validated scientific progress. Do not teach activity growth as a causal estimate of productivity or a forecast for students.
 
[Official post and methods appendix](https://openai.com/index/research-acceleration-view-inside-openai/).

## Reading sequence

Assign P3 with evaluation, P1 with security, R1 with multi-agent systems, and P2 with the capstone. R2 and R3 are short discussion readings. Suggested response format: question studied, method, evidence, limitations, and one testable change to the student's agent. Students should not memorize model rankings or transcribe headline percentages.

## Verification protocol

Each included item received three different checks:

1. **Identity and date:** open the primary publication or official release; distinguish manuscript dates from post dates.
2. **Claim support:** inspect the paper's relevant section, or the research post's experiment/methods text; do not rely on search snippets.
3. **Scope and counterclaim:** examine comparison conditions and limitations; separate reported findings from proposed teaching applications.

The detailed [claim ledger](CLAIM-LEDGER.md) records these checks. Re-reading one vendor's work does not create three independent replications. “Triple checked” here means three verification passes, not a guarantee of truth or independent reproduction of the research. No headline benchmark percentages or current model-price claims are needed for this proposal.
