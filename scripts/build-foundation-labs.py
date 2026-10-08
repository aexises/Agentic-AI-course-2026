from pathlib import Path
import ast, copy
import nbformat as nb
root=Path(__file__).resolve().parents[1]
source=(root/'labs/reference_support.py').read_text()
md=nb.v4.new_markdown_cell; code=nb.v4.new_code_cell
setup=md('''## Setup
These corrected foundation notebooks retain the manual-loop and corrective-retrieval learning goals of AAI[sum26] Labs 3–4. They are course-local replacements, with a smaller offline dependency path and source-preserving records. The original project remains the audit snapshot.

Use the course lab environment. Default runs make no API requests. All example facts are synthetic. These are worked foundation examples; Labs 5–8 contain the assessed implementation exercises.''')

def scaffold(name, solution):
 replacements = {
 'run': [
  ('try:reply=llm(messages,stop=["Observation:"])', 'try:\n            raise NotImplementedError("TODO 3.3a: call llm with messages and the stop sequence")'),
  ('observation=run_tool(name,args,tools)', 'raise NotImplementedError("TODO 3.3b: dispatch with the injected registry and save observation")')],
 'retrieve': [('q=set(re.findall(r"\\w+",query.lower()))', 'raise NotImplementedError("TODO 4.1a: tokenize the query into q")'),
              ('return [dict(r) for score,_,r in nlargest(k,scored,key=lambda x:x[:2]) if score>0]', 'raise NotImplementedError("TODO 4.1b: return copied positive-overlap top-k records")')],
 'corrective_rag': [('decision=grader(question,docs)', 'raise NotImplementedError("TODO 4.2a: grade against the ORIGINAL question; save decision")'),
                    ('if not valid_answer(answer,docs):', 'raise NotImplementedError("TODO 4.2b: reject invalid structured answers before the answered return")\n                if False:'),
                    ('additions=searcher(query);validate_records(additions)', 'raise NotImplementedError("TODO 4.2c: search and validate additions before merging")')]
 }
 if name not in replacements:
  return solution.split('\n')[0]+'\n    raise NotImplementedError("Implement '+name+' using the contract above")'
 for old,new in replacements[name]:
  assert old in solution,(name,old)
  solution=solution.replace(old,new)
 return solution

def write(name,cells):
 targets = {'03': ['parse','run_tool','run'], '04': ['retrieve','corrective_rag']}[name[:2]]
 parsed=ast.parse(source)
 functions={n.name:ast.get_source_segment(source,n) for n in parsed.body if isinstance(n,ast.FunctionDef)}
 # Keep only support relevant to this assignment, not the other lab's answers.
 allowed = {'calculator','word_count'} if name.startswith('03') else {'normalize_search','search_and_scrape','validate_records','valid_answer'}
 support=[]
 for node in parsed.body:
  if isinstance(node,(ast.Import,ast.ImportFrom)) or (isinstance(node,ast.FunctionDef) and node.name in allowed) or (name.startswith('03') and isinstance(node,(ast.Assign,ast.ClassDef))):
   support.append(ast.get_source_segment(source,node) if not isinstance(node,ast.ClassDef) else '@dataclass\n'+ast.get_source_segment(source,node))
 for solved in (False, True):
  out=[copy.deepcopy(cells[0]),md("## Setup\nUse the Labs 3–8 environment. Implement the tasks below, set RUN_EXERCISES=True, restart and run all. Default execution does not solve or grade the assignment. All fixtures are invented. Instructor solutions are distributed separately."),code('RUN_EXERCISES = '+str(solved)),md('## Provided support\nThese utilities support the assignment; the agent/retrieval logic is your work.'),code('\n\n'.join(support))]
  for name_ in targets:
   signature=functions[name_].split('\n')[0]
   contract = {
    'parse':'Parse one Action: name[input] or Final Answer: text. Optionally allow a single leading Thought line as an observable protocol label, not a claim about hidden reasoning. Reject fabricated Observation lines, multiple actions, nonstrings, and messages longer than 10,000 characters. Return ("final", text), ("action", name, input), or ("error", None).',
    'run_tool':'Use only the supplied registry. Bound string input at 10,000 characters, reject unknown tools, and return sanitized errors. Never execute a rejected request.',
    'run':'Implement the model/tool loop. Validate a nonempty task of at most 10,000 characters and an integer max_steps in 1..32. Forward the Observation stop sequence, append actual observations to history, retain action traces, and return Result with final_answer, parse_error, model_error, or max_steps.',
    'retrieve':'Return up to k copied records ranked by overlap of lowercase word tokens. Exclude zero-overlap records; resolve ties by input order. Validate nonnegative integer k. This is a lexical teaching baseline, not semantic retrieval.',
    'corrective_rag':'Implement bounded retrieval, grading, rewrite/search repair, and abstention. Grade against the original question. Preserve source records and input nonmutation. Validate records and structured answers with citations before accepting them. A citation must identify retrieved evidence; membership is not entailment. Follow the helper contracts and failure tests.'}[name_]
   out.extend([md('### TODO: '+name_+'\n'+contract),code(functions[name_] if solved else scaffold(name_, functions[name_]))])
  # The original examples become checks gated on student implementations.
  out.append(md('## Checks\nVisible checks are examples, not a complete grader. Add two normal and three failure cases.'))
  for c in cells[3:]:
   if c.cell_type=='code':out.append(code('if RUN_EXERCISES:\n'+'\n'.join('    '+line for line in c.source.splitlines())))
   elif c.source.startswith('## Next Steps'):out.append(copy.deepcopy(c))
  out.append(md('## Submission and rubric\nSubmit your implementation, test evidence, and a trace explanation. Implementation 50 points, added failure tests 25, trace and limitations 25. A default run with exercises disabled does not pass the lab. Do not import reference_support or instructor solutions to implement the tasks.'))
  notebook=nb.v4.new_notebook(cells=out,metadata={'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'},'language_info':{'name':'python'}})
  for i,c in enumerate(notebook.cells):c.id=f'{name[:2]}-{i:03}'
  nb.validate(notebook);nb.write(notebook,root/'labs'/('instructor' if solved else '')/name)

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
