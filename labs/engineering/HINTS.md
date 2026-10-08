# Staged hints

Read only the row for your current TODO. First explain the invariant in words; then inspect the suggested interface. These hints leave the implementation to you.

| TODO | First hint | Next interface to inspect |
|---|---|---|
| 18.1 authorization | Python True and integer 1 compare equal; the contract distinguishes them | type(value), membership |
| 18.2 transaction | Read and decide under the same write transaction; both identity columns matter | BEGIN IMMEDIATE, parameterized SELECT/INSERT, commit/rollback |
| 18.3 MCP | The decorated function calls HTTP; it does not approve its own request | server.tool(), client.post/get, raise_for_status |
| 19.1 release gate | Reject malformed evidence before comparing counts | exact dictionary keys, type(count) |
| 19.2 migration | Check whether the column exists before adding it; repeat safely | PRAGMA table_info, ALTER TABLE, INSERT OR IGNORE |
| 20.1 metrics | Count attempts before filtering successes; failures still cost time | sorted, median, ceil, isfinite |
| 20.2 cache identity | A result for another tenant or document version is a different cache entry | immutable tuple, validated inputs |
| 20.3 trace | Build a new record from allowed fields; do not redact an arbitrary copied body | explicit dictionary construction |

For the MCP API use the version linked in the track README. A failed transport test may be a server-startup error rather than an authorization failure; inspect stderr and the first exception. Do not write diagnostic text to the stdio protocol's stdout.
