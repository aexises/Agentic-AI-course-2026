import math
import numpy as np
import pytest
from pydantic import ValidationError
from raglab import db,models
from raglab.ingestion import corpus,chunk_documents,make_pipeline,validate_documents
from raglab.retrieval import rrf,document_metrics
from raglab.service import SearchRequest,api_keys

@pytest.mark.parametrize('bad',[None,{},[{}]])
def test_document_shapes(bad):
    with pytest.raises(ValueError):validate_documents(bad)

def test_documents_duplicate_blank_and_boolean_version():
    r=corpus()[0]
    for records in ([r,r],[dict(r,body=' ')],[dict(r,version=True)]):
        with pytest.raises(ValueError):validate_documents(records)
    assert validate_documents([])==[]

def test_chunk_identity_and_provenance():
    r=corpus()[0]
    a=chunk_documents([r],make_pipeline(64,8))
    b=chunk_documents([r],make_pipeline(64,8))
    assert a==b
    assert a and all(c['source']==r['source'] and c['tenant']==r['tenant'] for c in a)
    c=chunk_documents([dict(r,version=2)],make_pipeline(64,8))
    assert {row['chunk_id'] for row in a}.isdisjoint(row['chunk_id'] for row in c)
    assert chunk_documents([])==[]

@pytest.mark.parametrize('size,overlap',[(True,0),(31,0),(257,0),(64,64),(64,-1)])
def test_invalid_splitter(size,overlap):
    with pytest.raises(ValueError):make_pipeline(size,overlap)

@pytest.mark.parametrize('value',[np.zeros(384),np.ones(383),np.full(384,np.nan),np.full(384,np.inf),[[1]*384]])
def test_invalid_vectors(value):
    with pytest.raises(ValueError):db.vector(value)

def test_valid_vector_and_empty_embedding_batch():
    assert db.vector(np.ones(384)).shape==(384,)
    assert models.embed([]).shape==(0,384)
    with pytest.raises(ValueError):models.embed([' '])

def test_rrf_expected_value_tie_and_duplicates():
    a={'chunk_id':'a','doc_id':'a','text':'a'};b={'chunk_id':'b','doc_id':'b','text':'b'}
    rows=rrf([[a],[b,a]])
    assert rows[0]['chunk_id']=='a'
    assert math.isclose(rows[0]['fusion_score'],1/61+1/62)
    assert [r['chunk_id'] for r in rrf([[b],[a]])]==['a','b']
    assert rrf([])==[]
    with pytest.raises(ValueError):rrf([[a,a]])
    with pytest.raises(ValueError):rrf([[a],[dict(a,text='changed')]])

def test_metrics_document_dedup_and_no_answer():
    rows=[{'doc_id':'a'},{'doc_id':'a'},{'doc_id':'b'}]
    assert document_metrics(rows,{'a','b'},2)=={'recall':1.,'mrr':1.,'ndcg':1.}
    assert document_metrics(rows,set())=={'recall':None,'mrr':None,'ndcg':None}
    assert document_metrics([],{'a'})=={'recall':0.,'mrr':0.,'ndcg':0.}

@pytest.mark.parametrize('body',[{'query':''},{'query':' '},{'query':'x','k':True},{'query':'x','k':0},{'query':'x','k':21},{'query':'x','tenant':'beta'},{'query':'x','mode':'unknown'},{'query':'x'*1001}])
def test_request_validation(body):
    with pytest.raises(ValidationError):SearchRequest(**body)

def test_key_configuration_fails_closed(monkeypatch):
    monkeypatch.delenv('RAG_API_KEYS',raising=False)
    with pytest.raises(RuntimeError):api_keys()
    for raw in ('{}','[]','{"x":""}'):
        monkeypatch.setenv('RAG_API_KEYS',raw)
        with pytest.raises(ValueError):api_keys()
