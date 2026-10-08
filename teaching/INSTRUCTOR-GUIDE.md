# Teaching and self-assessment guide

The current route is Labs 3–16, then 18–20, followed by the capstone; Lab 17 is optional. Numbering preserves the supplied AAI[sum26] reference. The original reference project remains unchanged. Use the [lab index](../labs/README.md), [self-study route](SELF-STUDY-GUIDE.md), and [pilot log guidance](PILOT-GUIDE.md).

Labs 3–5 now require student implementations. Lab 3 assesses protocol parsing, injected dispatch and bounded execution. Lab 4 assesses retrieval and corrective control flow, including evidence identity and invalid-answer rejection. Lab 5 assesses dispatch and the native model/tool/model exchange. Instructor solutions are separate. Distribute student notebooks and required support, excluding instructor folders, reference_support.py, build scripts and executed instructor notebooks.

Use each notebook's rubric. Default execution with TODO checks disabled establishes setup only. Assessment requires enabled checks, fresh-kernel execution, added failure cases and an explanation. Visible checks are not an exhaustive grader; design an unseen case or, for self-study, freeze a small new set before implementing the final solution. Record solution consultation as assistance, not independent mastery.

Keep four environments separate: Labs 3–8, frameworks 9–11, RAG 12–16, engineering 18–20. The [framework guide](../labs/frameworks/README.md), [RAG instructor guide](../labs/rag/INSTRUCTOR-GUIDE.md) and [engineering guide](../labs/engineering/README.md) specify setup. Practice real pgvector SQL, LlamaIndex ingestion, neural reranking, FastAPI requests, MCP transport, Docker images and migrations; helper imports alone are insufficient student evidence.

The first learner has Python/ML experience and needs extra backend support. Assign the engineering backend primer before the service labs and use 6–8 hours weekly as a flexible planning assumption. Durations are unpiloted estimates.

The capstone has two outcomes: model-offline course completion and advanced live assessment. Students provide their own accounts/hardware; no free API or GPU access is assumed. Offline completion still includes real local services. GPU fine-tuning, cloud deployment and hosted CI are optional. Do not award advanced live completion for fixture traces.

Use the [evaluation runner](../evaluation/README.md) for manifest and failure-accounting practice. Its published holdout examples are not secret assessment data. Discuss a simpler baseline and require all attempted runs, including errors. Citation membership does not establish entailment; deterministic fixtures do not establish model quality. Separate papers, engineering reports, interface documentation and course-design choices when explaining evidence.

Textbook Markdown and LaTeX derive from the same sources; the earlier Word/PDF conspect and slide decks are companion material, not the current assignment authority. Follow [textbook instructions](../textbook/README.md). The current validation report records software checks, not classroom effectiveness or employment outcomes.
