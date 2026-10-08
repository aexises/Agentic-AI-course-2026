"""Build five practical student notebooks and matching instructor solutions."""
from pathlib import Path
import copy
import nbformat as nb
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'labs/rag'
def md(s): return nb.v4.new_markdown_cell(s.strip())
def code(s): return nb.v4.new_code_cell(s.strip())
def task(text,stub,solution,checks):
    return [md(text),{'stub':stub,'solution':solution},code('if RUN_EXERCISES:\n'+'\n'.join('    '+line for line in checks.strip().splitlines()))]
def save(name,cells):
    for solved in (False,True):
        cc=[]
        for c in cells:
            if 'stub' in c: cc.append(code(c['solution'] if solved else c['stub']))
            else:
                c=copy.deepcopy(c)
                if solved and c.cell_type=='code': c.source=c.source.replace('RUN_EXERCISES = False','RUN_EXERCISES = True')
                cc.append(c)
        n=nb.v4.new_notebook(cells=cc,metadata={'kernelspec':{'name':'python3','language':'python','display_name':'Course RAG'},'language_info':{'name':'python'}})
        for i,c in enumerate(n.cells): c.id=f'{name[:2]}-{i:03}'
        nb.validate(n);nb.write(n,OUT/('instructor' if solved else '')/(name+'.ipynb'))
SETUP_MD='''## Setup
Complete the track README preflight first: install this track's pinned environment and editable package; start PostgreSQL/pgvector with Docker Compose; download the two pinned model snapshots; seed the invented course corpus. Select that Python environment as the kernel. These notebooks need the **whole `labs/rag` folder**, not a standalone upload. They use a real database and local neural models. Missing services or models are errors, not silently replaced by mocks.

Run worked cells first, then implement TODOs, set `RUN_EXERCISES=True`, restart, and run all. Instructor copies enable those checks. `RUN_GENERATION` stays false unless you deliberately enable the separately documented Gemini request. Offline here means no inference API calls after package/model downloads; PostgreSQL is still a real local service. All data are invented and English-language. Never use this teaching database or its public example keys for real student records.'''
SETUP='''import json
from pathlib import Path
from importlib.metadata import version
import numpy as np
from raglab.config import ROOT, DIMENSION
from raglab import db, models
from raglab.ingestion import corpus, chunk_documents, make_pipeline
RUN_EXERCISES = False
RUN_GENERATION = False
print({p:version(p) for p in ("llama-index-core","pgvector","psycopg","fastapi","sentence-transformers")})
with db.connect() as conn:
    print(conn.execute("SELECT extversion FROM pg_extension WHERE extname='vector'").fetchone())'''

def start(title,goal):return [md('# '+title+'\n## Goal\n'+goal),md(SETUP_MD),code(SETUP)]

cells=start('Lab 12 · LlamaIndex ingestion into pgvector','Build and change an ingestion pipeline, generate real embeddings, and persist versioned documents. Prerequisites: Python functions/dictionaries, introductory SQL, Lab 6. Plan for 120 minutes after environment setup: 20 exploration, 45 implementation, 30 experiments, 25 tests/report. Timing is a teaching estimate.\n\nDeliver an ingestion manifest and evidence that re-ingestion, updates, and deletion behave correctly. You will use LlamaIndex `Document`, `SentenceSplitter`, and `IngestionPipeline`; PostgreSQL transactions own persistence in this implementation.')
cells += [md('''## Steps
### 1. Inspect actual chunks and embeddings
The fixture corpus contains two tenants. Chunk IDs incorporate tenant, document, version, ordinal, and content. Metadata stays attached to chunks but is excluded from the embedding text in this pipeline. Inspect the consequence of excluding the title: retrieval may lose a useful signal. The embedding snapshot is a compact teaching baseline, not a claim of current model superiority.'''),code('''records=corpus()
alpha=[r for r in records if r["tenant"]=="alpha"]
chunks=chunk_documents(alpha[:2])
vectors=models.embed([c["text"] for c in chunks])
assert vectors.shape==(len(chunks),384)
assert np.allclose(np.linalg.norm(vectors,axis=1),1,atol=1e-5)
assert len({c["chunk_id"] for c in chunks})==len(chunks)
print({"documents":len(records),"chunks_in_example":len(chunks),"vector_shape":vectors.shape})
print({k:chunks[0][k] for k in ("doc_id","version","source","text")})'''),md('''### 2. Inspect chunk boundaries
Use actual text, not just a chunk count, to decide whether an exception remains with its rule. Smaller chunks may lose context; overlapping chunks may repeat evidence. Do not tune chunking using the public assessment split. A chunk-size parameter is measured in the splitter's tokenizer units, not characters.'''),code('''for size,overlap in [(32,0),(64,8),(96,12)]:
    sample=chunk_documents([alpha[1]],make_pipeline(size,overlap))
    print({"chunk_size":size,"overlap":overlap,"chunks":len(sample)})
    print([c["text"] for c in sample])''')]
