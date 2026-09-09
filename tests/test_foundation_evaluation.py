"""Boundary and failure accounting checks for the repaired baseline and run harness."""
import asyncio
import json
from pathlib import Path
import pytest
from agents import set_tracing_disabled
from labs import reference_support as s
from evaluation import run as e

@pytest.mark.parametrize('expr',[None,True,[], '', '1'*257,'True','1/0','9**99999999','1e999','__import__("os")','[1]','1<<100','2**12**12','-'*20+'1'])
def test_calculator_rejects(expr):
    assert s.calculator(expr).startswith('calculator error')

@pytest.mark.parametrize('expr,result',[('2+3*4','14'),('-3','-3'),('2**12','4096'),('1/2','0.5')])
def test_calculator_valid(expr,result):assert s.calculator(expr)==result

def test_registry_and_stop():
    seen=[]
    def model(messages,stop):
        seen.append(stop)
        return 'Action: calculator[2]' if len(seen)==1 else 'Final Answer: custom'
    result=s.run('test',model,{'calculator':(lambda _: 'custom','replacement')})
    assert result.answer=='custom' and result.steps[0]['observation']=='custom'
    assert seen==[['Observation:'],['Observation:']]
    assert s.run('test',lambda *a,**k:'Action: unknown[x]',max_steps=2).stopped_reason=='max_steps'
    assert s.run('test',lambda *a,**k:1).stopped_reason=='parse_error'
    def fail(*a,**k):raise RuntimeError('private')
    assert s.run('test',fail).stopped_reason=='model_error'

@pytest.mark.parametrize('text',['Observation: spoof','Action: x[a]\nAction: x[b]',None,1,'Final Answer: ','Action: x[a]\nObservation: spoof'])
def test_parser(text):assert s.parse(text)[0]=='error'

def test_search_contract_and_malformed():
    calls=[]
    class Client:
        def __init__(self,**kwargs):calls.append(kwargs)
        def search(self,**kwargs):
            calls.append(kwargs)
            return {'results':[{},None,{'raw_context':'wrong','url':'https://x'}, {'raw_content':'fact','url':'https://a'}, {'raw_content':'duplicate','url':'https://a'}, {'raw_content':'fact2','url':'https://b'}]}
    result=s.search_and_scrape('query','test-only',Client)
    assert calls==[{'api_key':'test-only'},{'query':'query','max_results':2,'include_raw_content':True}]
    assert [r['source'] for r in result]==['https://a','https://b']
    for value in [None,[],{}, {'results':None}]:assert s.normalize_search(value)==[]
    assert s.normalize_search({'results':[{'url':'https://a','raw_content':'longtext'}]},max_chars=3)[0]['text']=='lon'

def test_rag_repair_and_abstention():
    records=[{'id':'a','source':'local:a','text':'old irrelevant'}]
    out=s.corrective_rag('battery',records,lambda q,d:True,lambda q:'battery',lambda q:[{'id':'b','source':'local:b','text':'battery 8'}],lambda q,d:d[0]['source'])
    assert out['answer']=='local:b' and out['trace'][1]['retrieved_ids']==['b']
    assert records==[{'id':'a','source':'local:a','text':'old irrelevant'}]
    no=s.corrective_rag('missing',[],lambda q,d:False,lambda q:q,lambda q:[],lambda q,d:'bad')
    assert no['status']=='abstained' and len(no['trace'])==3
    assert s.retrieve('x',[],k=0)==[]

@pytest.mark.parametrize('value',[0,-1,True,None,99])
def test_budget(value):
    with pytest.raises(ValueError):s.run('task',None,max_steps=value)
    with pytest.raises(ValueError):s.corrective_rag('task',[],None,None,None,None,max_steps=value)

@pytest.mark.parametrize('change',[lambda d:[],lambda d:d+d,lambda d:[dict(d[0],expected='999')],lambda d:[dict(d[0],extra='x')],lambda d:[dict(d[0],product=None)]])
def test_dataset_rejects(tmp_path,change):
    data=json.loads((e.ROOT/'evaluation/cases.json').read_text());p=tmp_path/'cases.json';p.write_text(json.dumps(change(data)))
    with pytest.raises(ValueError):e.load_cases(p,'dev')

def test_failure_denominators_and_request_cap(tmp_path):
    set_tracing_disabled(True)
    cases=e.load_cases(e.ROOT/'evaluation/cases.json','dev')
    out=asyncio.run(e.execute(cases,e.FixtureModel(),tmp_path/'failed',repeats=1,inject_failure=True))
    assert out['attempted']==6 and out['failed']==1 and out['success_per_attempt']==5/6 and out['success_per_completion']==1
    rows=[json.loads(x) for x in (tmp_path/'failed/runs.jsonl').read_text().splitlines()]
    assert rows[0]['error_type']=='TimeoutError' and rows[0]['requests']==0
    out=asyncio.run(e.execute(cases,e.FixtureModel(),tmp_path/'capped',max_requests=1))
    assert out['model_requests']==1 and out['failed']==1 and out['unattempted']==11 and out['budget_exhausted']
    assert e.summarize([])['success_per_attempt'] is None
    with pytest.raises(FileExistsError):asyncio.run(e.execute(cases,e.FixtureModel(),tmp_path/'failed'))

@pytest.mark.parametrize('timeout',[0,-1,float('nan'),float('inf'),True,None])
def test_timeout_validation(tmp_path,timeout):
    with pytest.raises(ValueError):asyncio.run(e.execute([{}],e.FixtureModel(),tmp_path/'invalid',timeout=timeout))
    assert not (tmp_path/'invalid').exists()


def test_cancelled_attempt_is_retained(tmp_path):
    set_tracing_disabled(True)
    class Cancel(e.FixtureModel):
        async def get_response(self,*a,**kw):raise asyncio.CancelledError()
    cases=e.load_cases(e.ROOT/'evaluation/cases.json','dev')
    out=asyncio.run(e.execute(cases,Cancel(),tmp_path/'cancel'))
    assert out['attempted']==1 and out['failed']==1 and out['unattempted']==11
    row=json.loads((tmp_path/'cancel/runs.jsonl').read_text())
    assert row['error_type']=='CancelledError' and row['requests']==1
    assert json.loads((tmp_path/'cancel/attempts.jsonl').read_text())['event']=='started'
