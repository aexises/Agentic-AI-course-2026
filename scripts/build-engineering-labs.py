"""Build unsolved engineering assignments and separate instructor execution copies."""
from pathlib import Path
import nbformat as nb
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'labs/engineering'
md=nb.v4.new_markdown_cell;code=nb.v4.new_code_cell
setup='''from pathlib import Path
import sys, importlib, json
HERE = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p / "engineeringlab").is_dir() or (p / "labs/engineering/engineeringlab").is_dir())
TRACK = HERE if (HERE / "engineeringlab").is_dir() else HERE / "labs/engineering"
if str(TRACK) not in sys.path: sys.path.insert(0, str(TRACK))
RUN_EXERCISES = False
MODULE = "submission"
impl = importlib.import_module(MODULE)
from engineeringlab import checks
print("Implement submission.py, reload it, then enable exercise checks. Default execution is not a pass.")'''
common='''## Setup
Use the separate engineering environment in README.md. Read the backend primer first. These assignments use local services and your own files; no model/API calls are made by default. All records and keys are invented teaching examples. Keep the whole track folder. Edit the numbered TODOs in `submission.py`, then run `importlib.reload(impl)` before rerunning tests. Instructor implementations are not included in the student handout.

Use a two-pass workflow: attempt each small TODO using the contract, then consult the staged hints in HINTS.md if needed. Record how much help you used in your learning log. Keep your solution in your own Git branch or copy. Never replace it with the instructor implementation before attempting the exercise.'''

def save(name,cells):
 for solved in (False,True):
  n=nb.v4.new_notebook(cells=[md('# '+name[3:].replace('_',' ').title()),md(common),code(setup.replace('RUN_EXERCISES = False','RUN_EXERCISES = '+str(solved)).replace('MODULE = "submission"','MODULE = "instructor.reference"' if solved else 'MODULE = "submission"'))]+cells,
    metadata={'kernelspec':{'name':'python3','display_name':'Course engineering','language':'python'}})
  for i,c in enumerate(n.cells):c.id=f'{name[:2]}-{i:03}'
  nb.validate(n);nb.write(n,OUT/('instructor' if solved else '')/(name+'.ipynb'))

save('18_enterprise_tools_mcp',[
md('''## Goal
Implement three small boundaries: authorization, atomic ticket creation with replay protection, and MCP tools forwarding to an HTTP service. Prerequisites: Labs 5, 8, 15–16; SQL transactions and HTTP basics from the primer. Plan two study sessions (about 3–4 hours total, an unpiloted estimate).

The system has three identities: the API caller, the tenant selected by its key, and a separate reviewer. A model can propose an operation; only the reviewer endpoint can create its approval receipt. The receipt is bound to tenant, operation ID, resource, and summary. Reusing the ID with changed content is a conflict. The local keys demonstrate identity separation; they are public and do not make this a production authentication system.

The action ledger uses SQLite to make this exercise portable. Your RAG corpus remains in pgvector from Labs 12–16; the capstone combines the services.'''),
md('''## Steps
### 1. Trace the provided transport before editing it
Read `engineeringlab/support.py`. Draw the path from X-API-Key to tenant, allowed resources, approval lookup, authorization, and transaction. Find where a caller-supplied tenant or approval field is rejected by the request schema. Explain why the MCP server must never receive the reviewer key.

A transaction groups database changes. The idempotency key identifies one intended business operation. Here the composite key is `(tenant, operation_id)` so another tenant's operation cannot be treated as a replay. The stored payload lets the service distinguish a genuine retry from a changed request.'''),
md('''### 2. TODO 18.1 — authorize
Edit `authorize`: accept only an actual boolean True and a resource in the trusted resource set. Reject strings such as "yes" and integer 1. The approved value comes from a server-side receipt lookup, not from model arguments.'''),
code('''if RUN_EXERCISES:
    importlib.reload(impl)
    checks.authorization(impl)
    print("Authorization contract passed")'''),
md('''### 3. TODO 18.2 — commit or replay one ticket
Implement the transaction in `commit_ticket`. Start with BEGIN IMMEDIATE, select by both identity columns, and compare the canonical payload. On an identical retry return the old ID. On changed content raise Conflict. For a new operation insert one row and commit. Roll back on every exception. Use explicit INSERT column names so an additive migration can remain compatible.

Return `{ticket_id: str, replayed: bool}`. Add your own concurrent duplicate-request test. A generated UUID alone is not replay protection. A lost HTTP response also does not imply that the database write failed.'''),
code('''if RUN_EXERCISES:
    importlib.reload(impl)
    checks.transactions(impl)
    print("Replay, conflict, tenant separation, and reopened-connection checks passed")'''),
md('''### 4. TODO 18.3 — expose an actual MCP server
Implement `register_tools` using the installed MCP SDK's `server.tool()` decorator. Expose create_ticket(operation_id, resource, summary) and ticket_status(operation_id). Use only the supplied HTTP client; it holds the caller key and timeout. Forward errors with raise_for_status. No tool accepts a tenant, API key, or approval flag.

The next check launches a real Uvicorn service and an MCP subprocess over stdio, creates approval through a separate reviewer request, and invokes your tool through an MCP client. It also checks that an unapproved call creates no ticket. The subprocess stdout is the protocol channel; write diagnostics to stderr. This local stdio exercise does not implement remote MCP OAuth.'''),
code('''if RUN_EXERCISES:
    importlib.reload(impl)
    result = await checks.mcp_roundtrip(MODULE)
    print(result)'''),
md('''## Checks and submission
Run `python -m pytest tests -q -k "authorization or transactions or mcp"` from this track after completing TODOs. Add a changed-summary-after-approval case, two simultaneous retries, a wrong-resource request, and a missing API key. For response-loss practice, discard a successful response deliberately, query by operation ID, then retry and verify the same ticket ID. State that deliberate response discard simulates this failure; do not claim a physical network outage.

Submit code, your identity/transaction diagram, tests, and one trace showing why an action was allowed or denied. Rubric: authorization 20, atomic commit 35, MCP integration 25, added tests and explanation 20. Default notebook execution is setup only; all checks must be enabled for assessment.

## Next Steps
Lab 19 packages this service and evolves its schema. Source: [official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), [SQLite transactions](https://www.sqlite.org/lang_transaction.html), [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/). Interfaces checked 2026-10-08 against the recorded package versions.''')])