cells+=task('''### 3. TODO: configure and inspect a LlamaIndex pipeline (30 points)
Implement `student_chunks(records, size, overlap)` by constructing `IngestionPipeline` with `SentenceSplitter`, then passing it to `chunk_documents`. Enforce the same size/overlap contract as `make_pipeline` (size 32–256, overlap 0..size-1, integers excluding booleans). Do not call `make_pipeline` in your implementation. Preserve metadata and return stable chunk IDs.''','''def student_chunks(records,size,overlap):
    raise NotImplementedError("Build the LlamaIndex transformation pipeline")''','''def student_chunks(records,size,overlap):
    from llama_index.core.ingestion import IngestionPipeline
    from llama_index.core.node_parser import SentenceSplitter
    if type(size) is not int or type(overlap) is not int or not 32<=size<=256 or not 0<=overlap<size:
        raise ValueError("invalid chunk parameters")
    pipeline=IngestionPipeline(transformations=[SentenceSplitter(chunk_size=size,chunk_overlap=overlap)])
    return chunk_documents(records,pipeline)''','''assert student_chunks([],64,8)==[]
a=student_chunks(alpha[:2],64,8)
b=student_chunks(alpha[:2],64,8)
assert [c["chunk_id"] for c in a]==[c["chunk_id"] for c in b]
assert all(c["tenant"]=="alpha" and c["source"].startswith("course://") for c in a)
for args in [(True,0),(31,0),(64,64),(64,-1)]:
    try: student_chunks(alpha[:1],*args)
    except ValueError: pass
    else: raise AssertionError("invalid chunk configuration accepted")''')
cells+=task('''### 4. TODO: persist, re-ingest, and update (40 points)
Implement `ingest_one(record)` using your splitter (64,8), `models.embed`, and `db.replace_document`. Return the number of chunks. Read `raglab/db.py`: identify the row lock, transaction boundary, and cascading foreign key. The helper replaces only the specified tenant/document; it never truncates the corpus. Tests use an isolated teaching tenant and remove only their own document.''','''def ingest_one(record):
    raise NotImplementedError("Chunk, embed, and atomically replace one document")''','''def ingest_one(record):
    parts=student_chunks([record],64,8)
    vectors=models.embed([p["text"] for p in parts])
    db.replace_document(record,parts,vectors)
    return len(parts)''','''record=dict(alpha[0],tenant="exercise12",doc_id="temporary",source="course://exercise12/temporary")
try:
    count=ingest_one(record)
    assert ingest_one(record)==count
    with db.connect() as conn:
        actual=conn.execute("SELECT count(*) AS n FROM rag_course.chunks WHERE tenant=%s AND doc_id=%s",("exercise12","temporary")).fetchone()["n"]
    assert actual==count
    updated=dict(record,version=2,body="Camera loans last four days in this isolated exercise.")
    ingest_one(updated)
    try: ingest_one(record)
    except ValueError: pass
    else: raise AssertionError("stale update accepted")
finally:
    db.delete_document("exercise12","temporary")
print("Ingestion, idempotent replay, version update, and cleanup checked")''')
cells += [md('''## Checks and submission
Save a small manifest: document count, chunk count, splitter settings, embedding snapshot revision, vector dimension, and source hashes. Add tests for duplicate document IDs, a blank body, and a database insert failure that must roll back the replacement. Compare two chunking configurations on development questions. Record a failure example even if aggregate scores are equal.

Rubric: pipeline 30, persistence 40, added tests 15, reproducible manifest and explanation 15. LlamaIndex pipeline caching is not the same as PostgreSQL upsert/version policy; identify which layer owns each operation.

## Next Steps
Lab 13 examines how pgvector searches the stored vectors. The student should be able to locate a returned chunk in the original document before treating it as evidence.

References checked 2026-10-07: [LlamaIndex ingestion](https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline/), [pgvector storage and indexes](https://github.com/pgvector/pgvector), [embedding model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).''')]
save('12_llamaindex_ingestion',cells)

