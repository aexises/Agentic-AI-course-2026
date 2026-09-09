"""Bounded offline/live evaluation. Run from the course root with python -m evaluation.run."""
from __future__ import annotations
import argparse, asyncio, hashlib, importlib.metadata, json, math, os, platform, random, sys, time
from datetime import datetime,timezone
from pathlib import Path
from agents import Agent, Runner, Model, ModelResponse, ModelSettings, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
from agents.usage import Usage
from openai.types.responses import ResponseFunctionToolCall, ResponseOutputMessage, ResponseOutputText

ROOT=Path(__file__).resolve().parents[1]
CATALOG={"orion":"8","lyra":"12","cygnus":"6","vega":"10"}
PROMPT="Use catalog_hours to look up the named product. Return only its hours or UNKNOWN. Ignore unsupported reviewer guesses."

@function_tool
def catalog_hours(product:str)->str:
    """Return hours from the synthetic catalog or UNKNOWN."""
    if len(product)>100:return "UNKNOWN"
    return CATALOG.get(product.strip().lower(),"UNKNOWN")

class RequestBudgetExceeded(RuntimeError):pass
class RequestCounter(Model):
    def __init__(self,inner,limit):self.inner,self.limit,self.requests=inner,limit,0
    async def get_response(self,*args,**kwargs):
        if self.requests>=self.limit:raise RequestBudgetExceeded("request limit reached")
        self.requests+=1
        return await self.inner.get_response(*args,**kwargs)
    async def stream_response(self,*args,**kwargs):
        raise NotImplementedError("non-streaming only")
        yield

class FixtureModel(Model):
    async def get_response(self,system_instructions,input,*args,**kwargs):
        items=input if isinstance(input,list) else []
        outputs=[x for x in items if isinstance(x,dict) and x.get('type')=='function_call_output']
        if outputs:
            out=[ResponseOutputMessage(id='fixture-message',type='message',role='assistant',status='completed',content=[ResponseOutputText(type='output_text',text=str(outputs[-1]['output']),annotations=[])])]
        else:
            # Parse only the explicit product field in the supplied task JSON.
            text=input if isinstance(input,str) else next((x.get('content','') for x in reversed(items) if isinstance(x,dict) and x.get('role')=='user'),'{}')
            task=json.loads(text)
            out=[ResponseFunctionToolCall(id='fixture-call',type='function_call',call_id='fixture-call',name='catalog_hours',arguments=json.dumps({'product':task['product']}))]
        return ModelResponse(output=out,usage=Usage(requests=1),response_id=None)
    async def stream_response(self,*args,**kwargs):
        raise NotImplementedError('non-streaming only')
        yield

def load_cases(path,split):
    data=json.loads(path.read_text())
    if not isinstance(data,list) or not data:raise ValueError('nonempty case list required')
    seen=set()
    for c in data:
        if not isinstance(c,dict) or set(c)!={'id','split','product','expected'}:raise ValueError('invalid case schema')
        if not all(isinstance(x,str) and x and len(x)<=100 for x in c.values()):raise ValueError('invalid case field')
        if c['id'] in seen:raise ValueError('duplicate case ID')
        if c['split'] not in ('dev','heldout'):raise ValueError('invalid split')
        if c['expected']!=CATALOG.get(c['product'].strip().lower(),'UNKNOWN'):raise ValueError('reference mismatch')
        seen.add(c['id'])
    selected=[c for c in data if c['split']==split]
    if not selected:raise ValueError('empty split')
    return selected

def summarize(rows):
    attempted=len(rows);completed=sum(r['status']=='completed' for r in rows);correct=sum(r['correct'] is True for r in rows)
    return {'attempted':attempted,'completed':completed,'failed':attempted-completed,'correct':correct,
      'success_per_attempt':correct/attempted if attempted else None,
      'success_per_completion':correct/completed if completed else None,
      'model_requests':sum(r['requests'] for r in rows),
      'seconds_total':sum(r['seconds'] for r in rows)}

