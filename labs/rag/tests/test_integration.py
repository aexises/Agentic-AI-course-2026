"""Requires the real course database and locally downloaded neural models."""
from contextlib import contextmanager
import numpy as np
import psycopg
import pytest
from fastapi.testclient import TestClient
from raglab import db,models
from raglab.ingestion import chunk_documents,corpus
from raglab.seed import seed
from raglab.service import create_app
from raglab.benchmark import prepare,measure,recall

@pytest.fixture(scope='module',autouse=True)
def seeded():
    seed()

@pytest.fixture
def temporary():
    record=dict(corpus()[0],tenant='integration-test',doc_id='temporary',source='course://integration-test/temporary')
    yield record
    db.delete_document(record['tenant'],record['doc_id'])

def store(record):
    chunks=chunk_documents([record]);vectors=models.embed([r['text'] for r in chunks])
    db.replace_document(record,chunks,vectors)
    return chunks,vectors

def test_actual_embedding_and_reranker():
    vectors=models.embed(['Camera loans last three days.','Microphones record sound.'])
    assert vectors.shape==(2,384)
    assert np.allclose(np.linalg.norm(vectors,axis=1),1,atol=1e-5)
    rows=[{'chunk_id':str(i),'doc_id':str(i),'text':text} for i,text in enumerate(['Camera loans last three days.','Microphones record sound.'])]
    result=models.rerank('How long can I borrow a camera?',rows,2)
    assert {r['chunk_id'] for r in result}=={'0','1'}
    assert all(np.isfinite(r['rerank_score']) for r in result)
    assert result[0]['chunk_id']=='0'
    assert models.rerank('camera',[],2)==[]

def test_atomic_replace_replay_stale_and_rollback(temporary):
    chunks,vectors=store(temporary)
    db.replace_document(temporary,chunks,vectors)
    with db.connect() as conn:
        assert conn.execute('SELECT count(*) AS n FROM rag_course.chunks WHERE tenant=%s',(temporary['tenant'],)).fetchone()['n']==len(chunks)
    changed=dict(temporary,version=2,body='The temporary camera loan now lasts four days.')
    newer,new_vectors=store(changed)
    with pytest.raises(ValueError,match='stale'):db.replace_document(temporary,chunks,vectors)
    with pytest.raises(ValueError,match='newer version'):store(dict(changed,body='Conflicting same-version content.'))
    damaged=dict(changed,version=3)
    bad=[dict(newer[0],version=3),dict(newer[0],version=3)]
    with pytest.raises(psycopg.errors.UniqueViolation):
        db.replace_document(damaged,bad,[new_vectors[0],new_vectors[0]])
    with db.connect() as conn:
        row=conn.execute('SELECT version,body FROM rag_course.documents WHERE tenant=%s AND doc_id=%s',(temporary['tenant'],temporary['doc_id'])).fetchone()
        assert row['version']==2 and row['body']==changed['body']
    db.delete_document(temporary['tenant'],temporary['doc_id'])
    with db.connect() as conn:
        assert conn.execute('SELECT count(*) AS n FROM rag_course.chunks WHERE tenant=%s',(temporary['tenant'],)).fetchone()['n']==0

def test_tenant_filter_empty_and_sql_injection():
    vector=models.embed(['camera'])[0]
    with db.connect() as conn:
        for mode in ('dense','lexical'):
            rows=db.search(conn,'alpha',vector,'BETA-ONLY-MARKER camera',20,mode)
            assert all('BETA-ONLY-MARKER' not in r['text'] for r in rows)
            assert db.search(conn,"alpha' OR true --",vector,'camera',20,mode)==[]
        assert db.search(conn,'alpha',None,'zzzznonexistenttoken',20,'lexical')==[]

def test_ann_actual_index_plans():
    with db.connect() as conn:
        vectors=prepare(conn,n=400)
        queries=vectors[::100]
        exact,_=measure(conn,queries,exact=True)
        for name,ddl in [('hnsw','USING hnsw(embedding vector_cosine_ops)'),('ivfflat','USING ivfflat(embedding vector_cosine_ops) WITH (lists=4)')]:
            conn.execute(f'CREATE INDEX ann_{name} ON ann_lab {ddl}')
            conn.execute('SET LOCAL enable_seqscan=off')
            plan=conn.execute('EXPLAIN (FORMAT JSON) SELECT id FROM ann_lab ORDER BY embedding <=> %s LIMIT 10',(queries[0],)).fetchone()
            assert f'ann_{name}' in str(plan)
            actual,times=measure(conn,queries)
            assert 0<=recall(exact,actual)<=1 and all(t>=0 for t in times)
            conn.execute(f'DROP INDEX ann_{name}')

def test_api_real_db_contract_and_busy():
    app=create_app({'a':'alpha','b':'beta'})
    with TestClient(app) as client:
        assert client.get('/health').status_code==200
        assert client.post('/search',json={'query':'camera'}).status_code==401
        assert client.post('/search',headers={'X-API-Key':'wrong'},json={'query':'camera'}).status_code==401
        assert client.post('/search',headers={'X-API-Key':'a'},json={'query':'camera','tenant':'beta'}).status_code==422
        result=client.post('/search',headers={'X-API-Key':'a'},json={'query':'BETA-ONLY-MARKER camera','k':20,'rerank':True})
        assert result.status_code==200,result.text
        assert all('BETA-ONLY-MARKER' not in h['text'] for h in result.json()['hits'])
        assert client.post('/search',headers={'X-API-Key':'b'},json={'query':'BETA-ONLY-MARKER'}).json()['hits']
        app.state.slots.acquire();app.state.slots.acquire()
        try:
            assert client.post('/search',headers={'X-API-Key':'a'},json={'query':'camera'}).status_code==503
        finally:
            app.state.slots.release();app.state.slots.release()

def test_api_database_failure_sanitized(monkeypatch):
    app=create_app({'a':'alpha'})
    with TestClient(app) as client:
        @contextmanager
        def fail():
            raise psycopg.OperationalError('private database credentials')
            yield
        monkeypatch.setattr(app.state.pool,'connection',fail)
        response=client.post('/search',headers={'X-API-Key':'a'},json={'query':'camera'})
        assert response.status_code==503
        assert 'private' not in response.text
        assert client.get('/health').status_code==503
        # The failure path must release both admission slots.
        assert app.state.slots.acquire(blocking=False)
        assert app.state.slots.acquire(blocking=False)
        app.state.slots.release();app.state.slots.release()