cells=start('Lab 13 · pgvector indexes, SQL, and query plans','Write vector SQL, build HNSW and IVFFlat indexes, inspect plans, and compare approximate neighbors with an exact baseline. Prerequisite: Lab 12 and SQL SELECT/WHERE/ORDER BY. Planned 120 minutes: 20 SQL, 40 index work, 35 measurements, 25 failure tests/report.\n\nThe index experiment uses generated vectors to isolate database behavior. Its neighbor recall is not semantic relevance. PostgreSQL may reasonably choose a sequential scan on a tiny corpus; verify plans rather than assume the index was used.')
cells += [md('''## Steps
### 1. Execute a tenant-filtered cosine query
`<=>` is cosine distance; smaller values rank earlier. A distance operator and index operator class must match. Values are bound as parameters; table/index names must be trusted identifiers, not user text interpolated into SQL.'''),code('''query="How long can I borrow a camera?"
qv=models.embed([query])[0]
with db.connect() as conn:
    rows=conn.execute("""SELECT doc_id,text,embedding <=> %s AS distance
      FROM rag_course.chunks WHERE tenant=%s
      ORDER BY embedding <=> %s LIMIT %s""",(qv,"alpha",qv,3)).fetchall()
print([(r["doc_id"],round(r["distance"],4)) for r in rows])''')]
cells+=task('''### 2. TODO: implement a filtered vector query (30 points)
Write `student_search(conn,tenant,embedding,k)` using parameterized SQL against `rag_course.chunks`. Select `chunk_id`, `doc_id`, `text`, and distance; filter the tenant before returning results; order by cosine distance and limit k. Reject blank/non-string tenants and non-integer k outside 1–20, and validate the vector with `db.vector`. This application filter is not database row-level security.''','''def student_search(conn,tenant,embedding,k):
    raise NotImplementedError("Write the pgvector SQL query")''','''def student_search(conn,tenant,embedding,k):
    if not isinstance(tenant,str) or not tenant.strip() or type(k) is not int or not 1<=k<=20:
        raise ValueError("invalid tenant or k")
    v=db.vector(embedding)
    return conn.execute("""SELECT chunk_id,doc_id,text,embedding <=> %s AS distance
       FROM rag_course.chunks WHERE tenant=%s ORDER BY embedding <=> %s LIMIT %s""",(v,tenant,v,k)).fetchall()''','''with db.connect() as conn:
    assert student_search(conn,"nonexistent",qv,5)==[]
    assert student_search(conn,"alpha' OR true --",qv,5)==[]
    assert all("BETA-ONLY-MARKER" not in r["text"] for r in student_search(conn,"alpha",qv,20))
    for bad in (0,21,True,None):
        try: student_search(conn,"alpha",qv,bad)
        except ValueError: pass
        else: raise AssertionError("invalid k accepted")''')
cells += [md('''### 3. Run a controlled HNSW experiment
The temporary `ann_lab` table disappears when the connection closes. It contains normalized random vectors with a seeded generator. For the diagnostic ANN run we disable sequential scans to encourage an index plan; this setting is local to the transaction and is not a production tuning recommendation. Both the plan and result must be inspected. Eight queries are enough to practice the measurement procedure, not enough for stable performance conclusions.'''),code('''from raglab.benchmark import prepare,measure,recall
import matplotlib.pyplot as plt
with db.connect() as conn:
    vectors=prepare(conn,n=2000,seed=7)
    queries=vectors[::250].copy()
    exact,exact_ms=measure(conn,queries,exact=True)
    conn.execute("CREATE INDEX ann_hnsw ON ann_lab USING hnsw(embedding vector_cosine_ops) WITH (m=8,ef_construction=64)")
    conn.execute("SET LOCAL hnsw.ef_search=80")
    approximate,ann_ms=measure(conn,queries)
    conn.execute("SET LOCAL enable_seqscan=off")
    plan=conn.execute("EXPLAIN (FORMAT JSON) SELECT id FROM ann_lab ORDER BY embedding <=> %s LIMIT 10",(queries[0],)).fetchone()
    print(json.dumps(plan,default=str)[:1800])
    print({"neighbor_recall_at_10":recall(exact,approximate),"queries":len(queries)})
plt.figure(figsize=(7,3))
plt.plot(range(1,9),exact_ms,"o-",label="Exact")
plt.plot(range(1,9),ann_ms,"s-",label="HNSW, ef_search=80")
plt.xlabel("Query number (generated vectors)");plt.ylabel("Observed query latency (ms)")
plt.title("One local run: 2,000 generated vectors; includes order/cache effects")
plt.legend();plt.tight_layout();plt.show()''')]
cells+=task('''### 4. TODO: compare both approximate indexes (40 points)
Implement `build_index(conn,kind)` for the existing temporary `ann_lab` table. Drop only the two lab index names, then create either HNSW (`m=8`, `ef_construction=64`) or IVFFlat (`lists=16`), with `vector_cosine_ops`. Reject other kinds before issuing SQL. Use fixed SQL strings. Do not leave both indexes present when comparing plans. IVFFlat builds after data insertion in this experiment.''','''def build_index(conn,kind):
    raise NotImplementedError("Create the chosen pgvector index")''','''def build_index(conn,kind):
    if kind not in ("hnsw","ivfflat"): raise ValueError("unknown index")
    conn.execute("DROP INDEX IF EXISTS pg_temp.ann_hnsw")
    conn.execute("DROP INDEX IF EXISTS pg_temp.ann_ivfflat")
    if kind=="hnsw":
        conn.execute("CREATE INDEX ann_hnsw ON ann_lab USING hnsw(embedding vector_cosine_ops) WITH (m=8,ef_construction=64)")
    else:
        conn.execute("CREATE INDEX ann_ivfflat ON ann_lab USING ivfflat(embedding vector_cosine_ops) WITH (lists=16)")''','''with db.connect() as conn:
    vectors=prepare(conn,n=2000,seed=7)
    queries=vectors[::250]
    reference,_=measure(conn,queries,exact=True,cohort=0)
    for kind in ("hnsw","ivfflat"):
        build_index(conn,kind)
        conn.execute("SET LOCAL hnsw.ef_search=80")
        conn.execute("SET LOCAL ivfflat.probes=8")
        result,times=measure(conn,queries,cohort=0)
        score=recall(reference,result)
        assert 0<=score<=1
        print({"index":kind,"filtered_recall":score,"returned_counts":[len(r) for r in result]})
    try: build_index(conn,"hnsw; DROP TABLE x")
    except ValueError: pass
    else: raise AssertionError("unsafe index kind accepted")''')
