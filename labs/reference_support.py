"""Repaired foundation functions adapted from the supplied Lab 3 and Lab 4 contracts."""
from __future__ import annotations
import ast
import math
import operator
import re
from dataclasses import dataclass, field
from heapq import nlargest

_OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,
      ast.FloorDiv:operator.floordiv,ast.Mod:operator.mod,ast.Pow:operator.pow}

def calculator(expr: str) -> str:
    """Bounded arithmetic with at most 256 characters, 64 AST nodes, and magnitude 1e12."""
    def finite(value):
        if type(value) not in (int,float) or abs(value)>1e12 or not math.isfinite(value):
            raise ValueError("numeric limit")
        return value
    def compute(node,depth=0):
        if depth>16: raise ValueError("nesting limit")
        if isinstance(node,ast.Expression):return compute(node.body,depth+1)
        if isinstance(node,ast.Constant):return finite(node.value)
        if isinstance(node,ast.UnaryOp) and type(node.op) in (ast.UAdd,ast.USub):
            return finite(compute(node.operand,depth+1)*(1 if isinstance(node.op,ast.UAdd) else -1))
        if isinstance(node,ast.BinOp) and type(node.op) in _OPS:
            a,b=compute(node.left,depth+1),compute(node.right,depth+1)
            if isinstance(node.op,ast.Pow) and (type(b) is not int or abs(b)>12):raise ValueError("exponent limit")
            return finite(_OPS[type(node.op)](a,b))
        raise ValueError("unsupported expression")
    if not isinstance(expr,str) or not expr.strip() or len(expr)>256:return "calculator error: invalid input"
    try:
        tree=ast.parse(expr,mode="eval")
        if sum(1 for _ in ast.walk(tree))>64:raise ValueError("expression limit")
        return str(compute(tree))
    except (ValueError,SyntaxError,ArithmeticError,RecursionError):
        return "calculator error: invalid or out-of-bounds expression"

def word_count(text:str)->str:
    if not isinstance(text,str) or len(text)>10_000:raise ValueError("text limit")
    return str(len(text.split()))

TOOLS={"calculator":(calculator,"bounded arithmetic"),"word_count":(word_count,"count whitespace-separated words")}

def parse(text):
    if not isinstance(text,str) or len(text)>10_000:return ("error",None)
    # One action or final result only. A supplied Observation is a protocol violation.
    if re.search(r"(?m)^Observation:",text):return ("error",None)
    body=re.sub(r"\AThought:[^\n]*\n", "",text.strip()).strip()
    match=re.fullmatch(r"Final Answer:\s*(.+)",body,re.S)
    if match:return ("final",match.group(1).strip())
    match=re.fullmatch(r"Action:\s*([A-Za-z_]\w*)\[([^\[\]]*)\]",body,re.S)
    return ("action",match.group(1),match.group(2)) if match else ("error",None)

def run_tool(action,action_input,tools=TOOLS):
    if not isinstance(action,str) or action not in tools:return "tool error: unknown tool"
    if not isinstance(action_input,str) or len(action_input)>10_000:return "tool error: invalid input"
    try:return tools[action][0](action_input)
    except Exception:return "tool error: execution failed"

@dataclass
class Result:
    answer: str|None
    steps: list=field(default_factory=list)
    stopped_reason: str="final_answer"

def run(task,llm,tools=TOOLS,max_steps=8):
    if type(max_steps) is not int or not 1<=max_steps<=32:raise ValueError("step budget must be 1..32")
    if not isinstance(task,str) or not task.strip() or len(task)>10_000:raise ValueError("invalid task")
    menu="\n".join(f"{name}: {desc}" for name,(_,desc) in tools.items())
    messages=[{"role":"system","content":"Emit Action: name[input] or Final Answer: text. Never emit Observation.\n"+menu},{"role":"user","content":task}]
    steps=[]
    for _ in range(max_steps):
        try:reply=llm(messages,stop=["Observation:"])
        except Exception:return Result(None,steps,"model_error")
        parsed=parse(reply)
        if parsed[0]=="final":return Result(parsed[1],steps)
        if parsed[0]=="error":return Result(None,steps,"parse_error")
        _,name,args=parsed
        observation=run_tool(name,args,tools)
        steps.append({"action":name,"input":args,"observation":observation})
        messages.extend([{"role":"assistant","content":reply},{"role":"user","content":"Observation: "+str(observation)}])
    return Result(None,steps,"max_steps")

