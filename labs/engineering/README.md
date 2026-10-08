# Labs 18–20: enterprise tools and local operation

These are **assignments to solve** with guided TODOs in [submission.py](submission.py), notebook instructions, visible tests, and [staged hints](HINTS.md). Read the [backend primer](BACKEND-PRIMER.md) before starting. All data and keys are synthetic local examples.

| Lab | Practical work | Prerequisites |
|---|---|---|
| [18: enterprise tools and MCP](18_enterprise_tools_mcp.ipynb) | FastAPI approval boundary, SQLite atomic replay, actual MCP stdio tools | Labs 5, 8, 15–16 |
| [19: local delivery and migrations](19_local_delivery_and_migrations.ipynb) | Docker Compose image, release gate, additive migration, rollback | Completed 18 |
| [20: observability and performance](20_observability_performance_cost.ipynb) | Structured request logs, HTTP load measurements, cost/failure aggregation, cache scope | Completed 18–19 |

Allow 3–4 hours per lab plus prerequisite reading; these estimates have not been student-piloted. Required deployment is local Docker Compose. Cloud and hosted CI are optional. The ledger uses SQLite; retrieval remains in the pgvector service from Labs 12–16. Flask is not an additional requirement.

## Setup

Use Python 3.12 and a separate environment, from this directory:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python -m ipykernel install --user --name course-engineering --display-name 'Course engineering'
```

Choose that kernel in your notebook editor. Keep this entire directory together. The MCP exercises target the pinned MCP 2.3.0 API: `MCPServer` and `Client`. Older FastMCP/ClientSession examples use different interfaces; do not mix versions. See [validation](VALIDATION.md) for actual tested scope. requirements-lock.txt is the resolved host snapshot; the smaller requirements-service.txt supplies the container dependencies.

## Work sequence

1. Open the student notebook and run setup with exercises disabled.
2. Edit numbered TODOs in submission.py, reload the module, enable RUN_EXERCISES and run all.
3. Run the relevant visible tests: `python -m pytest tests -q`. An unfinished submission is expected to fail. Some tests depend on later labs; use the notebook's subset or pytest `-k` while progressing.
4. Add your own cases and retain evidence. Lab 19 requires an actual Docker demonstration; Lab 20 requires actual request logs and measurements.

The supplied service, transport launcher, fixtures and timing harness are scaffolding. Authorization, transaction behavior, MCP tool functions, migration, release decisions, metrics and trace records are your work. Instructor copies and instructor/reference.py are for separate checking, not student starter code.

## Run locally

After completing Lab 18, from this directory:

```bash
python -m uvicorn engineeringlab.support:create_app --factory --port 58018
```

The service stores local state in student-results/tickets.sqlite. GET /health checks database access. POST /approvals uses a reviewer key; POST /tickets uses an agent key. See the primer for requests. These public keys demonstrate separated roles, not secure production identity. MCP starts through the notebook harness with an agent key only.

For Lab 20 after implementing trace_event, set COURSE_TRACE=1 when starting the process or Compose stack. JSON events appear in Uvicorn's log and response headers carry X-Request-ID. Logs are local request observations, not distributed traces.

## Rebuild and verify as an instructor

From the course root using this environment:

```bash
python scripts/build-engineering-labs.py
COURSE_SUBMISSION=instructor.reference python -m pytest labs/engineering/tests -q
python scripts/validate-engineering-labs.py
```

No paid model calls happen in these checks. Live capstone inference requires an explicit account/model configuration and a student-defined budget. Never submit keys or .env files. Use the [course self-study guide](../../teaching/SELF-STUDY-GUIDE.md) and [capstone](../../teaching/CAPSTONE.md) for the complete route.
