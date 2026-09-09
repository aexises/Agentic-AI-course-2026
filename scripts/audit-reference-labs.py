"""Reproduce selected reference defects with isolated local fakes; never call APIs."""
import ast,json,sys,types
from pathlib import Path
reference=Path('/Users/daeron/Documents/Codex/AAI[sum26]')
root=Path(__file__).resolve().parents[1]

def cell(filename,index):
    return ''.join(json.loads((reference/filename).read_text())['cells'][index]['source'])

def function(source,name):
    node=next(n for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==name)
    return ast.Module(body=[node],type_ignores=[])

results=[]
s=cell('Lab3_ReAct_Tools_Colab.ipynb',10)
ns={'TOOLS':{'x':(lambda text:'global','description')}}
exec(compile(function(s,'run_tool'),'reference','exec'),ns)
observed=ns['run_tool']('x','',{'x':(lambda text:'supplied','description')})
assert observed=='global'
results.append({'id':'R1','cell':10,'observed':observed,'expected':'supplied','finding':'run_tool ignores supplied registry after membership check'})
manual=function(cell('Lab3_ReAct_Tools_Colab.ipynb',14),'run_native_manual')
assert sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='generate_content' for n in ast.walk(manual))==1
results.append({'id':'R2','cell':14,'finding':'manual function has one generate_content call; dispatch results are printed, not returned to model','method':'AST plus source inspection'})
seen={}
class FakeTavily:
    def __init__(self,**kwargs): seen.update(kwargs)
    def search(self,**kwargs): return {'results':[{'raw_content':'fixture page'}]}
module=types.ModuleType('tavily');module.TavilyClient=FakeTavily
sys.modules['tavily']=module
ns={'os':types.SimpleNamespace(environ={'TAVILY_API_KEY':'fixture-key'})}
exec(cell('lab4.ipynb',8),ns)
assert ns['search_and_scrape']('fixture')==[] and seen=={'api_base_url':'fixture-key'}
results.append({'id':'R3','cell':8,'finding':'passes API key as api_base_url; raw_content result produces empty list','observed_constructor_keys':list(seen)})
class TypoTavily(FakeTavily):
    def search(self,**kwargs):return {'results':[{'raw_context':'fixture page'}]}
ns['TavilyClient']=TypoTavily
try:ns['search_and_scrape']('fixture')
except AttributeError:pass
else:raise AssertionError('expected string append failure')
results.append({'id':'R4','cell':8,'finding':'if raw_context branch is reached, text becomes a string and append fails'})
run=function(s,'run')
llm_calls=[n for n in ast.walk(run) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='llm']
assert llm_calls and all(not any(k.arg=='stop' for k in n.keywords) for n in llm_calls)
results.append({'id':'R5','cell':10,'finding':'run calls llm(messages) without the stop argument described in the prose','method':'AST plus source inspection'})
assert 'ast.Pow: operator.pow' in cell('Lab3_ReAct_Tools_Colab.ipynb',6)
results.append({'id':'R6','cell':6,'finding':'calculator allows exponentiation without explicit operand/exponent/expression-size limits','method':'source inspection only; no expensive expression executed'})
p=root/'improvements'/'validation'/'reference-audit.json';p.parent.mkdir(exist_ok=True)
p.write_text(json.dumps(results,indent=2)+'\n')
print('Six reference findings checked using source inspection, AST, or local fakes; no API calls')
