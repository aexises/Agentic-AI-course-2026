# Practical RAG engineering: Labs 12–16

This required track leads into [MCP and local operation Labs 18–20](../engineering/README.md). Read the [backend primer](../engineering/BACKEND-PRIMER.md) before the service exercises. The final [capstone](../../teaching/CAPSTONE.md) integrates pgvector retrieval with an approved action service; fine-tuning is optional.

Build one working application across five labs: **LlamaIndex → embeddings → PostgreSQL/pgvector → hybrid retrieval → neural reranking → FastAPI**. The required database is pgvector. Milvus/Pinecone remain an optional portability extension in Lab 16, so the core sequence gives students repeated practice with PostgreSQL and FastAPI.

| Lab | Students actually implement | Deliverable |
|---|---|---|
| [12 · Ingestion](12_llamaindex_ingestion.ipynb) | LlamaIndex transformations, embedding batches, versioned persistence and update/delete checks | Ingestion code and manifest |
| [13 · pgvector indexing](13_pgvector_indexing.ipynb) | Parameterized SQL, HNSW/IVFFlat DDL, EXPLAIN analysis, filtered-neighbor experiments | SQL and measurement report |
| [14 · Hybrid search](14_hybrid_search_reranking.ipynb) | Rank fusion and retrieval→cross-encoder integration; compare lexical/dense/hybrid methods | Query-level relevance evaluation |
| [15 · FastAPI](15_fastapi_rag_service.ipynb) | A typed route, tenant dependency, HTTP contract tests, real Uvicorn requests | Python application and API tests |
| [16 · Integration](16_pgvector_fastapi_capstone.ipynb) | Service smoke checks, update verification, evaluation summary, deployment/failure drill | Running service and reproducible report |

Labs 12–15 are planned for 120 minutes each after preflight. Lab 16 is a two-session capstone (two 90-minute sessions) or take-home assignment. Durations are estimates, not pilot measurements. Prerequisites include Python, basic SQL, HTTP concepts, and the earlier RAG/framework labs. Teach this sequence after textbook chapters 5–7 and alongside chapters 11–13.

## Preflight: before the teaching session

Use Python 3.12 and Docker with Compose. Keep this environment separate from Labs 3–11. From the course root:

```bash
python3.12 -m venv .venv-rag
source .venv-rag/bin/activate
python -m pip install -r labs/rag/requirements.txt
python -m pip install --no-deps -e labs/rag
python -m pip check
python -m ipykernel install --user --name course-rag --display-name 'Course RAG'
docker compose -f labs/rag/compose.yaml up -d --wait
python -m raglab.prepare_models
python -m raglab.seed
```

Select **Course RAG** as the notebook kernel. The notebooks require the complete `labs/rag` directory and editable package. They are not single-file Colab examples. Docker must run on the same host or be deliberately configured with a reachable database; this remote arrangement is not the default classroom setup.

Package/model downloads need internet access. The two local models run on CPU; the first load and model download can dominate setup time. Prepare and test the environment before class. `prepare_models` uses the shipped `models.lock.json` revisions and records them in `models/manifest.json`. Runtime model loading uses local files only. Keep the manifest with submitted results. Model weights/cache directories are excluded from version control.

The default database URL is `postgresql://course:course-local-only@127.0.0.1:55432/rag_course`. These are public, local teaching credentials. Override with `RAG_DATABASE_URL` if needed. The supplied Compose project binds the database only to localhost and uses its own named volume. `python -m raglab.seed` upserts the supplied documents and retains unrelated records; it does not truncate tables. The code creates only the `rag_course` schema, its tables/indexes, and the vector extension. Use a dedicated teaching database, not a production one.

If a database or model is missing, the notebooks fail explicitly. There is no automatic substitution with random embeddings, fake retrieval, or a mock database. Unit tests can use injected failures, but database integration checks require the real stack.

## Service practice

From `labs/rag`, with the environment active:

```bash
export RAG_API_KEYS='{"student-alpha":"alpha","student-beta":"beta"}'
uvicorn raglab.service:create_app --factory --host 127.0.0.1 --port 58000
```

