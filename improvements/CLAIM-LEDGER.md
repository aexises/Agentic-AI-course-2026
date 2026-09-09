# Claim and verification ledger

Checked 9 September 2026. This ledger covers the substantive factual claims introduced in the research update, improvement plan, and notebook implementation notes. Teaching choices, rubrics, priorities, and estimated durations are proposals. It does not certify the entire pre-existing course or reproduce frontier-lab research.

Three passes mean identity/evidence, corroboration or implementation inspection, and scope/negative-case review. For a single-source research post, the second pass is a check of its methods and internal comparison, not an independent study.

## Research

| ID | Claim used | Pass 1: identity/date | Pass 2: support | Pass 3: scope check | Disposition |
|---|---|---|---|---|---|
| P1 | GPT-Red uses self-play with defenders and tests held-out transfer. | [Official release](https://openai.com/index/unlocking-self-improvement-gpt-red/) dated July 15, 2026; linked PDF title/affiliation checked. | [Paper](https://cdn.openai.com/pdf/gpt-red-automated-red-teaming-via-self-play-at-scale.pdf), abstract and sections 3–7. | Training and reported transfer do not establish universal robustness; no performance number transferred into course claims. | Include as technical paper; Lab 8 is an adaptation of testing discipline only. |
| P2 | Scientific-computing report studies eight projects and discusses verification/stewardship. | [Official release](https://openai.com/index/scientific-computing-agentic-ai/) dated July 28, 2026. | [Report](https://cdn.openai.com/pdf/scientific-computing-in-the-age-of-agentic-ai-an-exploratory-field-report.pdf), abstract, affiliations, case study G. | Exploratory cases; aggregate output agreement did not rule out implementation errors in the cited case. No causal productivity estimate inferred. | Include as OpenAI-affiliated collaborative field report. |
| P3 | CHIVE uses counterfactual prompt experiments and does not treat generated explanations as ground truth. | [arXiv](https://arxiv.org/abs/2608.16747) v1 August 17; [official post](https://alignment.anthropic.com/2026/chive/) August 21, 2026; authors checked. | [Paper](https://arxiv.org/html/2608.16747v1), sections 2 and 3. | Section 5 distinguishes the evaluation proxy from broader uses of interpretability. | Include; do not generalize its negative finding beyond the tested setup. |
| R1 | Multi-agent experiments expose coordination and information-sharing problems. | [Official post](https://www.anthropic.com/research/multiagent-systems), August 13, 2026. | Read coordination, epistemic-failure, and conflicting-goal experiments. | Search-scope/token differences prevent a simple unconditional “more agents is better” conclusion; production prevalence is not measured. | Include as research post. |
| R2 | Harness settings changed reported ARC-AGI-3 results. | [Official post](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/), July 29, 2026; checked against research index. | Read retained-reasoning/compaction comparison and public-set description. | Model, harness, and task-specific; no Gemini effect inferred. | Include as engineering/research post. |
| R3 | Internal research activity indicators need cautious interpretation. | [Official post](https://openai.com/index/research-acceleration-view-inside-openai/), September 6, 2026; checked against index. | Read opening findings and methods appendix. | Relationship between activity metrics and research progress is uncertain. | Include as observational post, not an independent causal study. |

## Software and protocol claims

| ID | Claim used | Documentation check | Implementation or second-source check | Boundary/negative check |
|---|---|---|---|---|
| S1 | Manual Gemini function calling returns tool results to the model; automatic execution can be disabled. | [Google function calling](https://ai.google.dev/gemini-api/docs/function-calling). | Installed `google-genai` types exercised; real client serialization tested through a mocked HTTP transport. | Fake client asserts second request includes result and call ID; budgets/empty responses/multiple calls tested. This does not verify a live model. |
| S2 | OpenAI Agents SDK can use Gemini through Chat Completions compatibility. | [SDK model guide](https://openai.github.io/openai-agents-python/models/). | [Google endpoint guide](https://ai.google.dev/gemini-api/docs/openai) matches explicit base URL; SDK client/model constructors checked. | Actual Runner tested with scripted Model and a mocked HTTP round-trip through the compatibility adapter. Provider feature parity and authenticated inference are not claimed. |
| S3 | LangGraph interrupts can resume with persisted checkpoints; the node restarts. | [Interrupt guide](https://docs.langchain.com/oss/python/langgraph/interrupts). | [Persistence guide](https://docs.langchain.com/oss/python/langgraph/persistence) and installed SQLite saver. | Notebook closes/reopens saver, recreates graph, resumes, and checks denied/replayed effects. Full crash consistency and remote exactly-once semantics are not claimed. |
| S4 | Schema validation and citation membership are insufficient for truth or authorization. | [Google structured output guide](https://ai.google.dev/gemini-api/docs/structured-output); runtime validation responsibility checked. | Pydantic schema tests and citation checker inspected. | Valid citation IDs can accompany unrelated prose; unauthorized proposals with valid field types are rejected. |
| S5 | Roots should not be treated as a sandbox. | [MCP roots, version 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/client/roots). | Security section assigns access control and path validation to implementations; protocol returns root metadata. | Inference: advertised scope alone does not enforce OS access. No claim made about the latest roots status; select an explicit version before updating the chapter. |
| S6 | A2A teaching should identify the binding/version. | [Official specification](https://a2a-protocol.org/latest/specification/), retrieved September 9. | The specification separates operations/data model from JSON-RPC, gRPC, and HTTP/REST bindings. | Current page is mutable; pin a release when implementing the course update. Existing chapter's stack is an incomplete general description, not proof of a broken implementation. |

## Course observations

| ID | Local evidence | Second check | Third check / scope |
|---|---|---|---|
| C1 | README and source map describe 13 chapters and generator-based rebuild. | Enumerated chapter files and inspected `presentations/src/course-data.mjs`. | Original PDF sequence not in checkout; output studybook PDF is present. Review claims refer to available Markdown and reference notebooks. |
| C2 | Chapters 7, 11, 12, 13 already discuss memory, evaluation, safety, and production. | Read objectives, notes, and self-tests. | Plan identifies an implementation/assessment gap, not absence of the concepts. |
| C3 | Lab 3 tool registry bug. | Isolated function run with two different registries. | Returned global result instead of supplied result; no live tool executed. |
| C4 | Lab 3 manual native loop stops after dispatch. | AST finds one `generate_content` call. | Source inspection finds printed outputs but no model continuation. |
| C5 | Lab 4 search constructor and response handling defects. | Fake Tavily response with `raw_content` yields empty list. | Fake typo-field response reaches string `.append` failure. No network request used. |
| C6 | Lab 3 described stop sequence is not passed by `run`. | AST inspects `llm(messages)` invocation. | Does not claim every provider supports that stop sequence; structured calls are the new lab's path. |
| C7 | Lab 3 arithmetic has no explicit expression/magnitude/exponent cap. | Inspected operator map and function body. | No resource-intensive input evaluated; new lab's bounded operations tested on huge numbers and nonfinite values. |
| C8 | New student copies contain TODOs; instructor copies contain solutions. | Notebook structure and mode flags checked. | Fresh-kernel execution distinguishes worked examples from enabled solution checks; see validation record. |

Reference-cell observations are reproduced by `scripts/audit-reference-labs.py`, with evidence in [reference-audit.json](validation/reference-audit.json). The script reads the AAI[sum26] snapshot at its local project path and does not modify it.

## Claims intentionally excluded

No claim that every original source-PDF statement has been recertified, that offline fixtures measure Gemini quality, that API use is free, that a named model is available in every account, that counterfactual edits expose internal reasoning, or that these small labs reproduce the cited experiments. No blanket “SOTA” ranking is offered: performance requires a specified task, system, budget, and evaluation.