save('19_local_delivery_and_migrations',[
md('''## Goal
Build and operate your own application image with Docker Compose, implement a release gate and an additive database migration, and rehearse a rollback. Prerequisite: completed Lab 18. Plan two sessions (3–4 hours, an unpiloted estimate). Cloud deployment is optional; local Compose is the required target.

An image packages application code and dependencies. A container is a running instance. The named volume preserves the ticket ledger when the process or container is replaced. A readiness response shows that a service can answer that probe; it does not establish business correctness. Release checks must include ticket creation, approval, tenant isolation, and replay.'''),
md('''## Steps
### 1. Inspect and build your application
Read the Dockerfile, `.dockerignore`, and compose.yaml. Explain each COPY boundary and why instructor solutions and credentials must stay outside the build context. From this folder, after completing Lab 18:

```bash
COURSE_RELEASE=v1 docker compose build
COURSE_RELEASE=v1 docker compose up -d --wait
curl --fail http://127.0.0.1:58018/health
```

Use a second terminal to submit an approval with alpha-reviewer-demo and then the matching ticket with alpha-demo. Use the same JSON operation_id/resource/summary for both requests. Repeat the ticket request and compare IDs. Do not add an approved field: the server forbids it. Save image IDs and responses in student-results; the default starter cannot pass business tests until you implement it.'''),
md('''### 2. TODO 19.1 — make a release decision
Implement `release_gate` in submission.py. Accept exactly tests, failures, unauthorized_effects, replay_duplicates. Counts must be nonnegative integers excluding booleans; at least one test must run, and all three failure counts must be zero. Missing, malformed, or extra fields reject the release. These are teaching criteria, not a complete production risk policy. A hand-written all-zero report is not evidence: retain test output and trace IDs supporting each count.'''),
code('''if RUN_EXERCISES:
    importlib.reload(impl)
    checks.releases(impl)
    print("Release decision contracts passed")'''),
md('''### 3. TODO 19.2 — evolve the ledger
Implement `upgrade_schema(conn)` in submission.py. Use an explicit transaction, inspect PRAGMA table_info(tickets), add created_by TEXT NOT NULL DEFAULT 'legacy' only if absent, and insert schema version 2 only if absent. Preserve rows and support a repeated migration. Roll back if any step fails. Do not drop tables or delete the volume.

Run the migration against the container's ledger using `docker compose exec api python` and your function. Record before/after schema versions, then repeat a pre-migration ticket request. The additive column with a default is chosen to let the previous application keep working; this compatibility must still be tested.'''),
code('''if RUN_EXERCISES:
    importlib.reload(impl)
    checks.migration(impl)
    print("Additive migration, repeat migration, old replay, and new insert passed")'''),
md('''### 4. Exercise a broken release and rollback
Keep your v1 image. Make a controlled application change in your own branch that breaks a contract, run the tests, and confirm the gate rejects it. Repair the change, build v2, run business smoke checks, then roll back with:

```bash
COURSE_RELEASE=v1 docker compose up -d --no-build --wait
```

Verify the reported version, existing ticket IDs, and approval behavior. Rolling back code does not undo database effects. Record whether your schema remains compatible. Stop your course stack with `docker compose down`; retain its named volume. Never use `down -v` as routine cleanup.'''),
md('''## Checks and submission
Submit v1/v2 image IDs, build commands, real API smoke results, migration evidence, gate decisions, and rollback results. Add a test where a dependency is unavailable. Keep that separate from an injected exception test. `ci-template.yml` is an optional GitHub Actions starting point to copy into your own repository; hosted CI is not run by this notebook.

Rubric: working image/Compose 30, gate 20, migration 25, rollback and evidence 25. Automated reference checks do not substitute for your own Docker demonstration.

## Next Steps
Lab 20 measures the service. References: [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/), [SQLite ALTER TABLE](https://www.sqlite.org/lang_altertable.html), [GitHub Python CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).''')])

