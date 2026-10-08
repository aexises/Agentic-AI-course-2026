# Validation record — Labs 12–16

Checked **2026-10-07**. This record distinguishes executed behavior from suggested student work. The stack uses real local neural models and a real PostgreSQL service; optional Gemini generation was disabled.

## Executed checks

| Check | Observed result | Evidence |
|---|---|---|
| Unit tests | 27 passed | [Combined JUnit report](validation/all-tests.xml) |
| Database/model integration tests | 6 passed | Same report; real embeddings, reranking, atomic replacement/rollback, tenant filters, both ANN index plans, API contracts, injected database failure |
| Network service test | 1 passed | Same report; a temporary Uvicorn process served actual localhost HTTP requests |
| Student notebooks | All 5 passed in fresh kernels | [Notebook execution manifest](validation/notebook-results.json); worked cells executed, unfinished student exercises disabled |
| Instructor notebooks | All 5 passed in fresh kernels | Same manifest; exercise solutions and their checks enabled |
| Development evaluation | 20 query/method runs completed | [Query-level JSON](validation/dev-evaluation.json), five development questions × four methods |

The combined test invocation reported **34 passed, 1 warning**. Tests included empty/invalid inputs, wrong vector dimensions, nonfinite vectors, duplicate document identities, SQL-injection-shaped tenant values, stale versions, transaction rollback, authentication failures, strict request validation, admission-limit rejection, and a sanitized simulated database error. The simulated error is not a physical database outage test. The HTTP test starts and terminates its own service process.

Both exported figures were visually inspected: [index experiment](validation/13_pgvector_indexing-1.png) and [retrieval comparison](validation/14_hybrid_search_reranking-1.png). Labels and plotted content were legible. Notebook structure, saved outputs, execution counts, and absence of error outputs were checked separately. Full notebook layout in a browser was not visually verified because local-file browser preview was unavailable.

## Reproducibility

- Python 3.12.14, CPU execution on macOS; [execution manifest](validation/notebook-results.json) records the platform and core package versions.
- PostgreSQL **17.8**, server extension pgvector **0.8.1**: [database version](validation/database-version.txt). The Python client package `pgvector==0.5.0` is a different component.
- Database image: `pgvector/pgvector:0.8.1-pg17`; inspected image ID `sha256:3e8b3adfd27b5707128f60956f62a793c3c9326ea8cfaf0eab7adccb5d700b21`.
- [Direct package pins](requirements.txt), [complete installed package snapshot](requirements-lock.txt), and [immutable model revisions](models.lock.json) are retained. The complete package snapshot is from this platform, not a claim of cross-platform reproducibility. `pip check` reported no broken requirements.
- The encoder was copied from an existing local cache at the locked revision; the reranker files were downloaded from the locked upstream revision. A clean-room first download through `raglab.prepare_models` was not reproduced.
- The seeded fixture had **17 documents and 17 chunks** at the default splitter setting. Temporary exercise records were cleaned up. The fixture is invented teaching data, not a benchmark sampled from real users.
- Notebook validation used `OMP_NUM_THREADS=2`, `TOKENIZERS_PARALLELISM=false`, and `HF_HUB_OFFLINE=1`. Gemini/OpenAI credentials were removed from kernel environments; `RUN_GENERATION` remained false. Fresh model/package downloads are a separate preflight step.

Run the commands in the [README](README.md) to reproduce the checks. Rebuilding notebooks clears outputs; rerun the validator afterward so saved output and hashes describe the rebuilt notebooks.

The dedicated course database container was stopped after validation; its data volume was retained. Start it with the README preflight command before running notebooks again.

## Reranker failure found and repaired

The initial integration run failed three checks because the cross-encoder returned NaN scores. Its parameters were finite. With the tested torch **2.14.1** stack, the first attention query linear layer produced some nonfinite values using loaded parameter storage; the same operation with cloned weight values was finite. Switching attention implementation alone did not resolve it. Running the model in float64 produced a finite score, and cloning all parameters into independent contiguous float32 storage also restored finite scores.

`raglab.models.cross_encoder` now performs that explicit copy once when loading. It does not alter weight values, substitute a different model, or replace invalid scores. Output validation still rejects nonfinite results. The exact underlying runtime defect was not established; the storage-copy workaround is supported by this local experiment and subsequent end-to-end checks, not a universal claim about torch. The full 34-test suite and all ten notebook executions passed after the change.

## Interpretation of the development run

| Method | Mean Recall@5 | Mean MRR@5 | Mean nDCG@5 |
|---|---:|---:|---:|
| PostgreSQL lexical ranking | 0.400 | 0.300 | 0.326 |
| Dense | 1.000 | 0.900 | 0.926 |
| Hybrid RRF | 1.000 | 0.900 | 0.926 |
| Hybrid + cross-encoder | 1.000 | 0.850 | 0.886 |

These are arithmetic means over **five labeled development questions**, rounded to three decimal places. Reranking did not improve recall and lowered the two rank-sensitive metrics in this run. This is a useful failure-analysis exercise, not evidence for a universal ranking of retrieval methods. The public test split was not evaluated during this validation. Query timings include cold starts, cache/order effects, and concurrent local activity; they do not establish production latency or capacity.

## Remaining limits

- Optional Gemini requests, generated-answer correctness, and citation entailment were not tested.
- The database container was executed. The separate optional API Docker image was not built or run; the host Uvicorn service was tested. The combined Compose configuration passed validation.
- No student pilot, grading reliability study, load test, external identity provider, TLS deployment, or database RLS policy was validated. Lab durations are planning estimates.
- Starlette emitted an `httpx` TestClient deprecation warning; the tests still passed. Some notebook kernels emitted local TCP transport warnings, the progress bar reported missing optional `ipywidgets`, and the deliberately small splitter setting emitted a short-chunk warning. These are not hidden as successful production readiness checks.
- Primary documentation links were inspected when authoring the labs. Version-sensitive behavior was then checked against the installed packages. No claim that these compact MiniLM models are state of the art is made.