cells += [md('''## Checks and submission
Run at least two `ef_search` settings and two `ivfflat.probes` settings, repeat query ordering, and retain EXPLAIN plans. Report build time, index size using `pg_relation_size`, returned result count, neighbor recall@10, and latency distribution. Include an empty tenant, wrong embedding dimension, zero vector, NaN, and a restrictive filter.

Do not report an ANN speedup from one query. In the filtered experiment, fewer than k returned rows is a result to investigate. Read pgvector's filtering/iterative-scan guidance before proposing a fix. Keep approximate-neighbor recall separate from human relevance labels.

Rubric: search SQL 30, index DDL 40, experiments 20, interpretation 10. Lab 14 measures relevance on the actual policy corpus.

## Next Steps
For production, evaluate a tenant/index strategy with realistic data and concurrency. This tiny fixture does not establish capacity or a universally best index.

References checked 2026-10-07: [pgvector exact search, HNSW, IVFFlat, filtering and EXPLAIN](https://github.com/pgvector/pgvector), [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html).''')]
save('13_pgvector_indexing',cells)

cells=start('Lab 14 · Hybrid search and neural reranking','Compare lexical retrieval, dense retrieval, rank fusion, and an actual cross-encoder on the same corpus. Prerequisites: Labs 12–13, basic evaluation metrics. Plan 120 minutes: 20 baselines, 40 implementation, 35 evaluation, 25 failure analysis.\n\nUse development questions to choose settings. Keep the public test split untouched until your final run; instructors should add private assessment cases. No improvement is assumed. The local cross-encoder is a teaching baseline, not a claim that its architecture or weights are SOTA.')
cells += [md('''## Steps
### 1. Compare candidates before generation
PostgreSQL full-text search here uses `ts_rank_cd`, **not BM25**. Lab vocabulary matters: rank fusion is also different from a neural reranker. The dense branch uses MiniLM embeddings; the reranker scores query/passage pairs with a separate cross-encoder. Its scores are not calibrated probabilities.'''),code('''from raglab.retrieval import retrieve,rrf,document_metrics
query="E-204"
with db.connect() as conn:
    dense=db.search(conn,"alpha",models.embed([query])[0],query,10,"dense")
    lexical=db.search(conn,"alpha",None,query,10,"lexical")
print("Dense:",[r["doc_id"] for r in dense[:5]])
print("Lexical:",[r["doc_id"] for r in lexical[:5]])
fused=rrf([dense,lexical])
reranked=models.rerank(query,fused,5)
print("Reranked:",[(r["doc_id"],round(r["rerank_score"],3)) for r in reranked])''')]
cells+=task('''### 2. TODO: implement reciprocal rank fusion (30 points)
Implement `student_rrf(rankings,c=60)` returning `(chunk_id,score)` pairs sorted by descending score then ID. Each ranking is a list of IDs; reject duplicates within a ranking and nonpositive/non-integer c. A document appearing in multiple rankings gets one contribution per list: `1/(c+rank)`, with rank starting at 1. Empty rankings return an empty result. Do not add raw lexical and cosine scores.''','''def student_rrf(rankings,c=60):
    raise NotImplementedError("Fuse rankings using reciprocal ranks")''','''def student_rrf(rankings,c=60):
    if type(c) is not int or c<1: raise ValueError("invalid constant")
    scores={}
    for ranking in rankings:
        if len(ranking)!=len(set(ranking)): raise ValueError("duplicate ranking ID")
        for rank,key in enumerate(ranking,1): scores[key]=scores.get(key,0)+1/(c+rank)
    return sorted(scores.items(),key=lambda pair:(-pair[1],pair[0]))''','''assert student_rrf([])==[]
assert student_rrf([["a"],["b","a"]])[0][0]=="a"
assert np.isclose(dict(student_rrf([["a"],["b","a"]]))["a"],1/61+1/62)
for rankings,c in [([["a","a"]],60),([],0),([],True)]:
    try: student_rrf(rankings,c)
    except ValueError: pass
    else: raise AssertionError("invalid fusion input accepted")''')
