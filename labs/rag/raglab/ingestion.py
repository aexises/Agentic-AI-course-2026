"""LlamaIndex chunking and explicit provenance; PostgreSQL owns persistence."""
import hashlib
import json
from llama_index.core import Document
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from .config import ROOT

REQUIRED={'tenant','doc_id','version','title','body','source'}

def validate_documents(records):
    if not isinstance(records,list): raise ValueError('documents must be a list')
    seen=set()
    for r in records:
        if not isinstance(r,dict) or set(r)!=REQUIRED: raise ValueError('invalid document fields')
        for key in REQUIRED-{'version'}:
            if not isinstance(r[key],str) or not r[key].strip(): raise ValueError('empty document field')
        if type(r['version']) is not int or r['version']<1: raise ValueError('positive version required')
        identity=(r['tenant'],r['doc_id'])
        if identity in seen: raise ValueError('duplicate tenant/document identity')
        seen.add(identity)
    return records

def corpus():
    return validate_documents(json.loads((ROOT/'data/documents.json').read_text()))

def make_pipeline(chunk_size=96, overlap=12):
    if type(chunk_size) is not int or type(overlap) is not int or not 32<=chunk_size<=256 or not 0<=overlap<chunk_size:
        raise ValueError('chunk size 32..256; overlap 0..chunk_size-1')
    return IngestionPipeline(transformations=[SentenceSplitter(chunk_size=chunk_size,chunk_overlap=overlap)])

def chunk_documents(records, pipeline=None):
    records=validate_documents(records)
    pipeline=make_pipeline() if pipeline is None else pipeline
    output=[]
    for r in records:
        metadata={k:r[k] for k in REQUIRED-{'body'}}
        doc=Document(text=r['body'],id_=r['tenant']+':'+r['doc_id'],metadata=metadata,
                     excluded_embed_metadata_keys=list(metadata),excluded_llm_metadata_keys=list(metadata))
        nodes=pipeline.run(documents=[doc],show_progress=False)
        for ordinal,node in enumerate(nodes):
            text=node.get_content()
            digest=hashlib.sha256((r['tenant']+'\0'+r['doc_id']+'\0'+str(r['version'])+'\0'+str(ordinal)+'\0'+text).encode()).hexdigest()
            output.append({**metadata,'ordinal':ordinal,'chunk_id':digest,'text':text})
    return output
