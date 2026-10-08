"""Retrieval and evaluation kept separate from generation."""
import math
from . import db, models

def rrf(rankings,constant=60):
    if type(constant) is not int or constant<1: raise ValueError('positive integer constant required')
    scores={}; records={}
    for ranking in rankings:
        seen=set()
        for rank,row in enumerate(ranking,1):
            key=row['chunk_id']
            if key in seen: raise ValueError('duplicate ID within a ranking')
            seen.add(key)
            if key in records and (row['doc_id'],row['text'])!=(records[key]['doc_id'],records[key]['text']):
                raise ValueError('same chunk ID has conflicting content')
            records[key]=row
            scores[key]=scores.get(key,0)+1/(constant+rank)
    return [dict(records[key],fusion_score=scores[key]) for key in sorted(scores,key=lambda key:(-scores[key],key))]

def retrieve(conn,tenant,query,k=5,mode='hybrid',rerank=False):
    if mode not in ('dense','lexical','hybrid'): raise ValueError('invalid retrieval mode')
    if type(k) is not int or not 1<=k<=20: raise ValueError('k must be 1..20')
    n=min(50,max(10,k*3))
    qv=models.embed([query])[0] if mode!='lexical' else None
    dense=db.search(conn,tenant,qv,query,n,'dense') if mode!='lexical' else []
    lexical=db.search(conn,tenant,None,query,n,'lexical') if mode!='dense' else []
    candidates=rrf([dense,lexical]) if mode=='hybrid' else dense if mode=='dense' else lexical
    return models.rerank(query,candidates,k) if rerank else candidates[:k]

def document_metrics(rows,relevant,k=5):
    if type(k) is not int or k<1 or not isinstance(relevant,set): raise ValueError('invalid metric parameters')
    # Retrieval evaluation unit is a document, not repeated chunks from that document.
    docs=list(dict.fromkeys(row['doc_id'] for row in rows))[:k]
    if not relevant:
        return {'recall':None,'mrr':None,'ndcg':None}
    hits=[int(doc in relevant) for doc in docs]
    dcg=sum(hit/math.log2(rank+2) for rank,hit in enumerate(hits))
    ideal=sum(1/math.log2(rank+2) for rank in range(min(k,len(relevant))))
    return {'recall':sum(hits)/len(relevant), 'mrr':next((1/(i+1) for i,h in enumerate(hits) if h),0.0),'ndcg':dcg/ideal}