cells+=task('''### 3. TODO: wire a real hybrid retrieval pipeline (40 points)
Implement `student_hybrid(conn,tenant,query,k=5)` using dense and lexical candidate queries (ten each), your rank fusion, and `models.rerank`. Preserve complete records and IDs; select at most twenty fused candidates before reranking. Reject k outside 1–20. There must be no score-based assumption that all queries have an answer.''','''def student_hybrid(conn,tenant,query,k=5):
    raise NotImplementedError("Retrieve, fuse, preserve records, and rerank")''','''def student_hybrid(conn,tenant,query,k=5):
    if type(k) is not int or not 1<=k<=20: raise ValueError("invalid k")
    d=db.search(conn,tenant,models.embed([query])[0],query,10,"dense")
    l=db.search(conn,tenant,None,query,10,"lexical")
    records={r["chunk_id"]:r for r in d+l}
    fused=student_rrf([[r["chunk_id"] for r in d],[r["chunk_id"] for r in l]])
    return models.rerank(query,[records[key] for key,score in fused[:20]],k)''','''with db.connect() as conn:
    assert student_hybrid(conn,"missing","camera",3)==[]
    rows=student_hybrid(conn,"alpha","E-204",3)
assert 1<=len(rows)<=3 and len({r["chunk_id"] for r in rows})==len(rows)
assert all("BETA-ONLY-MARKER" not in r["text"] for r in rows)
assert all(np.isfinite(r["rerank_score"]) for r in rows)
print("Hybrid retrieval exercised with real models and PostgreSQL")''')
cells += [md('''### 4. Evaluate methods without assuming a winner
The evaluation unit is a document. Repeated chunks from the same document are deduplicated before computing metrics. Queries with no relevant document have null relevance metrics, not a fabricated perfect score. Evaluate abstention separately. The visible development corpus is small; its means do not establish general superiority.'''),code('''from raglab.evaluate import evaluate
import matplotlib.pyplot as plt
report=evaluate("dev")
methods=["lexical","dense","hybrid","hybrid+rerank"]
means=[np.mean([r["recall"] for r in report["rows"] if r["mode"]==method and r["recall"] is not None]) for method in methods]
plt.figure(figsize=(7,3))
plt.bar(methods,means,color=["#4477AA","#66CCEE","#228833","#AA3377"])
plt.ylim(0,1.08);plt.ylabel("Mean document Recall@5")
plt.title("Five development questions · invented English policy corpus")
plt.xticks(rotation=15);plt.tight_layout();plt.show()
print([{k:r[k] for k in ("question","mode","recall","mrr","ndcg")} for r in report["rows"][:4]])'''),md('''## Checks and submission
Produce a query-level table and a summary of Recall@5, MRR@5, nDCG@5, and observed time. Fix the dataset, model revisions, candidate count, and final k across comparisons; record changes rather than comparing incompatible configurations. Explain any tie, degradation, or missing relevant candidate. A reranker cannot recover a document absent from its candidates.

Add a no-answer query, an exact identifier, a paraphrase, and a conflicting policy case. Add a BM25 baseline using the supplied `rank-bm25` package if you want to compare lexical scoring methods; label it distinctly from PostgreSQL full-text ranking.

Rubric: fusion 30, integrated search 40, evaluation 20, failure analysis 10.

## Next Steps
Lab 15 exposes this retrieval pipeline as an HTTP service. Keep corpus text out of logs unless it is explicitly needed and appropriate.

References checked 2026-10-07: [PostgreSQL text-search ranking](https://www.postgresql.org/docs/current/textsearch-controls.html), [pgvector hybrid search](https://github.com/pgvector/pgvector#hybrid-search), [cross-encoder usage](https://www.sbert.net/docs/cross_encoder/usage/usage.html), [reranker model card](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2).''')]
save('14_hybrid_search_reranking',cells)

