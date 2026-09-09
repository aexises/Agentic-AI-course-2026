"""Edge tests for notebook solutions and offline protocol integration."""
import ast, asyncio, inspect, json
from pathlib import Path
from types import SimpleNamespace
import pytest

ROOT=Path(__file__).resolve().parents[1]

@pytest.fixture(scope='module')
def namespaces():
    async def load(path):
        ns={'__name__':'__main__'}
        for cell in json.loads(path.read_text())['cells']:
            if cell['cell_type']!='code': continue
            source=''.join(cell['source'])
            if 'workspace.cleanup()' in source: continue
            result=eval(compile(source,str(path),'exec',flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT),ns)
            if inspect.isawaitable(result): await result
        return ns
    spaces={p.name[:2]:asyncio.run(load(p)) for p in sorted((ROOT/'labs'/'instructor').glob('*.ipynb'))}
    yield spaces
    spaces['08']['workspace'].cleanup()

@pytest.mark.parametrize('value',[True,False,float('nan'),float('inf'),-float('inf'),10**1000,'1',None,[]])
def test_numeric_boundary(namespaces,value):
    ns=namespaces['05']
    assert 'error' in ns['arithmetic'](value,1,'add')
    assert 'error' in ns['dispatch']('arithmetic',{'a':value,'b':1,'operation':'add'},{'arithmetic':ns['arithmetic']})

def test_overflow_result(namespaces):
    assert 'error' in namespaces['05']['arithmetic'](1,5e-324,'divide')

def test_unknown_tool_never_executes(namespaces):
    ns=namespaces['05']; called=[]
    assert ns['dispatch']('nope',{}, {'arithmetic':lambda **kw:called.append(1)})=={'error':'unknown_tool'}
    assert called==[]

def test_multiple_calls_and_empty_response(namespaces):
    ns=namespaces['05']; types=ns['types']
    class Multi:
        def __init__(self): self.models=self; self.n=0
        def generate_content(self,**kw):
            self.n+=1
            if self.n==1:
                parts=[types.Part(function_call=types.FunctionCall(name='arithmetic',id=str(i),args={'a':i,'b':1,'operation':'add'})) for i in range(2)]
            else:
                replies=kw['contents'][-1].parts
                assert [p.function_response.id for p in replies]==['0','1']
                assert [p.function_response.response for p in replies]==[{'value':1},{'value':2}]
                parts=[types.Part(text='done')]
            return SimpleNamespace(candidates=[SimpleNamespace(content=types.Content(role='model',parts=parts))])
    assert ns['native_loop'](Multi(),'fixture','task',ns['dispatch'])['answer']=='done'
    r=ns['native_loop'](Multi(),'fixture','task',ns['dispatch'],max_calls=1)
    assert r=={'status':'call_budget','trace':[]}
    empty=SimpleNamespace(models=SimpleNamespace(generate_content=lambda **kw:SimpleNamespace(candidates=[])))
    assert ns['native_loop'](empty,'fixture','task',ns['dispatch'])['status']=='empty_response'

@pytest.mark.parametrize('limit',[0,-1,True,1.5,9])
def test_round_bounds(namespaces,limit):
    with pytest.raises(ValueError): namespaces['05']['native_loop'](None,'fixture','',None,max_rounds=limit)

def test_retrieval_provenance_and_nonmutation(namespaces):
    ns=namespaces['06']; docs=ns['DOCS']
    r=ns['retrieve']('Orion',docs,100)
    assert r[0]['source']=='fixture://guide-1'
    r[0]['text']='changed'
    assert docs[0]['text']!='changed'
    for k in [-1,True,1.5]:
        with pytest.raises(ValueError): ns['retrieve']('',docs,k)

def test_empty_corpus_terminates(namespaces):
    ns=namespaces['06']; graph=ns['build_rag']([],ns['enough'],ns['rewrite'])
    r=graph.invoke(ns['initial']('Orion battery'),{'recursion_limit':10})
    assert r['status']=='abstained' and r['attempts']==2

def test_identifier_check_is_not_entailment(namespaces):
    ns=namespaces['06']
    # Even an unrelated answer can cite a known ID: membership is not semantic verification.
    assert ns['valid_citations'](['guide-1'],ns['DOCS'])
    assert not ns['valid_citations']([{}],ns['DOCS'])

def test_sdk_max_turns(namespaces):
    from agents.exceptions import MaxTurnsExceeded
    ns=namespaces['07']
    with pytest.raises(MaxTurnsExceeded): asyncio.run(ns['Runner'].run(ns['agent'],'Orion',max_turns=1))

