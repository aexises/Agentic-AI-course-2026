"""Disposable pgvector index experiment on generated vectors, not semantic quality."""
import time
import numpy as np

def prepare(conn,n=2000,seed=7):
    if type(n) is not int or not 100<=n<=20_000: raise ValueError('n must be 100..20000')
    rng=np.random.default_rng(seed)
    vectors=rng.normal(size=(n,384)).astype(np.float32)
    vectors/=np.linalg.norm(vectors,axis=1,keepdims=True)
    conn.execute('CREATE TEMP TABLE ann_lab (id integer PRIMARY KEY, cohort integer NOT NULL, embedding vector(384) NOT NULL)')
    with conn.cursor() as cur:
        cur.executemany('INSERT INTO ann_lab VALUES (%s,%s,%s)',[(i,i%10,v) for i,v in enumerate(vectors)])
    conn.execute('ANALYZE ann_lab')
    return vectors

def measure(conn,queries,k=10,exact=False,cohort=None):
    results=[]; timings=[]
    with conn.transaction():
        conn.execute("SET LOCAL statement_timeout='10000ms'")
        conn.execute('SET LOCAL enable_seqscan='+('on' if exact else 'off'))
        conn.execute('SET LOCAL enable_indexscan='+('off' if exact else 'on'))
        conn.execute('SET LOCAL enable_bitmapscan=off')
        for query in queries:
            where='' if cohort is None else 'WHERE cohort=%s'
            params=(query,k) if cohort is None else (cohort,query,k)
            sql=f'SELECT id FROM ann_lab {where} ORDER BY embedding <=> %s LIMIT %s'
            start=time.perf_counter()
            rows=conn.execute(sql,params).fetchall()
            timings.append(1000*(time.perf_counter()-start))
            results.append([r['id'] for r in rows])
    return results, timings

def recall(reference,actual):
    if len(reference)!=len(actual) or not reference: raise ValueError('nonempty aligned runs required')
    return float(np.mean([len(set(a)&set(b))/len(set(a)) if a else 1.0 if not b else 0.0 for a,b in zip(reference,actual)]))