cells=start('Lab 15 · FastAPI retrieval service','Build and test a typed HTTP endpoint backed by actual pgvector retrieval. Practice request validation, dependency injection, API-key tenant mapping, lifespan resource management, connection pools, and failure handling. Prerequisites: Labs 12–14 and HTTP basics. Plan 120 minutes: 20 service exploration, 45 implementation, 30 tests, 25 server exercise/report.\n\nThis is a local teaching service. Example API keys are public, not production credentials. There is no database row-level-security policy in this starter; the application must include the tenant filter on every retrieval path.')
cells += [md('''## Steps
### 1. Start and inspect the reference application
Read `raglab/service.py`. Its lifespan loads models and opens a database pool once. Requests run synchronous inference/database work in FastAPI's synchronous endpoint execution path. A two-slot semaphore rejects excess concurrent work; SQL has a statement timeout. This does not implement an end-to-end CPU inference deadline.

`TestClient` below executes the real ASGI application and database calls in-process. It does not establish that a network server is listening. Use the terminal exercise later for that.'''),code('''from fastapi.testclient import TestClient
from raglab.service import create_app,SearchRequest,SearchResponse,Hit
app=create_app({"student-alpha":"alpha","student-beta":"beta"})
headers={"X-API-Key":"student-alpha"}
with TestClient(app) as client:
    assert client.get("/health").status_code==200
    response=client.post("/search",headers=headers,json={"query":"camera loans","k":3,"rerank":True})
    assert response.status_code==200,response.text
    print(response.json())
    assert client.post("/search",json={"query":"camera"}).status_code==401
    assert client.post("/search",headers=headers,json={"query":"   "}).status_code==422
    assert client.post("/search",headers=headers,json={"query":"camera","tenant":"beta"}).status_code==422''')]
cells+=task('''### 2. TODO: add your own FastAPI route (40 points)
Implement `add_student_route(app)` to register POST `/student-search` with request type `SearchRequest` and response type `SearchResponse`. Obtain the tenant through `Depends(app.state.tenant_dependency)`; use the request's application pool and the shared `retrieve` function. Do not accept a tenant in the request body or query parameters. Add the route before starting `TestClient`. This first route intentionally lacks the reference route's load/error policy; add those in your submission after making the data path work.''','''def add_student_route(app):
    raise NotImplementedError("Register a typed route and inject the authenticated tenant")''','''def add_student_route(app):
    from fastapi import Request,Depends
    from raglab.retrieval import retrieve
    @app.post("/student-search",response_model=SearchResponse)
    def student_route(body:SearchRequest,request:Request,owner:str=Depends(app.state.tenant_dependency)):
        with request.app.state.pool.connection() as conn:
            rows=retrieve(conn,owner,body.query,body.k,body.mode,body.rerank)
        return SearchResponse(hits=[Hit(**{key:row[key] for key in Hit.model_fields}) for row in rows],mode=body.mode,reranked=body.rerank)''','''student_app=create_app({"student-alpha":"alpha","student-beta":"beta"})
add_student_route(student_app)
with TestClient(student_app) as client:
    assert client.post("/student-search",json={"query":"camera"}).status_code==401
    response=client.post("/student-search",headers=headers,json={"query":"BETA-ONLY-MARKER camera","k":20})
    assert response.status_code==200,response.text
    assert all("BETA-ONLY-MARKER" not in h["text"] for h in response.json()["hits"])
    assert client.post("/student-search",headers=headers,json={"query":"camera","k":True}).status_code==422
    assert "/student-search" in client.get("/openapi.json").json()["paths"]
print("Student route exercised against pgvector")''')
cells+=task('''### 3. TODO: write an API contract test (30 points)
Implement `assert_contract(client,path)` using real HTTP test-client calls. Verify missing/invalid keys return 401; a blank query, k=0, and an extra tenant field return 422; a valid alpha query returns 200 with only `hits`, `mode`, `reranked`; no returned text contains the beta marker. The function should raise assertions on a regression and return nothing.''','''def assert_contract(client,path):
    raise NotImplementedError("Test authentication, validation, response shape, and isolation")''','''def assert_contract(client,path):
    assert client.post(path,json={"query":"camera"}).status_code==401
    assert client.post(path,headers={"X-API-Key":"wrong"},json={"query":"camera"}).status_code==401
    for body in ({"query":" "},{"query":"camera","k":0},{"query":"camera","tenant":"beta"}):
        assert client.post(path,headers=headers,json=body).status_code==422
    result=client.post(path,headers=headers,json={"query":"camera","k":20})
    assert result.status_code==200
    data=result.json()
    assert set(data)=={"hits","mode","reranked"}
    assert all("BETA-ONLY-MARKER" not in hit["text"] for hit in data["hits"])''','''with TestClient(student_app) as client:
    assert_contract(client,"/student-search")
    assert_contract(client,"/search")
print("Both endpoint contracts checked")''')
cells += [md('''### 4. Run a real server from a terminal
From `labs/rag`, activate the environment and run:

```bash
export RAG_API_KEYS='{"student-alpha":"alpha","student-beta":"beta"}'
uvicorn raglab.service:create_app --factory --host 127.0.0.1 --port 58000
```

Open `http://127.0.0.1:58000/docs`, inspect the generated request schema, and call `/search`. In a second terminal:

```bash
curl -sS http://127.0.0.1:58000/search -H 'Content-Type: application/json' -H 'X-API-Key: student-alpha' -d '{"query":"E-204","k":3,"rerank":true}'
```

Stop the server with Ctrl-C. Do not expose this demonstration service publicly. To serve the student route, put it in a Python module and register it in your app factory; a function defined only inside the notebook does not modify a separate Uvicorn process.

## Checks and submission
Submit your app module and tests, plus the notebook as a client/report. Add the reference route's bounded-concurrency and sanitized 503 behavior to your own route. Test pool exhaustion/database failure by dependency injection; test a genuinely stopped database only in the isolated Compose project and restart it afterward. Explain the difference between a 401, 422, and 503. Do not log request keys or raw retrieved passages.

Rubric: route 40, contract tests 30, real HTTP demonstration 15, failure policy 15. Existing passing tests are not proof that every future SQL path preserves isolation.

## Next Steps
Lab 16 combines updates, service operation, retrieval evaluation, and optional grounded generation.

References checked 2026-10-07: [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/), [lifespan](https://fastapi.tiangolo.com/advanced/events/), [dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/), [psycopg connection pools](https://www.psycopg.org/psycopg3/docs/advanced/pool.html).''')]
save('15_fastapi_rag_service',cells)

