# Instructor preparation and grading

For the current full course, use the [self-study route](../../teaching/SELF-STUDY-GUIDE.md) and [two-outcome capstone](../../teaching/CAPSTONE.md). Labs 18–20 follow this track. Allocate extra HTTP, SQL and Docker practice using the [backend primer](../engineering/BACKEND-PRIMER.md).

Complete the full preflight before class. In particular, start the real database, download models, warm the splitter/tokenizer and models by seeding, and execute the integration suite. Check available disk space and ports 55432/58000. Distribute the whole track except `instructor/`, validation answer outputs if they expose solutions, and model caches; supply the model manifest separately if sharing cached weights under their licenses.

## Observable practice requirements

| Lab | Ask the student to demonstrate | A weak submission looks like |
|---|---|---|
| 12 | Change chunk boundaries, inspect provenance, replay ingestion without duplicate rows, update a version, remove a document and its chunks | Calling seed once without inspecting data |
| 13 | Execute their SQL, inspect EXPLAIN, build each index separately, measure exact-versus-ANN neighbors with and without filters | Claiming an index was used because CREATE INDEX succeeded |
| 14 | Show candidate IDs at each stage and a query where ranking changes or stays unchanged; explain the metric denominator | Reporting fluent generated text as retrieval evaluation |
| 15 | Start their own app, use its HTTP docs/client, exercise 401/422/503 behavior, show tenant selection in a dependency and SQL | Running only the shipped reference endpoint |
| 16 | Update evidence through ingestion, observe the change over HTTP, retain a reproducibility manifest, diagnose a failure | A screenshot of one successful query |

Keep the public fixtures for teaching. For assessment, introduce a new tenant, a novel document, a restrictive filter, a query with an exact identifier, and a schema-valid but unauthorized request. Do not grade a student's retrieval method as incorrect merely because it fails to beat another method on this tiny corpus; grade experimental validity and their diagnosis.

## Practical failure drills

Use only the isolated course project. A simulated `OperationalError` test checks response policy; a stopped database checks a different system path. Have students label which they executed. Restart the database after a deliberate outage. For document transactions, inject a duplicate chunk key and confirm the preceding document version remains readable. A failed transaction should not leave the document without chunks.

For index experiments, retain the plan and actual returned row count. A small table may choose a sequential scan; forced planner settings are diagnostic only. Filtering can change both returned counts and approximate-neighbor recall. Do not infer production latency from the generated-vector notebook.

The starter applies tenant filters in the application; it does not implement RLS. An advanced exercise may add a least-privilege database role and an RLS policy, but students must test those with the actual service role rather than a database owner.

## Scope and progression

The four first labs are planned for 120 minutes each after setup. The integrated capstone gets two 90-minute sessions or take-home time. If the course schedule is fixed, prioritize Labs 12–15 and make Lab 16 the final project. Retain the optional Milvus/Pinecone adapter as enrichment, not a replacement for pgvector practice.

Use the per-notebook rubric. Require implementation plus tests plus interpretation. Instructor reference solutions cover the specified TODO contracts; deployment hardening and student-authored failure cases remain assessed extension work.
