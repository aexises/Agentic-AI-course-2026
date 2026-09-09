from pathlib import Path
import nbformat as nb
root=Path(__file__).resolve().parents[1]
source=(root/'labs/reference_support.py').read_text()
md=nb.v4.new_markdown_cell; code=nb.v4.new_code_cell
setup=md('''## Setup
These corrected foundation notebooks retain the manual-loop and corrective-retrieval learning goals of AAI[sum26] Labs 3–4. They are course-local replacements, with a smaller offline dependency path and source-preserving records. The original project remains the audit snapshot.

Use the course lab environment. Default runs make no API requests. All example facts are synthetic. These are worked foundation examples; Labs 5–8 contain the assessed implementation exercises.''')

def write(name,cells):
 n=nb.v4.new_notebook(cells=cells,metadata={'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'},'language_info':{'name':'python'}})
 nb.validate(n);nb.write(n,root/'labs'/name)

write('03_react_tools_repaired.ipynb',[
md('# Lab 3 · Repaired manual ReAct foundation\n\n## Goal\nTrace a bounded model/tool exchange and test dispatch independently of a provider.'),setup,code(source),
md('## Steps\nThe fake model asserts that the harness passes a stop sequence and then sees the real observation. A stop sequence is a format aid, not an authorization mechanism.'),
code('''calls=[]
def fake(messages,stop):
    assert stop==["Observation:"]
    calls.append(messages[-1]["content"])
    if len(calls)==1:return "Action: calculator[2*21]"
    assert messages[-1]["content"]=="Observation: 42"
    return "Final Answer: 42"
result=run("Calculate 2*21",fake)
assert result.answer=="42"
assert run_tool("calculator","",{"calculator":(lambda _:"replacement","")})=="replacement"
print(result)'''),
md('## Checks\nTest syntax, resource bounds, parse failures, unknown tools, and step exhaustion.'),
code('''assert calculator("2*(3+4)")=="14"
for bad in ["2**1000000000","True","__import__('os')", "1/0", "1e999", "9"*257]:
    assert calculator(bad).startswith("calculator error")
assert parse("Action: missing[x]\\nFinal Answer: fake")[0]=="error"
assert run_tool("missing","x")=="tool error: unknown tool"
assert run("task",lambda *a,**kw:"bad").stopped_reason=="parse_error"
assert run("task",lambda *a,**kw:"Action: word_count[a b]",max_steps=1).stopped_reason=="max_steps"
print("Foundation checks passed")'''),
md('''## Native protocol continuation
Use Lab 5 for the complete Gemini native tool cycle, including matching call IDs, returning results to the model, and separate round/call budgets. This replaces the reference example that stopped after printing tool outputs.

## Next Steps
Explain the distinction between protocol errors, tool errors, and model errors. Add a fake model that emits an Observation and show rejection. Then complete Lab 5's native protocol and policy exercises.

[Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) documents the native continuation.''')])
write('04_corrective_rag_repaired.ipynb',[
md('# Lab 4 · Repaired corrective retrieval foundation\n\n## Goal\nPreserve evidence identity through a bounded retrieval, repair, and answer loop.'),setup,code(source),
md('## Steps\nSearch returns records with IDs, URLs, and text. The offline fake uses the documented `raw_content` response field and checks that the API key enters the constructor as `api_key`.'),
code('''class FakeSearch:
    def __init__(self,**kwargs): assert kwargs=={"api_key":"offline-placeholder"}
    def search(self,**kwargs):
        assert kwargs["include_raw_content"] is True
        return {"results":[{"url":"https://example.org/orion","raw_content":"Orion battery lifetime is 8 hours."}]}
records=search_and_scrape("Orion battery", "offline-placeholder", FakeSearch)
assert records[0]["source"]=="https://example.org/orion"
result=corrective_rag("Orion battery",[],
    grader=lambda q,docs:any("8 hours" in d["text"] for d in docs),
    rewriter=lambda q:q,
    searcher=lambda q:records,
    answerer=lambda q,docs:{"text":docs[0]["text"],"citations":[docs[0]["id"]]})
assert result["status"]=="answered" and len(result["trace"])==2
print(result)'''),
md('## Checks\nMalformed or empty search results must not become evidence. Unknown questions must terminate.'),
code('''for response in [None,{}, {"results":None},{"results":[{},None,{"url":"https://example.org","raw_context":"wrong field"}]}]:
    assert normalize_search(response)==[]
assert normalize_search({"results":[{"url":"https://example.org/x","raw_content":"abc"}]*3})==[{"id":"https://example.org/x","source":"https://example.org/x","text":"abc"}]
r=corrective_rag("unknown",[],lambda q,d:False,lambda q:q,lambda q:[],lambda q,d:"bad",max_steps=2)
assert r["status"]=="abstained" and len(r["trace"])==2
print("Foundation checks passed")'''),
md('''## Optional live search adapter
The tested `search_and_scrape` accepts an injected client factory. With Tavily installed and configured, use `TavilyClient` as that factory and read the key from the environment. This notebook does not run that request. Current provider access and billing must be checked separately.

[Official Tavily Python reference](https://docs.tavily.com/sdk/python/reference).

## Next Steps
Complete Lab 6 for explicit LangGraph state and Gemini answer generation. Explain why a rewrite may help, may do nothing, or may worsen retrieval. Citation membership is a provenance check; it does not prove entailment.''')])
print('Built two repaired foundation notebooks')