def normalize_search(response,max_urls=2,max_chars=15_000):
    """Preserve URL provenance, cap records, and reject malformed records."""
    if type(max_urls) is not int or not 1<=max_urls<=10:raise ValueError("max_urls must be 1..10")
    if type(max_chars) is not int or not 1<=max_chars<=15_000:raise ValueError("max_chars must be 1..15000")
    rows=response.get("results",[]) if isinstance(response,dict) else []
    if not isinstance(rows,list):return []
    out=[];seen=set()
    for row in rows:
        if not isinstance(row,dict):continue
        raw,url=row.get("raw_content"),row.get("url")
        if not isinstance(raw,str) or not raw.strip() or not isinstance(url,str) or not url.startswith(("https://","http://")) or url in seen:continue
        seen.add(url);out.append({"id":url,"source":url,"text":raw[:max_chars]})
        if len(out)==max_urls:break
    return out

def search_and_scrape(query,api_key,client_factory,max_urls=2):
    if not isinstance(query,str) or not query.strip() or len(query)>1000:raise ValueError("invalid query")
    if not isinstance(api_key,str) or not api_key:raise ValueError("missing key")
    if type(max_urls) is not int or not 1<=max_urls<=10:raise ValueError("max_urls must be 1..10")
    client=client_factory(api_key=api_key)
    response=client.search(query=query,max_results=max_urls,include_raw_content=True)
    return normalize_search(response,max_urls)

def retrieve(query,records,k=3):
    if type(k) is not int or k<0:raise ValueError("invalid k")
    if not isinstance(query,str) or not query.strip():raise ValueError("invalid query")
    validate_records(records)
    q=set(re.findall(r"\w+",query.lower()))
    scored=((len(q & set(re.findall(r"\w+",r["text"].lower()))),-i,r) for i,r in enumerate(records))
    return [dict(r) for score,_,r in nlargest(k,scored,key=lambda x:x[:2]) if score>0]

def validate_records(records):
    if not isinstance(records,list):raise ValueError("records must be a list")
    seen=set()
    for row in records:
        if not isinstance(row,dict) or any(not isinstance(row.get(k),str) or not row[k].strip() for k in ('id','source','text')):
            raise ValueError("invalid evidence record")
        if row['id'] in seen:raise ValueError("duplicate evidence ID")
        seen.add(row['id'])

def valid_answer(answer,docs):
    if not isinstance(answer,dict) or set(answer)!={'text','citations'}:return False
    citations=answer['citations']
    return (isinstance(answer['text'],str) and bool(answer['text'].strip())
            and isinstance(citations,list) and bool(citations)
            and all(isinstance(c,str) for c in citations)
            and len(citations)==len(set(citations))
            and set(citations)<={d['id'] for d in docs})

def corrective_rag(question,records,grader,rewriter,searcher,answerer,max_steps=3):
    if type(max_steps) is not int or not 1<=max_steps<=5:raise ValueError("max_steps must be 1..5")
    if not isinstance(question,str) or not question.strip():raise ValueError("invalid question")
    validate_records(records)
    corpus={r['id']:dict(r) for r in records};query=question;trace=[]
    for step in range(max_steps):
        docs=retrieve(query,list(corpus.values()))
        trace.append({"query":query,"retrieved_ids":[d['id'] for d in docs]})
        if docs:
            decision=grader(question,docs)
            if type(decision) is not bool:raise ValueError("grader must return bool")
            if decision:
                answer=answerer(question,docs)
                if not valid_answer(answer,docs):
                    return {"answer":None,"trace":trace,"status":"invalid_answer"}
                return {"answer":answer,"trace":trace,"status":"answered"}
        if step+1<max_steps:
            query=rewriter(question)
            if not isinstance(query,str) or not query.strip():raise ValueError("invalid rewritten query")
            additions=searcher(query);validate_records(additions)
            for r in additions:
                if r['id'] in corpus and corpus[r['id']]!=r:raise ValueError("conflicting evidence ID")
                corpus[r['id']]=dict(r)
    return {"answer":"Insufficient evidence.","trace":trace,"status":"abstained"}