Open [local API documentation](http://127.0.0.1:58000/docs). In another terminal:

```bash
curl -sS http://127.0.0.1:58000/search \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: student-alpha' \
  -d '{"query":"How long can I borrow a camera?","k":5,"rerank":true}'
```

The reference app serves retrieval results; it does not label retrieved passages as verified answers. Lab 16 has an explicit optional Gemini generation step using those results. The service teaches lifespan startup/cleanup, a connection pool, Pydantic request/response models, dependency-based tenant selection, admission limits, SQL timeouts, and sanitized database errors. It is not a complete production security system: no TLS, external identity provider, database RLS, distributed rate limiting, or end-to-end inference deadline is supplied.

Students implement `/student-search` in the notebook and then move it into their own Python application module. A notebook-defined route does not automatically appear in a separate Uvicorn process. The shipped `raglab/service.py` is a reference application to inspect and test, not a substitute for this submission.

For an optional containerized API, from `labs/rag`:

```bash
docker compose -f compose.yaml -f compose.api.yaml up --build -d --wait
```

Stop any host Uvicorn process on port 58000 first. Model snapshots are mounted read-only from `./models`. Stop this project with `docker compose -f compose.yaml -f compose.api.yaml down`; the named database volume is retained. Removing the volume erases its teaching data, so that is not part of routine cleanup.

## Exercise and assessment workflow

Student notebooks execute worked cells by default. Implement TODOs, set `RUN_EXERCISES=True`, restart the kernel, and run all. Instructor solutions are in [instructor/](instructor/); exclude that directory from student distribution. Each notebook defines contracts, starter checks, submission artifacts, and a 100-point rubric. Add unseen failure cases for grading rather than relying only on the visible assertions.

The reference package exposes implementation details deliberately. Require students to explain their SQL, inspect query plans, modify pipeline settings, and implement routes; copying an invocation of the reference service is insufficient. [Instructor guide](INSTRUCTOR-GUIDE.md) contains grading prompts and preparation checks.

## Data, models, and measurement

[data/documents.json](data/documents.json) contains 17 invented English policy documents: 16 for alpha and one private beta marker document. [data/questions.json](data/questions.json) contains five development questions and seven public test questions, including one unanswerable question. Relevant-document labels are authored teaching judgments. They are not a representative benchmark, and the public test split is not a secret assessment set.

The MiniLM bi-encoder and MS MARCO cross-encoder are compact teaching baselines. They are not presented as state-of-the-art model choices. The architecture can be reused with other models, but changing embedding dimension or model requires a compatible schema and re-embedding the corpus.

Important distinctions to preserve in reports:

- LlamaIndex pipeline transformations/caching and database version/upsert policy are separate mechanisms.
- PostgreSQL `ts_rank_cd` is not BM25. An additional `rank-bm25` comparison is optional.
- HNSW/IVFFlat neighbor recall against an exact query is not relevance against human labels.
- Reciprocal rank fusion combines rankings; the cross-encoder separately scores query/passage pairs.
- Reranker scores are not calibrated probabilities or universal abstention thresholds.
- Citation-ID membership does not establish entailment or answer correctness.
- The application tenant filter is not database row-level security.

Freeze configurations before evaluating the public test split:

```bash
python -m raglab.evaluate --split dev --output student-results/dev.json
python -m raglab.evaluate --split test --output student-results/final.json
```

The report records versions, model revisions, corpus hash, query-level results, and elapsed times. Query times include cold-start/order effects and are not load-test performance claims. No-answer queries have null relevance metrics and need separate abstention assessment.

## Rebuild and verify

From the course root, in this track's environment:

```bash
python scripts/build-rag-labs.py
python -m pytest labs/rag/tests/test_unit.py -q
python -m pytest labs/rag/tests/test_integration.py -q
python -m pytest labs/rag/tests/test_http.py -q
python scripts/validate-rag-labs.py
```

The builder generates all ten notebooks and clears old outputs. The validator executes them in fresh kernels with Gemini keys removed and generation disabled, retaining executed outputs and a hash manifest. It exports notebook figures for inspection. Unit/integration tests are separate so a unit-only pass cannot be mistaken for a database/model validation pass. See [validation record](VALIDATION.md) for actual tested scope.

Optional Gemini use requires `GEMINI_API_KEY`, `GEMINI_MODEL`, and explicit `RUN_GENERATION=True` in Lab 16. It consumes provider quota and is not part of the default validation. No OpenAI API key is needed for these labs.

## Primary references

Documentation checked 2026-10-07. Mutable documentation may differ from pinned package behavior; report the versions actually executed.

- [LlamaIndex ingestion pipeline](https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline/)
- [pgvector](https://github.com/pgvector/pgvector)
- [PostgreSQL text search](https://www.postgresql.org/docs/current/textsearch-controls.html) and [EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [Sentence Transformers cross-encoder usage](https://www.sbert.net/docs/cross_encoder/usage/usage.html)
- [Embedding model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) and [reranker model card](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2)
- [FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/), [dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/), and [testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [psycopg pool lifecycle](https://www.psycopg.org/psycopg3/docs/advanced/pool.html)
- [Docker Compose startup dependencies](https://docs.docker.com/compose/how-tos/startup-order/)
- [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output)
