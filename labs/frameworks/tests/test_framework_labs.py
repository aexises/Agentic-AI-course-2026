"""Regression checks for actual instructor notebook implementations (offline)."""
import ast
import asyncio
import inspect
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[3]

@pytest.fixture(scope='module')
def notebooks():
    contexts = {}
    for path in sorted((ROOT/'labs/frameworks/instructor').glob('*.ipynb')):
        namespace = {'__name__':'__notebook__'}
        data=json.loads(path.read_text())
        for cell in data['cells']:
            if cell['cell_type'] != 'code':
                continue
            compiled=compile(''.join(cell['source']),str(path),'exec',flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
            result=eval(compiled,namespace)
            if inspect.isawaitable(result):
                asyncio.run(result)
        contexts[path.name[:2]]=namespace
    return contexts


def test_single_and_maximum_workload(notebooks):
    n=notebooks['09']
    for count in (1,8):
        docs=[{'id':str(i),'text':'Approval required.'} for i in range(count)]
        output=n['make_consensus_graph'](n['worker']).invoke({'docs':docs,'findings':[],'summary':[]})
        assert len(output['summary'])==count
        assert all(row['mentions_approval'] for row in output['summary'])


def test_invalid_batch_never_schedules_worker(notebooks):
    n=notebooks['09']; calls=[]
    def record(s):
        calls.append(s)
        return n['worker'](s)
    app=n['make_consensus_graph'](record)
    for docs in ([{'id':str(i),'text':'x'} for i in range(9)], [{'id':'x','text':'x'}]*2, None):
        with pytest.raises(ValueError):
            app.invoke({'docs':docs,'findings':[],'summary':[]})
    assert calls==[]


def test_worker_failure_is_not_silent_success(notebooks):
    n=notebooks['09']
    def broken(s): raise RuntimeError('worker unavailable')
    with pytest.raises(RuntimeError,match='worker unavailable'):
        n['make_consensus_graph'](broken).invoke({'docs':[{'id':'x','text':'x'}],'findings':[],'summary':[]})


def test_merge_is_order_independent(notebooks):
    n=notebooks['09']; rows=[{'id':'b','mentions_approval':False},{'id':'a','mentions_approval':True}]
    assert n['merge_findings'](rows)==n['merge_findings'](rows[::-1]*3)


def test_exact_model_call_budget(notebooks):
    n=notebooks['10']
    from langchain.agents.middleware.model_call_limit import ModelCallLimitExceededError
    class CountingModel(n['ScriptedInventoryModel']):
        calls: int = 0
        def _generate(self,*args,**kwargs):
            self.calls+=1
            return super()._generate(*args,**kwargs)
    for limit in (1,2,5):
        model=CountingModel(repeat=True)
        with pytest.raises(ModelCallLimitExceededError):
            n['bounded_agent'](model,limit).invoke({'messages':[{'role':'user','content':'Check'}]})
        assert model.calls==limit


def test_multi_call_protocol_and_out_of_order_results(notebooks):
    n=notebooks['10']; AI=n['AIMessage']; Tool=n['ToolMessage']
    call=AI(content='',tool_calls=[{'name':'stock','args':{'item':'camera'},'id':key,'type':'tool_call'} for key in ('a','b')])
    result=[Tool(content='2',tool_call_id=key) for key in ('b','a')]
    assert n['audit_trace']([call,*result])=={'calls':2,'results':2}
    with pytest.raises(ValueError): n['audit_trace']([result[0],call,result[1]])


def test_schema_extra_fields_and_currency_boundaries(notebooks):
    n=notebooks['11']; Quote=n['Quote']; ValidationError=n['ValidationError']
    assert Quote(item='x',quantity=5,total_cents=100_000).total_cents==100_000
    for change in ({'total_cents':-1},{'total_cents':100_001},{'total_cents':float('inf')},{'total_cents':True},{'extra':1},{'item':''}):
        with pytest.raises(ValidationError):
            Quote(**({'item':'x','quantity':1,'total_cents':0}|change))


def test_unknown_tool_item_exhausts_retry(notebooks):
    n=notebooks['11']
    def unknown(messages,info):
        return n['ModelResponse'](parts=[n['ToolCallPart']('catalog_price',{'item':'unknown'},tool_call_id='unknown')])
    app=n['make_quote_agent'](n['FunctionModel'](unknown))
    with pytest.raises(n['UnexpectedModelBehavior']):
        asyncio.run(app.run('Quote',deps=n['checked_catalog']({}),usage_limits=n['UsageLimits'](request_limit=3)))


def test_request_limit_stops_tool_round_trip(notebooks):
    n=notebooks['11']
    from pydantic_ai.exceptions import UsageLimitExceeded
    app=n['make_quote_agent'](n['FunctionModel'](n['scripted_quote']))
    with pytest.raises(UsageLimitExceeded):
        asyncio.run(app.run('Quote two cameras',deps=n['catalog'],usage_limits=n['UsageLimits'](request_limit=1)))


def test_legacy_and_framework_runner_scopes_are_disjoint():
    legacy=set((ROOT/'labs').glob('*.ipynb')) | set((ROOT/'labs/instructor').glob('*.ipynb'))
    new=set((ROOT/'labs/frameworks').glob('*.ipynb')) | set((ROOT/'labs/frameworks/instructor').glob('*.ipynb'))
    assert len(new)==6 and len(legacy)==10
    assert not legacy & new
