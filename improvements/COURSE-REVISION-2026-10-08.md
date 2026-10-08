# Course revision — 8 October 2026

## Delivered scope

Labs 3–5 now require implementation rather than providing their assessed solutions. Longer functions have small guided TODOs; reference answers are in instructor notebooks. Lab 4 additionally rejects invalid structured answers and unsupported citation IDs, invalid grader types and conflicting evidence identities. Citation membership still does not prove entailment.

Labs 18–20 add actual MCP/HTTP tools, transactional replay protection, local Docker Compose, migrations, release decisions, rollback, safe request logs and measurement exercises. Lab 17 is an optional fine-tuning brief, not a validated training notebook. The capstone defines offline completion and advanced live assessment separately.

The self-study route assumes Python/ML familiarity and 6–8 hours weekly, with extra SQL, HTTP and Docker support. An 18-week schedule is a flexible teaching estimate, not a measured guarantee. Current READMEs, teaching guides and textbook preface now link to the complete course path. Historical reports retain their original evidence scope.

## Verification

- Core regression suite: **101 passed, 18 subtests passed**.
- Engineering reference suite: **10 passed**, including actual local HTTP and MCP subprocess execution.
- Fresh-kernel notebook execution: **12 core notebooks** (six student setup runs, six instructor exercise runs) and **six engineering notebooks** (three of each).
- Textbook source build and consistency check passed: 13 chapters, 65 exercises, 35 references. Markdown, generated LaTeX and its source archive were rebuilt; no PDF was compiled.
- Engineering dependency compatibility check passed; exact resolved versions are saved in the track.
- Docker build, readiness, approval/replay, migration, replacement, rollback and actual JSON request logging passed. See the [precise scope](../labs/engineering/VALIDATION.md).

Default student execution is setup evidence, not completion. The current pass counts concern the reference implementations and regression tests, not a solved student submission. No new live provider, GPU, cloud, hosted-CI or student-pilot evidence was produced. Existing framework and RAG runtime reports describe earlier validation; those entire tracks were not re-executed for these documentation changes.

## Source and presentation checks

Changed interfaces were checked against official Gemini function-calling, Tavily Python, MCP Python SDK, SQLite transaction/ALTER TABLE, Docker Compose and HTTPX documentation. Package behavior was also exercised locally where reported above. These checks cover the changed material; this revision does not claim to revalidate every historical research statement in the textbook.

Notebook schema, Python syntax, executed outputs, exercise separation and local navigation were inspected. Full notebook-editor visual layout remains unreviewed. The textbook's final typesetting remains for the user to compile and inspect, as requested.