@pytest.mark.parametrize('qty',[-100,0,True,False,1.0,'1',None,4,10**1000])
def test_policy_boundary(namespaces,qty):
    ns=namespaces['08']
    assert not ns['authorize']({'action':'reserve','resource':'lab-seat','quantity':qty},True)

def test_pydantic_and_sdk_configuration(namespaces):
    from google import genai
    from google.genai import types
    from agents import Agent, OpenAIChatCompletionsModel
    from openai import AsyncOpenAI
    from pydantic import ValidationError
    # Constructors only: no request, no usable credentials.
    with genai.Client(api_key='offline-placeholder',http_options=types.HttpOptions(timeout=20_000,retry_options=types.HttpRetryOptions(attempts=1))): pass
    async def check():
        async with AsyncOpenAI(api_key='offline-placeholder',base_url='https://generativelanguage.googleapis.com/v1beta/openai/',timeout=20,max_retries=0) as client:
            model=OpenAIChatCompletionsModel(model='fixture',openai_client=client)
            assert Agent(name='test',model=model).model is model
    asyncio.run(check())
    with pytest.raises(ValidationError): namespaces['06']['GroundedAnswer'].model_validate_json('{"answer":"x","citations":"bad"}')

def test_google_wire_roundtrip(namespaces):
    """Actual GenAI serialization over a mocked HTTP transport; never contacts Google."""
    import httpx
    from google import genai
    from google.genai import types
    seen=[]
    def handler(request):
        body=json.loads(request.content); seen.append(body)
        assert body['generationConfig']['maxOutputTokens']==1024
        if len(seen)==1:
            assert body['tools'][0]['functionDeclarations'][0]['name']=='arithmetic'
            part={'functionCall':{'name':'arithmetic','id':'wire-1','args':{'a':20,'b':22,'operation':'add'}}}
        else:
            fr=body['contents'][-1]['parts'][0]['functionResponse']
            assert fr['id']=='wire-1' and fr['response']=={'value':42}
            part={'text':'42'}
        return httpx.Response(200,json={'candidates':[{'content':{'role':'model','parts':[part]},'finishReason':'STOP'}]})
    with genai.Client(api_key='offline-placeholder',http_options=types.HttpOptions(client_args={'transport':httpx.MockTransport(handler)})) as client:
        ns=namespaces['05']
        assert ns['native_loop'](client,'fixture','add',ns['dispatch'])['answer']=='42'
    assert len(seen)==2


def test_agents_gemini_compatibility_wire(namespaces):
    """Actual Agents SDK Chat Completions adapter over a mocked HTTP transport."""
    import httpx2
    from openai import AsyncOpenAI, DefaultAsyncHttpxClient
    from agents import Agent, Runner, OpenAIChatCompletionsModel
    seen=[]
    def handler(request):
        body=json.loads(request.content);seen.append(body)
        assert request.url.host=='generativelanguage.googleapis.com'
        assert request.url.path.endswith('/chat/completions')
        if len(seen)==1:
            message={'role':'assistant','content':None,'tool_calls':[{'id':'wire-call','type':'function','function':{'name':'catalog_hours','arguments':'{"product":"orion"}'}}]}
            finish='tool_calls'
        else:
            tool_messages=[m for m in body['messages'] if m['role']=='tool']
            assert tool_messages[-1]['tool_call_id']=='wire-call' and tool_messages[-1]['content']=='8'
            message={'role':'assistant','content':'8'}; finish='stop'
        return httpx2.Response(200,json={'id':'response','object':'chat.completion','created':0,'model':'fixture',
            'choices':[{'index':0,'message':message,'finish_reason':finish}],
            'usage':{'prompt_tokens':10,'completion_tokens':2,'total_tokens':12}})
    async def run():
        async with AsyncOpenAI(api_key='offline-placeholder',base_url='https://generativelanguage.googleapis.com/v1beta/openai/',
            max_retries=0,http_client=DefaultAsyncHttpxClient(transport=httpx2.MockTransport(handler))) as client:
            agent=Agent(name='test',model=OpenAIChatCompletionsModel(model='fixture',openai_client=client),tools=[namespaces['07']['catalog_hours']])
            result=await Runner.run(agent,'Orion hours?',max_turns=3)
            assert result.final_output=='8' and result.context_wrapper.usage.requests==2
    asyncio.run(run())
    assert len(seen)==2