cells=start('Lab 16 · Integrated pgvector RAG application','Operate the stack as one application: ingest an update, query it through FastAPI, verify tenant isolation, collect an evaluation report, and diagnose a controlled failure. Prerequisites: Labs 12–15. Plan two 90-minute sessions or a capstone assignment; full deployment and evaluation are not compressed into one short tutorial.\n\npgvector remains the required backend. The earlier optional Milvus/Pinecone portability proposal is retained as an extension at the end; the core practical work goes deeper into the selected database and FastAPI stack.')
cells += [md('''## Steps
### 1. Verify a database update through the API
A database write is not enough: verify the service returns the current version's evidence and that old chunks were removed. Use a dedicated exercise tenant so the evaluation corpus is unchanged. Each change is a transaction; embedding computation happens before the transaction begins.'''),code('''from raglab.service import create_app
from fastapi.testclient import TestClient
record={"tenant":"exercise16","doc_id":"policy","version":1,"title":"Demonstration policy","body":"The capstone camera loan lasts three days.","source":"course://exercise16/policy"}
def store(record):
    chunks=chunk_documents([record])
    db.replace_document(record,chunks,models.embed([c["text"] for c in chunks]))
try:
    store(record)
    app=create_app({"capstone-key":"exercise16"})
    with TestClient(app) as client:
        payload={"query":"camera loan","mode":"lexical","k":5}
        first=client.post("/search",headers={"X-API-Key":"capstone-key"},json=payload).json()
        store(dict(record,version=2,body="The capstone camera loan lasts six days."))
        second=client.post("/search",headers={"X-API-Key":"capstone-key"},json=payload).json()
        assert any("six days" in h["text"] for h in second["hits"])
        assert not any("three days" in h["text"] for h in second["hits"])
        assert {h["chunk_id"] for h in first["hits"]}.isdisjoint(h["chunk_id"] for h in second["hits"])
        print({"before":first["hits"],"after":second["hits"]})
finally:
    db.delete_document("exercise16","policy")''')]
cells+=task('''### 2. TODO: implement a deployment smoke test (30 points)
Implement `smoke(client)` against the reference FastAPI app. Verify health, authenticated alpha retrieval, beta retrieval of its marker, rejection of a missing key, and alpha isolation. Return a dictionary of named boolean checks only after asserting all are true. Use test-client responses now; repeat the same checks against an `httpx.Client` connected to the real server before submission.''','''def smoke(client):
    raise NotImplementedError("Probe both tenants, authentication, and readiness")''','''def smoke(client):
    body={"query":"BETA-ONLY-MARKER camera","k":20}
    a=client.post("/search",headers={"X-API-Key":"student-alpha"},json=body)
    b=client.post("/search",headers={"X-API-Key":"student-beta"},json=body)
    checks={"health":client.get("/health").status_code==200,
        "alpha_search":a.status_code==200,
        "beta_search":b.status_code==200 and any("BETA-ONLY-MARKER" in h["text"] for h in b.json()["hits"]),
        "isolation":a.status_code==200 and all("BETA-ONLY-MARKER" not in h["text"] for h in a.json()["hits"]),
        "auth":client.post("/search",json=body).status_code==401}
    assert all(checks.values()),checks
    return checks''','''with TestClient(create_app({"student-alpha":"alpha","student-beta":"beta"})) as client:
    print(smoke(client))''')
