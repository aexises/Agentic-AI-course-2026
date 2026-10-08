"""Parameterized SQL, tenant filters, atomic document replacement, and pgvector."""
import numpy as np
import psycopg
from psycopg.rows import dict_row
from pgvector.psycopg import register_vector
from .config import database_url, DIMENSION
from .ingestion import validate_documents

DDL='''
CREATE EXTENSION IF NOT EXISTS vector;
CREATE SCHEMA IF NOT EXISTS rag_course;
CREATE TABLE IF NOT EXISTS rag_course.documents (
 tenant text NOT NULL, doc_id text NOT NULL, version integer NOT NULL CHECK(version>0),
 title text NOT NULL, body text NOT NULL, source text NOT NULL,
 PRIMARY KEY(tenant,doc_id)
);
CREATE TABLE IF NOT EXISTS rag_course.chunks (
 chunk_id text PRIMARY KEY, tenant text NOT NULL, doc_id text NOT NULL,
 ordinal integer NOT NULL CHECK(ordinal>=0), text text NOT NULL,
 embedding vector(384) NOT NULL,
 lexemes tsvector GENERATED ALWAYS AS (to_tsvector('english',text)) STORED,
 FOREIGN KEY(tenant,doc_id) REFERENCES rag_course.documents(tenant,doc_id) ON DELETE CASCADE,
 UNIQUE(tenant,doc_id,ordinal)
);
CREATE INDEX IF NOT EXISTS chunks_tenant ON rag_course.chunks(tenant);
CREATE INDEX IF NOT EXISTS chunks_lexemes ON rag_course.chunks USING gin(lexemes);
'''

def connect():
    conn=psycopg.connect(database_url(),row_factory=dict_row,connect_timeout=5)
    try: register_vector(conn)
    except Exception:
        conn.close(); raise
    return conn

def initialize():
    with psycopg.connect(database_url(),connect_timeout=5) as conn:
        conn.execute(DDL)

def vector(value):
    a=np.asarray(value,dtype=np.float32)
    if a.shape!=(DIMENSION,) or not np.isfinite(a).all() or np.linalg.norm(a.astype(np.float64))==0:
        raise ValueError('expected a finite nonzero 384-dimensional vector')
    return a

def replace_document(record,chunks,embeddings):
    validate_documents([record])
    if not chunks or len(chunks)!=len(embeddings): raise ValueError('nonempty aligned chunks and embeddings required')
    if any(c['tenant']!=record['tenant'] or c['doc_id']!=record['doc_id'] or c['version']!=record['version'] for c in chunks):
        raise ValueError('chunk ownership/version mismatch')
    vectors=[vector(v) for v in embeddings]
    # Row lock serializes writers of the same document. A lower version cannot overwrite a newer one.
    with connect() as conn:
        conn.execute('''INSERT INTO rag_course.documents(tenant,doc_id,version,title,body,source)
          VALUES (%(tenant)s,%(doc_id)s,%(version)s,%(title)s,%(body)s,%(source)s)
          ON CONFLICT (tenant,doc_id) DO NOTHING''',record)
        old=conn.execute('SELECT version,title,body,source FROM rag_course.documents WHERE tenant=%s AND doc_id=%s FOR UPDATE',(record['tenant'],record['doc_id'])).fetchone()
        if old['version']>record['version']: raise ValueError('stale document version')
        if old['version']==record['version'] and any(old[key]!=record[key] for key in ('title','body','source')):
            raise ValueError('changed content requires a newer version')
        conn.execute('''UPDATE rag_course.documents SET version=%(version)s,title=%(title)s,body=%(body)s,source=%(source)s
           WHERE tenant=%(tenant)s AND doc_id=%(doc_id)s''',record)
        conn.execute('DELETE FROM rag_course.chunks WHERE tenant=%s AND doc_id=%s',(record['tenant'],record['doc_id']))
        with conn.cursor() as cur:
            cur.executemany('''INSERT INTO rag_course.chunks(chunk_id,tenant,doc_id,ordinal,text,embedding)
              VALUES (%s,%s,%s,%s,%s,%s)''',[(c['chunk_id'],c['tenant'],c['doc_id'],c['ordinal'],c['text'],v) for c,v in zip(chunks,vectors)])

def delete_document(tenant,doc_id):
    with connect() as conn:
        return conn.execute('DELETE FROM rag_course.documents WHERE tenant=%s AND doc_id=%s',(tenant,doc_id)).rowcount

def search(conn,tenant,query_vector,query,k=10,mode='dense',exact=False):
    if not isinstance(tenant,str) or not tenant.strip() or not isinstance(query,str) or not query.strip():
        raise ValueError('tenant and query required')
    if type(k) is not int or not 1<=k<=50 or mode not in ('dense','lexical'): raise ValueError('invalid search options')
    with conn.transaction():
        conn.execute("SET LOCAL statement_timeout='3000ms'")
        if exact:
            conn.execute('SET LOCAL enable_indexscan=off')
            conn.execute('SET LOCAL enable_bitmapscan=off')
        if mode=='dense':
            rows=conn.execute('''SELECT chunk_id,doc_id,text,embedding <=> %s AS distance
                FROM rag_course.chunks WHERE tenant=%s ORDER BY embedding <=> %s LIMIT %s''',
                (vector(query_vector),tenant,vector(query_vector),k)).fetchall()
        else:
            rows=conn.execute('''SELECT chunk_id,doc_id,text,ts_rank_cd(lexemes,websearch_to_tsquery('english',%s)) AS lexical_score
                FROM rag_course.chunks WHERE tenant=%s AND lexemes @@ websearch_to_tsquery('english',%s)
                ORDER BY lexical_score DESC,chunk_id LIMIT %s''',(query,tenant,query,k)).fetchall()
    return rows
