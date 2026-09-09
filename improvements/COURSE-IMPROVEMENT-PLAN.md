# Course improvement plan

**Recommendation:** keep the 13-chapter structure, correct overbroad statements, and add an assessed engineering sequence. The course already teaches evaluation, safety, memory, and multi-agent tradeoffs. Its main weakness is the gap between those principles and observable student work.

Reviewed: the 13 Markdown chapters, README, source map, exam guide, the relevant generator text, and the two notebooks in AAI[sum26]. This review does not certify every sentence in the original PDFs, generated decks, or studybook. The original source PDFs were not present in this course checkout. The implementation status below now reflects the integrated course update. Original findings are retained as audit history.

## Prioritized findings

| Priority | Evidence in existing material | Why it matters | Proposed correction and acceptance check |
|---|---|---|---|
| P0 | Reference Lab 3 `run_tool`, cell 10, checks the supplied registry but dispatches through global `TOOLS`. | Injected tool registries are not respected; isolated tests can execute the wrong function. | Dispatch only through the supplied registry. A replacement tool must return its replacement result. Covered by new Lab 5. |
| P0 | Reference Lab 3 `run_native_manual`, cell 14, prints dispatched outputs and ends. | Students do not observe a completed native model→tool→model cycle. | Preserve complete model content, match call IDs, return tool results, and continue under separate round/call caps. Lab 5 fake client verifies the second request. |
| P0 | Reference Lab 4 `search_and_scrape`, cell 8, passes the key as `api_base_url`, reads `raw_context`, and overwrites a list with a string before `.append`. | The search stage cannot implement the stated behavior as written. | Use the documented constructor and response fields; preserve source metadata; test empty and malformed responses before live search. New Lab 6 uses controlled records rather than depending on that broken path. |
| P0 | Reference Lab 3 calculator allows exponentiation with no explicit input-size or magnitude bounds. | AST whitelisting alone does not bound resource consumption. | Teach bounded numeric operations and runtime constraints. New Lab 5 rejects huge/nonfinite operands and nonfinite results. No expensive expression was executed during this audit. |
| P1 | Chapter 11 describes repeated runs, traces, and CI; the reviewed reference labs do not provide a comparable evaluation harness. | Students can report an anecdotal answer without demonstrating repeatability or accounting for failed attempts. | Require task IDs, expected results, model/prompt/package versions, request counts, and failure classification. Lab 7 supplies a starting harness. |
| P1 | Chapter 7 discusses state; chapter 13 names retries and idempotency. | There is no checkpoint/replay exercise in the two reference notebooks. | Reopen a checkpoint before resume; deny malformed actions; prove a replay does not duplicate the local effect. Lab 8 implements these checks. |
| P1 | Reference Lab 4 returns strings from retrieval and teaches an iterative correction path without source-ID checks. | The evidence lineage is lost before answer verification. | Carry ID, text, and source through retrieval; distinguish provenance membership from entailment; require abstention. Lab 6. |
| P1 | Chapter 2 says native calling produces “provider-enforced structured calls”; chapter 3 recommends text stop sequences. | Readers may infer uniform provider support or confuse format control with execution control. | Qualify by provider/model/schema support and keep local validation. Reference Lab 3 does not pass its described stop sequence in `run`; either pass it where supported or remove that claim. Lab 5 teaches the structured path. |
| P1 | Chapter 10 describes sampled chains as independent and implies wrong answers are less likely to coincide. | Sampling does not establish independent errors or make voting a verifier. | Phrase this as a hypothesis to test; add shared-error and misleading-cue cases. Lab 7 and Anthropic multi-agent reading. |
| P1 | Chapter 5 describes roots as permitted filesystem scopes; chapter 9 presents a specific A2A transport stack without a version. | Protocol description can be confused with enforced authorization, and mutable specifications become undated facts. | State the exact protocol version and implementation. Treat roots as contextual information, not sandbox enforcement. Use a versioned A2A source and identify the binding actually taught. See the claim ledger. |
| P2 | Chapters have conceptual self-tests but no coding rubric in this checkout. | Assessment emphasizes explanation without an executable acceptance condition. | Attach implementation, failure-case, experiment, and limitation marks. Each new notebook includes a rubric totaling 100 points. |
| P2 | `SOURCE-MAP.md` and chapter source-basis notes describe a source-PDF-only rebuild. | Adding research directly could make the provenance notes inaccurate. | Keep a dated research supplement and amend provenance before regenerating content. Update `presentations/src/course-data.mjs`, not only generated Markdown. |

The reference defects are documented in [reference-audit.json](validation/reference-audit.json); cell numbers are zero-based. They are observations about the supplied snapshots, not about all editions of the reference course.