save('20_observability_performance_cost',[
md('''## Goal
Record real HTTP measurements, aggregate failures honestly, and design an optimization experiment with authorization and freshness constraints. Prerequisites: Labs 14, 18–19 and chapter 13. Plan two sessions (3–4 hours, unpiloted).

The first measurement targets the health endpoint to isolate HTTP/process overhead. It does not measure RAG or model inference. Your submission repeats the method on the integrated retrieval/action path and labels stages separately. Traces should identify request, component, duration, status, and configuration version; exclude API keys and unnecessary document text.'''),
md('''## Steps
### 1. TODO 20.1 — calculate trustworthy summaries
Implement summarize(rows). Each row has success (boolean), latency_ms and cost (finite nonnegative numbers). Include failed requests in the attempted denominator and latency distribution. Return the fields listed in submission.py. p95 uses the nearest-rank convention; with n samples its zero-based index is ceil(0.95*n)-1. For no attempts, rates and percentiles are null. For no successes, cost per success is null.

The exact-value fixture below is invented and uses arbitrary cost units. It checks arithmetic, not API billing. Observed provider usage and the applicable rate schedule are required before reporting monetary model costs.'''),
code('''if RUN_EXERCISES:
    importlib.reload(impl)
    rows=[{"success":True,"latency_ms":2.,"cost":.3},{"success":False,"latency_ms":10.,"cost":.2}]
    print(impl.summarize(rows))'''),
md('''### 2. TODO 20.2 — isolate cache entries
Implement cache_key(tenant,resource,version) and validate its inputs. Include every listed field in the returned tuple. Then design a read-cache experiment: populate one tenant/version, update the source, and prove that a new version does not receive stale evidence. Do not cache a write operation as if it were a read. The key exercise alone does not implement a cache or prove correct invalidation in a deployed system.'''),
code('''if RUN_EXERCISES:
    importlib.reload(impl)
    checks.measurements(impl)
    print("Denominators, invalid times, empty runs, tenant and version keys checked")'''),
md('''### 3. Measure a real local service
The following invokes actual HTTP requests, with a 3-second request timeout and bounded worker count. Each request creates its own client, so connection setup contributes to latency. It records zero model cost because this endpoint calls no model; it does not claim zero hosting cost. The helper launches and stops its own temporary service, independently of your Compose project.'''),
code('''if RUN_EXERCISES:
    from engineeringlab.harness import running_service
    from engineeringlab.bench import measure
    with running_service(MODULE) as url:
        experiments=[]
        for workers in (1,2,4):
            rows=measure(url,n=20,workers=workers)
            experiments.append({"workers":workers,**impl.summarize(rows)})
    for row in experiments:print(row)
    print("Observed local HTTP results; no causal scaling conclusion from this single ordered run.")'''),
md('''### 4. Design and run your comparison
Measure your Compose service and your Lab 16 retrieval endpoint. Keep workload, data, package/model versions, and final answer contract fixed. Separate warm-up and measured requests, change run order, and repeat conditions. Compare one change at a time: candidate count, eligible-read caching, connection reuse, or independent read parallelism. Retain failures and quality checks.

Optional live extension: use your own Gemini account, declare a spending limit before execution, record actual usage and failures, and compare against a simple baseline. A request count is not a monetary guarantee. Never report the fixture cost units above as dollars. GPU access is unnecessary for the required HTTP experiments.'''),
md('''### 4. TODO 20.3 — inspect an actual request trace
Implement trace_event, then start the service with COURSE_TRACE=1. The supplied middleware measures requests and emits your allowlisted JSON event to the Uvicorn log. Request bodies, keys, and URL parameter values are excluded. Send an approved request and a denied request. Match the X-Request-ID response header to each logged event and explain its HTTP status. Save the JSON event lines as JSONL. The route field is a template, not a raw URL.

Add a test passing a secret inside an extra headers argument and verify it is absent from the returned event. Run tests/test_engineering.py after implementing the function. These are local structured request logs; distributed OpenTelemetry spans and an external collector are optional extensions. Do not describe this exercise as distributed tracing.'''),
md('''## Checks and submission
Submit raw JSONL observations, a configuration manifest, a results table (attempts, successes, p50/p95, timeouts, cost units), and a short explanation. Plot distributions if your sample supports it. Include at least one failed request and explain its denominator treatment. Define your acceptance criteria before comparing configurations. No speedup is required for full credit; a sound negative result is valid.

Rubric: aggregation 20, cache identity/freshness experiment 15, safe request traces 15, actual measured comparison 30, interpretation/reproducibility 20. A 20-request exercise is practice, not a production capacity claim.

## Next Steps
Complete the course capstone using the offline outcome or the advanced live-evidence outcome. Reference: [Python statistics](https://docs.python.org/3/library/statistics.html), [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/), chapter 13 of the course textbook.''')])
print('Built three student assignments and three instructor copies')
