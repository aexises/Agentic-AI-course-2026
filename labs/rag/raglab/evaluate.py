"""One recorded evaluation run; no tuning on the public assessment split."""
import argparse
import hashlib
import json
import platform
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
import numpy as np
from .config import ROOT,model_dir
from . import db
from .retrieval import retrieve,document_metrics

def evaluate(split='dev',output=None):
    if split not in ('dev','test'): raise ValueError('split must be dev or test')
    questions=json.loads((ROOT/'data/questions.json').read_text())
    rows=[]
    with db.connect() as conn:
        for question in (q for q in questions if q['split']==split):
            for mode,rerank in [('lexical',False),('dense',False),('hybrid',False),('hybrid',True)]:
                start=time.perf_counter()
                hits=retrieve(conn,question['tenant'],question['query'],5,mode,rerank)
                rows.append({'question':question['id'],'mode':mode+('+rerank' if rerank else ''),
                    'milliseconds':1000*(time.perf_counter()-start),
                    'retrieved_documents':list(dict.fromkeys(h['doc_id'] for h in hits)),
                    **document_metrics(hits,set(question['relevant']))})
    report={'utc_time':datetime.now(timezone.utc).isoformat(),'split':split,'python':platform.python_version(),
            'packages':{p:version(p) for p in ('llama-index-core','pgvector','psycopg','sentence-transformers','fastapi')},
            'corpus_sha256':hashlib.sha256((ROOT/'data/documents.json').read_bytes()).hexdigest(),
            'models':json.loads((model_dir()/'manifest.json').read_text()),'rows':rows,
            'limitations':'Small invented English corpus; observed timings include cold starts and are not service-load benchmarks. Public test questions are not secret assessment data. No relevant-document queries have null relevance metrics.'}
    if output:
        path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(report,indent=2)+'\n')
    return report

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--split',choices=['dev','test'],default='dev');parser.add_argument('--output',required=True)
    args=parser.parse_args();report=evaluate(args.split,args.output)
    print(f"Recorded {len(report['rows'])} query/method runs to {args.output}")

if __name__=='__main__':main()
