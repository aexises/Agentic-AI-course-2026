# Your first course run

Start here. This route assumes you are comfortable with Python/ML, want more backend and deployment guidance, and have **6–8 hours per week**. You are the first learner in this revision: the schedule is a planning estimate, not a measured completion promise. Extend a week when a prerequisite or environment issue needs attention.

## Weekly rhythm

Reserve 90 minutes for textbook reading and recall, 3–4 hours for implementation, 60–90 minutes for tests and debugging, and 30–60 minutes for a learning log. Keep the final hour flexible. Close the book and explain one design decision before consulting selected answers.

Use a personal copy or branch for solutions. Start with student notebooks, not instructor copies. Try a TODO for 20–30 focused minutes, write the exact failing case, then use a hint or official documentation. If you inspect a reference solution, record that assistance, close it, and reimplement the idea the next day on a changed example. Do not count copied execution as independent mastery.

## Suggested 18-week route

| Week | Reading and practice | Evidence to keep |
|---|---|---|
| 1 | Chapters 1–3; Lab 3 | Bounded tool loop, protocol failure tests |
| 2 | Chapters 4–6; Lab 4 | Retrieval repair, invalid citation rejection |
| 3 | Chapter 5 review; Lab 5 | Native tool round-trip and budgets |
| 4 | Chapters 6–7; Lab 6 | Graph state and abstention |
| 5 | Chapters 8–11; Lab 7 | Baseline comparison and failure accounting |
| 6 | Chapter 12; Lab 8 | Approval, restart, replay evidence |
| 7 | Lab 9; revisit chapter 8 | Parallel state updates and bounded work |
| 8 | Labs 10–11; compare framework choices | Two implementations and tradeoffs |
| 9 | Backend primer; Lab 12 | Ingestion and source lineage |
| 10 | Lab 13; SQL/index review | Actual pgvector queries and query plans |
| 11 | Lab 14 | Hybrid retrieval/reranking evaluation |
| 12 | Labs 15–16; chapter 13 | FastAPI routes, service tests, retrieval experiment |
| 13 | Lab 18 | Real MCP transport, approval and transaction tests |
| 14 | Lab 19 | Local images, migration, rollback |
| 15 | Lab 20 | Logs, raw HTTP measurements, honest comparison |
| 16 | Capstone design and offline integration | Frozen contracts, data and baseline |
| 17 | Capstone failure/recovery assessment | All attempts and reproducible evidence |
| 18 | Report and demonstration; optional live extension | Offline completion or advanced live assessment |

Reading-heavy weeks and paired-lab weeks may need splitting. Optional Lab 17 (fine-tuning) is outside this schedule. The [lab index](../labs/README.md) selects the right environment; do not combine all dependencies in one environment.

## Backend checkpoints

Before Lab 12, explain a primary key, a parameterized query, a transaction, and the difference between a table and an index. Before Lab 15, send a JSON request and explain 2xx, 4xx, 5xx and a timeout. Before Lab 19, distinguish an image, container, service, port and volume. Use the [backend primer](../labs/engineering/BACKEND-PRIMER.md) for small rehearsals.

## Completion and self-assessment

For each lab, enable exercise checks, restart the kernel, run all, add the requested failure cases, and complete the [submission template](SUBMISSION-TEMPLATE.md). A clean default run with exercises disabled is only a setup check.

The [capstone](CAPSTONE.md) defines two separate outcomes. Offline completion needs no paid model inference, but does require real local technologies, including pgvector and Docker. Initial package, image and model downloads require network access. Advanced assessment additionally requires your own live model evidence. Neither outcome guarantees hiring readiness or job offers.

Keep a weekly log: date, notebook hash, reading time, setup time, implementation time, checks passed/failed, first blocker, help consulted, one explanation from memory, and next action. No classroom pilot results exist yet; your observations will inform a later course revision.