cells+=task('''### 3. TODO: summarize evaluation without hiding missing labels (30 points)
Implement `summarize(rows)` for records from `raglab.evaluate.evaluate`. Group by method, report the number of query runs, number with non-null relevance metrics, mean Recall@5 over labeled queries, and median observed milliseconds over all runs. Empty input returns `{}`. Do not turn null recall into zero or include it in the relevance denominator. Reject negative/nonfinite time or recall outside [0,1].''','''def summarize(rows):
    raise NotImplementedError("Aggregate with explicit denominators")''','''def summarize(rows):
    groups={}
    for row in rows:
        t=row["milliseconds"]; r=row["recall"]
        if not np.isfinite(t) or t<0 or (r is not None and (not np.isfinite(r) or not 0<=r<=1)):
            raise ValueError("invalid measurement")
        groups.setdefault(row["mode"],[]).append(row)
    out={}
    for mode,group in groups.items():
        values=[r["recall"] for r in group if r["recall"] is not None]
        out[mode]={"queries":len(group),"labeled":len(values),"mean_recall":float(np.mean(values)) if values else None,
                   "median_ms":float(np.median([r["milliseconds"] for r in group]))}
    return out''','''assert summarize([])=={}
example=[{"mode":"dense","milliseconds":2,"recall":1.0},{"mode":"dense","milliseconds":4,"recall":None}]
assert summarize(example)["dense"]=={"queries":2,"labeled":1,"mean_recall":1.0,"median_ms":3.0}
for bad in (-1,float("nan"),float("inf")):
    try: summarize([{"mode":"x","milliseconds":bad,"recall":None}])
    except ValueError: pass
    else: raise AssertionError("invalid timing accepted")''')
cells += [md('''### 4. Optional Gemini generation from service evidence
This completes a retrieval→generation path when you have a Gemini account. Retrieval practice and grading do not require a paid API. Set `GEMINI_API_KEY` and `GEMINI_MODEL` outside the notebook, then deliberately enable `RUN_GENERATION`. The helper performs one model request with a timeout and no automatic retry beyond that attempt. Citation membership is checked; entailment and answer completeness still require separate assessment.'''),code('''if RUN_GENERATION:
    from raglab.generation import grounded_answer
    with TestClient(create_app({"student-alpha":"alpha"})) as client:
        query="How long can I borrow a camera?"
        response=client.post("/search",headers={"X-API-Key":"student-alpha"},json={"query":query,"k":5,"rerank":True})
        response.raise_for_status()
        answer=grounded_answer(query,response.json()["hits"])
        print(answer.model_dump())
else:
    print("Gemini generation not executed; no generated-answer quality claim.")'''),md('''### 5. Package and operate the stack
From `labs/rag`, after preparing model snapshots and seeding PostgreSQL:

```bash
docker compose -f compose.yaml -f compose.api.yaml up --build -d --wait
curl -sS http://127.0.0.1:58000/health
```

The API image mounts the already-downloaded model snapshots read-only. Record the built image ID, model revisions, package lock, and database version. Run the smoke test against `httpx.Client(base_url="http://127.0.0.1:58000")`. Stop only this stack with `docker compose -f compose.yaml -f compose.api.yaml down`; retain the database volume unless you intentionally want to erase the teaching data.

Freeze settings before running `python -m raglab.evaluate --split test --output student-results/final.json`. The test questions are public; use them for disciplined practice, not as a claim of blind evaluation. Latency in the evaluation report includes cold-start effects and is not a concurrent-load benchmark.

## Checks and submission
Submit app code, ten or more meaningful tests, one query-level evaluation JSON, a short operating guide, and a failure report. Demonstrate stale-update rejection, unknown tenant, unauthorized request, empty lexical results, and a simulated database timeout. Explain which failures return 503 and which should fail startup. Include a trace from source document to retrieved chunk to cited evidence.

Rubric: smoke checks 30, evaluation summary 30, deployment and failure tests 25, reproducibility and interpretation 15. For generated answers, assess evidence support and abstention separately from retrieval relevance. Raw neural scores are not universal abstention thresholds.

## Next Steps · Optional backend portability
Keep the same query corpus, embeddings, tenant policy, and evaluation contract. Implement one alternative adapter using Milvus or Pinecone and compare filtered retrieval, ingestion/update semantics, returned IDs, setup requirements, and measured cost/latency under declared conditions. Do not replace the required pgvector implementation. A managed API and a local container are not directly comparable performance environments.

References checked 2026-10-07: [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/), [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/), [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output), [Milvus hybrid search](https://milvus.io/docs/multi-vector-search.md), [Pinecone hybrid search](https://docs.pinecone.io/guides/search/hybrid-search).''')]
save('16_pgvector_fastapi_capstone',cells)
