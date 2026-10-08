# Backend bridge for a Python/ML learner

You already know Python functions. A web service exposes a function across a process boundary: a caller serializes arguments, sends a request, waits for a response, and must handle the possibility that the response never arrives. A timeout describes what the caller observed; it does not prove that the server did nothing.

## 1. Inspect a request

Start the Lab 18 service after implementing its TODOs. In another terminal send the following synthetic operation. The first request is from a reviewer; the second is from an agent. The keys below are public teaching fixtures.

```bash
curl --fail-with-body http://127.0.0.1:58018/approvals   -H 'Content-Type: application/json' -H 'X-API-Key: alpha-reviewer-demo'   -d '{"operation_id":"practice-1","resource":"camera","summary":"Check lens"}'
curl --fail-with-body http://127.0.0.1:58018/tickets   -H 'Content-Type: application/json' -H 'X-API-Key: alpha-demo'   -d '{"operation_id":"practice-1","resource":"camera","summary":"Check lens"}'
```

Repeat the second request. Your implementation should return the same ticket ID with replayed=true. Change the summary without new approval: expect denial. Add an approved field: expect request-schema rejection. Remove the agent key: expect an authentication failure. Explain each result before reading the test.

A 2xx response signals HTTP success; it is still your responsibility to check the business result. A 4xx response usually tells you the request cannot be accepted as sent. A 5xx response indicates server-side failure. Do not automatically retry every error. Use [FastAPI's testing tutorial](https://fastapi.tiangolo.com/tutorial/testing/) and the supplied HTTP checks to connect the request to the route.

## 2. Relate database state to business operations

A primary key uniquely identifies a row. The ticket key is (tenant, operation_id), not just a random ticket ID. A transaction makes a group of changes commit together or roll back. The supplied SQLite connection context commits or rolls back and closes the connection; your commit function explicitly controls its own write transaction. BEGIN IMMEDIATE attempts to acquire the write transaction before reading for a duplicate. SQLite permits one writer at a time; contention can still fail after the configured wait. [SQLite transaction documentation](https://www.sqlite.org/lang_transaction.html).

Rehearsal: create one operation, query its row, replay it, and count rows. Open another connection and repeat. Next send two retries concurrently. A check followed by an unprotected insert is not enough: the primary key and transaction must enforce the contract.

Keep SQL values in parameters, not string interpolation. An index helps a query access rows but does not replace relevance evaluation. In Labs 12–16, pgvector stores retrieval vectors in PostgreSQL; the local ticket ledger here isolates the transaction lesson. The capstone uses both.

## 3. Understand process and container boundaries

An image is the packaged application; a container runs it. Compose describes services, ports and volumes. A host port forwards traffic to the container port. A named volume preserves ledger data across replacement of the container. It is not a backup. A dependency being started does not mean it is ready; use readiness conditions and actual business probes. [Docker startup guidance](https://docs.docker.com/compose/how-tos/startup-order/).

Rehearsal: build v1, create a ticket, restart the container, query the same ticket. Stop with docker compose down and restart; verify it remains. Do not use down -v for this exercise because that deletes the volume. Save the image ID, not only a mutable tag.

## 4. Change code and schema separately

An additive column with a default can allow old insertion code with explicit column names to keep working. That compatibility is a hypothesis until tested. A code rollback does not reverse a database migration. Lab 19 requires old-row replay and a new insert after migration, then operation by the earlier image. [SQLite ALTER TABLE](https://www.sqlite.org/lang_altertable.html).

For the container migration, from this track after implementing upgrade_schema:

```bash
docker compose exec -T api python - <<'PYCODE'
import os
from engineeringlab.support import connect
from submission import upgrade_schema
with connect(os.environ['COURSE_TICKET_DB']) as conn:
    upgrade_schema(conn)
    print([tuple(r) for r in conn.execute('PRAGMA table_info(tickets)')])
PYCODE
```

## 5. Debug one boundary at a time

First verify the selected Python environment and imports. Then check service readiness, HTTP status/body, approval identity, and database state. Finally inspect the MCP client result. Preserve the first meaningful error; repeated restarts without new evidence lose information.

If the port is occupied, identify your own service before stopping it; do not kill unrelated processes. If Docker is unavailable, finish function tests and record the deployment task as incomplete. If a request times out, query by operation ID before retrying. HTTPX distinguishes connection, read, write and pool timeouts; these do not together imply a strict end-to-end deadline. [HTTPX timeout documentation](https://www.python-httpx.org/advanced/timeouts/).