## Chapter-by-chapter changes

| Chapter | Proposed change | Evidence or student artifact |
|---|---|---|
| 1 · Introduction | Keep minimum sufficient autonomy; add a measurable “when a workflow is enough” decision. | Student chooses a baseline and acceptance criteria before adding an agent. |
| 2 · Reasoning engine | Separate output format, semantic correctness, and faithful explanation. Qualify default prompting advice by task/model. | CHIVE reading response and one controlled prompt edit. |
| 3 · ReAct | Contrast the historical text loop with a complete structured tool protocol. | Lab 5 call IDs, observed tool results, and stop reasons. |
| 4 · Patterns | Require a baseline before adding routing, review, or workers. | Same-task comparison with all extra calls included. |
| 5 · Tools/MCP | Add typed dispatch, argument limits, provider compatibility, and versioned protocol notes. | Lab 5; version and enforcement distinction in a short quiz. |
| 6 · RAG | Add source lineage, conflicting evidence, abstention, and a static baseline. | Lab 6 separates retrieval hits from answer support. |
| 7 · Memory | Distinguish model-visible context from stored execution state; add checkpoint replay. | Lab 8 checkpoint test; optional context-policy ablation motivated by R2. |
| 8 · Multi-agent | Add shared mistakes, contradictory goals, and controlled reviewer comparisons. | R1 reading; Lab 7 single-agent/objective-review/model-review comparison. |
| 9 · Interoperability | Version the protocol and add trust-boundary reasoning rather than API-name memorization. | Student identifies who authenticates, authorizes, and owns a delegated effect. |
| 10 · Planning | Replace unqualified benefits with a testable choice among baseline, sampling, review, and search. | Counterfactual experiment; no claims based only on a verbal explanation. |
| 11 · Evaluation | Move a small evaluation exercise earlier; retain this chapter for experimental rigor and release gates. | Lab 7 manifest, attempted/completed denominators, held-out cases. |
| 12 · Security | Distinguish malicious model proposals from successful unauthorized effects. | P1 reading; Lab 8 benign/malicious cases and false rejection discussion. |
| 13 · Production | Add replay semantics, maintenance ownership, and evidence-quality critique. | P2/R3 reading; capstone runbook and reproducibility bundle. |

## Implementation sequence

Effort estimates below are planning estimates for an instructor/course maintainer, not measured promises. Dependencies matter more than calendar dates.

| Stage | Owner | Estimated effort | Deliverable | Completion gate |
|---|---|---:|---|---|
| 1. Repair teaching baseline | Course maintainer | 1–2 days | Apply reference-lab fixes if those originals will still be distributed; add setup and version notes. | Offline regression cases pass; no key required to inspect examples. |
| 2. Integrate research | Lecturer | 1 day | Add P1–P3/R1–R3 readings and chapter-specific discussion prompts. | Each external factual assertion has a source, date/type, and scope note. |
| 3. Pilot four labs | Lecturer + teaching assistant | Four class sessions plus 1 day review | Run the supplied labs with a small student group. | Record actual time, misunderstandings, failed setups, and rubric results; revise estimates. |
| 4. Add empirical evaluation | Teaching assistant | 1–2 days plus API access | Run selected Gemini model on held-out tasks; retain failures and usage. | Exact model ID and package snapshot recorded; live results clearly separated from fixtures. |
| 5. Rebuild course outputs | Course maintainer | 1 day | Edit generator data, update source map, regenerate Markdown/decks/studybook. | Citation and wording checks plus visual review of rebuilt artifacts. |
| 6. Capstone gate | Lecturer | One assessment cycle | Student submits a bounded agent with evaluation and operating notes. | Fresh-environment rerun; negative tests; reviewer can trace each conclusion to evidence. |

## Assessment proposal

Use the per-lab rubrics supplied in the notebooks. For a final capstone, propose: 30% functional correctness; 25% negative-case and recovery tests; 25% controlled evaluation and evidence; 20% reproducibility and explanation of limitations. These weights are suggested teaching choices.

Require a no-agent or simpler-workflow baseline, held-out tasks, explicit stopping conditions, and an explanation of the chosen framework. Award credit for a well-supported finding that an additional agent or query-repair step did not help. Do not grade students on obtaining a particular model's answer or reproducing a vendor's benchmark score.

## Implementation status

The local course update is implemented: repaired foundation copies, research integration, regenerated chapters/decks/studybook, a bounded evaluation runner, and pilot/capstone teaching materials. See [IMPLEMENTATION-STATUS.md](IMPLEMENTATION-STATUS.md) for completion evidence and the stages requiring an actual class or configured live API. The original AAI[sum26] project was retained as an audit reference; use the repaired course-local copies for distribution.