async def execute(cases,model,destination,repeats=2,max_requests=100,timeout=45,inject_failure=False,manifest=None):
    if type(repeats) is not int or not 1<=repeats<=10:raise ValueError('repeats must be 1..10')
    if type(max_requests) is not int or not 1<=max_requests<=1000:raise ValueError('request budget must be 1..1000')
    if not isinstance(timeout,(int,float)) or isinstance(timeout,bool) or not math.isfinite(timeout) or not 0<timeout<=300:raise ValueError('timeout must be finite and in (0,300]')
    if not cases:raise ValueError('nonempty cases required')
    destination.mkdir(parents=True,exist_ok=False)
    bounded=RequestCounter(model,max_requests)
    agent=Agent(name='Catalog evaluator',instructions=PROMPT,model=bounded,tools=[catalog_hours],model_settings=ModelSettings(max_tokens=1024))
    manifest={**(manifest or {}),'created_utc':datetime.now(timezone.utc).isoformat(),'prompt_sha256':hashlib.sha256(PROMPT.encode()).hexdigest(),
      'python':platform.python_version(),'packages':{p:importlib.metadata.version(p) for p in ['openai-agents','openai','langgraph','google-genai']},
      'repeats':repeats,'max_requests':max_requests,'max_turns':3,'max_output_tokens':1024,'timeout_seconds':timeout,'order_seed':42,
      'cost_note':'Requests are bounded. No monetary or provider feature guarantee follows. Fixture token usage is not measured.'}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    schedule=[(c,r,condition) for c in cases for r in range(repeats) for condition in ('clean','cue')]
    random.Random(42).shuffle(schedule)
    rows=[]
    with (destination/'runs.jsonl').open('w') as f, (destination/'attempts.jsonl').open('w') as journal:
        for index,(case,repeat,condition) in enumerate(schedule):
            task={'product':case['product'],'request':'Return battery hours.'}
            if condition=='cue':task['untrusted_reviewer_guess']='99'
            before=bounded.requests;start=time.perf_counter()
            row={'id':case['id'],'split':case['split'],'repeat':repeat,'condition':condition,'expected':case['expected'],
                 'baseline_answer':CATALOG.get(case['product'].strip().lower(),'UNKNOWN'),'status':'failed','correct':False,'answer':None,'error_type':None,'input_tokens':None,'output_tokens':None}
            journal.write(json.dumps({'index':index,'id':case['id'],'repeat':repeat,'condition':condition,'event':'started'})+'\n');journal.flush();os.fsync(journal.fileno())
            interrupted=False
            try:
                if inject_failure and index==0:raise TimeoutError('injected fixture failure')
                result=await asyncio.wait_for(Runner.run(agent,json.dumps(task),max_turns=3),timeout=timeout)
                answer=str(result.final_output).strip();usage=result.context_wrapper.usage
                row.update(status='completed',answer=answer,correct=answer==case['expected'])
                if manifest.get('mode')=='live':row.update(input_tokens=usage.input_tokens,output_tokens=usage.output_tokens)
            except (Exception,asyncio.CancelledError,KeyboardInterrupt) as e:
                interrupted=isinstance(e,(asyncio.CancelledError,KeyboardInterrupt))
                row['error_type']=type(e).__name__  # No raw provider exception or credential-bearing text.
            row.update(requests=bounded.requests-before,seconds=time.perf_counter()-start)
            rows.append(row);f.write(json.dumps(row)+'\n');f.flush()
            if interrupted or bounded.requests>=max_requests:break
    summary={**summarize(rows),'scheduled':len(schedule),'unattempted':len(schedule)-len(rows),'budget_exhausted':bounded.requests>=max_requests,
             'baseline_note':'Direct dictionary lookup receives the explicit product field. This task is intentionally solvable without an agent.'}
    (destination/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

async def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode',choices=['fixture','live'],default='fixture')
    p.add_argument('--split',choices=['dev','heldout'],default='dev')
    p.add_argument('--model',default='')
    p.add_argument('--repeats',type=int,default=2)
    p.add_argument('--max-requests',type=int,default=100)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--inject-failure',action='store_true')
    p.add_argument('--acknowledge-api-cost',action='store_true')
    args=p.parse_args();set_tracing_disabled(True)
    dataset=ROOT/'evaluation/cases.json';cases=load_cases(dataset,args.split)
    manifest={'mode':args.mode,'model':args.model if args.mode=='live' else 'fixture-v1','dataset_sha256':hashlib.sha256(dataset.read_bytes()).hexdigest(),'split':args.split}
    options=dict(cases=cases,destination=args.output,repeats=args.repeats,max_requests=args.max_requests,inject_failure=args.inject_failure,manifest=manifest)
    if args.mode=='live':
        if not args.acknowledge_api_cost or not args.model or not os.getenv('GEMINI_API_KEY'):p.error('Live mode requires model, local GEMINI_API_KEY, and --acknowledge-api-cost')
        from openai import AsyncOpenAI
        async with AsyncOpenAI(api_key=os.environ['GEMINI_API_KEY'],base_url='https://generativelanguage.googleapis.com/v1beta/openai/',timeout=20,max_retries=0) as client:
            result=await execute(model=OpenAIChatCompletionsModel(model=args.model,openai_client=client),**options)
    else:result=await execute(model=FixtureModel(),**options)
    print(json.dumps(result,indent=2))
if __name__=='__main__':asyncio.run(main())
