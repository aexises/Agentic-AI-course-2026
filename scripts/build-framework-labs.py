"""Build the framework tutorial track; run from any working directory."""
from pathlib import Path
import copy
import nbformat as nb

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'labs/frameworks'

def md(s): return nb.v4.new_markdown_cell(s.strip())
def code(s): return nb.v4.new_code_cell(s.strip())
def task(text, stub, solution, checks):
    return [md(text), {'stub': stub, 'solution': solution}, code('if RUN_EXERCISES:\n' + '\n'.join('    '+x for x in checks.strip().splitlines()))]

def save(name, cells):
    for solved in (False, True):
        result=[]
        for cell in cells:
            if 'stub' in cell:
                result.append(code(cell['solution'] if solved else cell['stub']))
            else:
                item=copy.deepcopy(cell)
                if solved and item.cell_type=='code':
                    item.source=item.source.replace('RUN_EXERCISES = False','RUN_EXERCISES = True')
                result.append(item)
        notebook=nb.v4.new_notebook(cells=result, metadata={'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'},'language_info':{'name':'python'}})
        # Stable cell IDs make regeneration reviewable.
        for i, cell in enumerate(notebook.cells): cell.id=f'{name[:2]}-{i:03d}'
        nb.validate(notebook)
        nb.write(notebook, OUT / ('instructor' if solved else '') / (name+'.ipynb'))

SETUP_MD='''## Setup
Use the separate `labs/frameworks/requirements.txt` environment described in this track's README. Do not upgrade the earlier lab environment in place. Each notebook is self-contained after installation. Python 3.12 is the tested interpreter family.

Default execution uses invented equipment-service fixtures and real framework runtimes, without network inference. These checks establish application behavior, not model accuracy. Student tasks are disabled until you implement them and set `RUN_EXERCISES=True`. Instructor copies enable them. Optional live cells require explicit `RUN_LIVE=True`, `GEMINI_API_KEY`, and `GEMINI_MODEL`. Choose a model available to your account; API use consumes quota. Keep credentials out of notebook cells and saved output.
'''
SETUP='''import os
from importlib.metadata import version
RUN_EXERCISES = False
RUN_LIVE = False

def live_config():
    key, model = os.getenv("GEMINI_API_KEY"), os.getenv("GEMINI_MODEL")
    if not key or not model:
        raise RuntimeError("Set GEMINI_API_KEY and GEMINI_MODEL before enabling live calls")
    return key, model

print({p: version(p) for p in ("langgraph", "langchain", "pydantic-ai-slim")})'''

cells=[md('''# Lab 9 · LangGraph: parallel workers and explicit state
## Goal
Build a bounded equipment-policy review with `StateGraph`, dynamic `Send` workers, a reducer, and an aggregation barrier. Explain why collecting worker results is different from trusting them. Prerequisites: Labs 6 and 8, Python types and dictionaries; textbook chapters 4, 7, 8, and 11.

Estimated 110 minutes: 15 reading, 20 worked trace, 45 implementation, 20 failure cases, 10 explanation. By the end you will handle zero workers, preserve source identity, bound fan-out, and make deterministic output independent of worker completion order.

This exercise focuses on orchestration. Workers perform a transparent lexical check rather than pretend to be intelligent reviewers. A later model substitution must be evaluated separately.'''),md(SETUP_MD),code(SETUP),md('''## Steps
### 1. Define the workload and its contract
A document has a unique, nonempty string ID and nonempty text. Accept at most eight documents. Reject duplicates rather than letting a reducer silently overwrite one. The batch validator runs before any worker is scheduled. This is a teaching limit, not a framework limit.'''),code('''from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

class ReviewState(TypedDict):
    docs: list[dict]
    findings: Annotated[list[dict], operator.add]
    summary: list[dict]

class WorkerState(TypedDict):
    doc: dict

def validate_docs(docs):
    if not isinstance(docs, list) or len(docs) > 8:
        raise ValueError("docs must be a list of at most eight documents")
    seen = set()
    for doc in docs:
        if not isinstance(doc, dict) or set(doc) != {"id", "text"}:
            raise ValueError("document requires exactly id and text")
        if any(not isinstance(doc[k], str) or not doc[k].strip() for k in ("id", "text")):
            raise ValueError("id and text must be nonempty strings")
        if doc["id"] in seen:
            raise ValueError("duplicate document ID")
        seen.add(doc["id"])
    return docs

def worker(state: WorkerState):
    doc = state["doc"]
    return {"findings": [{"id": doc["id"], "mentions_approval": "approval" in doc["text"].lower()}]}

def route(state):
    return [Send("review", {"doc": doc}) for doc in state["docs"]] or "aggregate"

def aggregate(state):
    return {"summary": sorted(state["findings"], key=lambda row: row["id"])}

def make_graph(worker_fn=worker):
    graph = StateGraph(ReviewState)
    graph.add_node("validate", lambda state: {"docs": validate_docs(state["docs"])})
    graph.add_node("review", worker_fn)
    graph.add_node("aggregate", aggregate)
    graph.add_edge(START, "validate")
    graph.add_conditional_edges("validate", route, ["review", "aggregate"])
    graph.add_edge("review", "aggregate")
    graph.add_edge("aggregate", END)
    return graph.compile()

app = make_graph()
docs = [{"id":"B", "text":"Approval required for loans."}, {"id":"A", "text":"Bring student ID."}]
result = app.invoke({"docs": docs, "findings": [], "summary": []}, config={"max_concurrency":2})
assert result["summary"] == [{"id":"A", "mentions_approval":False}, {"id":"B", "mentions_approval":True}]
print(result["summary"])'''),md('''### 2. Trace the graph
`Send` gives each worker its own input. The reducer appends updates into the shared findings list. Sorting is an explicit presentation decision; do not depend on worker finish order. This graph does not have a checkpointer: invoke starts a fresh run. An in-memory result is not durable storage.

The validator costs O(n) plus string inspection; sorting n findings costs O(n log n), with O(n) stored results. Concurrency can overlap work but does not prove a speedup for these tiny Python functions. Total provider calls would grow with worker count if inference were added.'''),code('''updates = list(app.stream({"docs":docs, "findings":[], "summary":[]}, stream_mode="updates"))
print([list(event) for event in updates])
assert app.invoke({"docs":[], "findings":[], "summary":[]})["summary"] == []
for bad in (None, {}, [docs[0], docs[0]], [{"id":"", "text":"x"}], [{"id":"x","text":1}], docs * 5):
    try:
        app.invoke({"docs":bad, "findings":[], "summary":[]})
    except ValueError:
        pass
    else:
        raise AssertionError("invalid batch accepted")
print("Worked boundary checks passed")''')]
cells+=task('''### 3. TODO: build a conservative consensus reducer (35 points)
Implement `merge_findings(rows)` returning one row per ID in sorted order. A row must contain exactly `id` and a boolean `mentions_approval`. Reject malformed values. Repeated identical findings collapse; conflicting values for an ID raise `ValueError`. Do not resolve a disagreement by last-write-wins. Empty input returns an empty list.''','''def merge_findings(rows):
    raise NotImplementedError("TODO: validate, deduplicate, and detect disagreement")''','''def merge_findings(rows):
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    merged = {}
    for row in rows:
        if (not isinstance(row, dict) or set(row) != {"id", "mentions_approval"}
            or not isinstance(row["id"], str) or not row["id"].strip()
            or type(row["mentions_approval"]) is not bool):
            raise ValueError("invalid finding")
        key, value = row["id"], row["mentions_approval"]
        if key in merged and merged[key] != value:
            raise ValueError("conflicting findings")
        merged[key] = value
    return [{"id":key, "mentions_approval":merged[key]} for key in sorted(merged)]''','''assert merge_findings([]) == []
assert merge_findings(result["summary"] * 2) == result["summary"]
for bad in (None, [{"id":"A", "mentions_approval":1}], [{"id":"A", "mentions_approval":True}, {"id":"A", "mentions_approval":False}]):
    try: merge_findings(bad)
    except ValueError: pass
    else: raise AssertionError("bad findings accepted")''')
cells+=task('''### 4. TODO: integrate the reducer into the graph (35 points)
Build `make_consensus_graph(worker_fn)` with the same validation, routing, worker, and aggregation topology. Aggregation must call your `merge_findings`, not the worked `aggregate`. Demonstrate an injected worker returning duplicates and another returning a conflict. Dependency injection lets tests change behavior without network inference.''','''def make_consensus_graph(worker_fn):
    raise NotImplementedError("TODO: wire the graph to merge_findings")''','''def make_consensus_graph(worker_fn):
    graph = StateGraph(ReviewState)
    graph.add_node("validate", lambda s: {"docs":validate_docs(s["docs"])})
    graph.add_node("review", worker_fn)
    graph.add_node("aggregate", lambda s: {"summary":merge_findings(s["findings"])})
    graph.add_edge(START,"validate")
    graph.add_conditional_edges("validate", route, ["review", "aggregate"])
    graph.add_edge("review","aggregate")
    graph.add_edge("aggregate",END)
    return graph.compile()''','''def doubled(s): return {"findings":worker(s)["findings"] * 2}
assert make_consensus_graph(doubled).invoke({"docs":docs,"findings":[],"summary":[]})["summary"] == result["summary"]
def conflict(s):
    key=s["doc"]["id"]
    return {"findings":[{"id":key,"mentions_approval":True},{"id":key,"mentions_approval":False}]}
try: make_consensus_graph(conflict).invoke({"docs":docs[:1],"findings":[],"summary":[]})
except ValueError: pass
else: raise AssertionError("conflict hidden")
assert make_consensus_graph(worker).invoke({"docs":[],"findings":[],"summary":[]})["summary"] == []
print("Student graph checks passed")''')
cells += [md('''## Checks and submission
Submit the completed notebook and a short trace explaining validation → fan-out → aggregation. Add a one-document test, an eight-document test, and a test showing invalid input schedules no worker. Explain why the lexical rule fails on “approval is not required.” Replace it only after defining a labeled evaluation set.

Rubric: conservative merge 35; graph integration 35; added boundary tests 15; trace and limitations 15. The included checks are a starter suite, not exhaustive grading.

## Next Steps
Use Lab 8 for durable approval; combine it with this graph only after deciding what state and effects can be replayed. Compare the explicit graph to Lab 10's agent loop and Lab 7's Agents SDK runner. Framework choice is a design tradeoff, not a benchmark ranking.

References checked 2026-10-06: [LangGraph Graph API: Send, reducers, edges](https://docs.langchain.com/oss/python/langgraph/graph-api), [persistence](https://docs.langchain.com/oss/python/langgraph/persistence). The implementation and tests are original course examples.''')]
save('09_langgraph_parallel_workers',cells)

cells=[md('''# Lab 10 · LangChain: an agent loop with enforceable limits
## Goal
Use `create_agent`, real tool messages, custom tool middleware, and model-call limits. Compare a high-level agent factory with the explicit graph from Lab 9 and the OpenAI Agents SDK in Lab 7. Prerequisites: Labs 5–7; textbook chapters 3, 5, 11, and 12.

Estimated 110 minutes: 15 architecture, 20 trace, 40 implementation, 20 failure injection, 15 comparison. You will test success, rejected arguments, and a model that never stops asking for tools. The deterministic model below scripts responses; it is not a language model and cannot establish inference quality.'''),md(SETUP_MD),code(SETUP),md('''## Steps
### 1. Implement a narrow tool and a scripted model
The tool returns an invented inventory count. A model call requests the tool; a second call incorporates its result. `bind_tools` is a testing adapter here: it returns the scripted model unchanged. A provider integration must actually bind and transmit the schema. Inspect the returned message sequence, not only the final string.'''),code('''from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_tool_call
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult

INVENTORY = {"camera":2, "tripod":0}

def stock(item: str) -> str:
    """Return the available count for a known equipment item."""
    if item not in INVENTORY:
        raise ValueError("unknown equipment")
    return str(INVENTORY[item])

class ScriptedInventoryModel(BaseChatModel):
    item: str = "camera"
    repeat: bool = False
    @property
    def _llm_type(self): return "course-scripted-inventory"
    def bind_tools(self, tools, **kwargs): return self
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        tool_messages = [m for m in messages if isinstance(m, ToolMessage)]
        if tool_messages and not self.repeat:
            message = AIMessage(content="Inventory response: " + str(tool_messages[-1].content))
        else:
            message = AIMessage(content="", tool_calls=[{"name":"stock", "args":{"item":self.item}, "id":f"stock-{len(tool_messages)}", "type":"tool_call"}])
        return ChatResult(generations=[ChatGeneration(message=message)])

@wrap_tool_call
def safe_tool_errors(request, handler):
    try:
        return handler(request)
    except ValueError:
        return ToolMessage(content="invalid_equipment", tool_call_id=request.tool_call["id"], status="error")

agent = create_agent(ScriptedInventoryModel(), tools=[stock], middleware=[safe_tool_errors, ModelCallLimitMiddleware(run_limit=3, exit_behavior="error")])
trace = agent.invoke({"messages":[{"role":"user", "content":"How many cameras?"}]})
assert trace["messages"][-1].content == "Inventory response: 2"
print([(m.type, m.content) for m in trace["messages"]])'''),md('''### 2. Separate protocol correctness from answer quality
Check that the ToolMessage refers to the original tool-call ID. The error middleware exposes a stable error code; it does not silently invent a count. Returning an error message permits recovery, but the scripted model merely repeats that code. Application success still needs an independent criterion.

A model-call cap bounds loop iterations involving the model. It is not a token or currency budget, and parallel tool calls can require an additional tool-call limit. A run cap resets on a new invocation; a thread cap requires persisted thread state.'''),code('''unknown = create_agent(ScriptedInventoryModel(item="spaceship"), tools=[stock], middleware=[safe_tool_errors])
failed = unknown.invoke({"messages":[{"role":"user","content":"Check equipment"}]})
tool_reply = next(m for m in failed["messages"] if isinstance(m, ToolMessage))
assert tool_reply.status == "error" and tool_reply.content == "invalid_equipment"
assert tool_reply.tool_call_id == "stock-0"
print("Unknown equipment was rejected; no count was fabricated.")''')]
cells+=task('''### 3. TODO: construct a bounded agent (35 points)
Implement `bounded_agent(model, limit)` using `create_agent`, `stock`, `safe_tool_errors`, and `ModelCallLimitMiddleware`. Accept only integers 1–5 (reject booleans) and use `exit_behavior="error"`. Invalid limits must raise `ValueError` before building the agent.''','''def bounded_agent(model, limit):
    raise NotImplementedError("TODO: validate limit and configure middleware")''','''def bounded_agent(model, limit):
    if type(limit) is not int or not 1 <= limit <= 5:
        raise ValueError("limit must be an integer from 1 to 5")
    return create_agent(model, tools=[stock], middleware=[safe_tool_errors, ModelCallLimitMiddleware(run_limit=limit, exit_behavior="error")])''','''from langchain.agents.middleware.model_call_limit import ModelCallLimitExceededError
request = {"messages":[{"role":"user","content":"Check camera stock"}]}
assert bounded_agent(ScriptedInventoryModel(), 2).invoke(request)["messages"][-1].content.endswith("2")
for limit in (1,2,5):
    try: bounded_agent(ScriptedInventoryModel(repeat=True), limit).invoke(request)
    except ModelCallLimitExceededError: pass
    else: raise AssertionError("runaway model escaped budget")
for bad in (True,0,6,-1,1.5,None,"2"):
    try: bounded_agent(ScriptedInventoryModel(), bad)
    except ValueError: pass
    else: raise AssertionError("invalid limit accepted")''')
cells+=task('''### 4. TODO: audit the message protocol (35 points)
Implement `audit_trace(messages)` returning `{"calls": n, "results": n}` for a complete trace. Across AI messages collect tool-call IDs; reject duplicate IDs, tool results without a preceding call, duplicate results, and a trace ending with unresolved calls. Raise `ValueError` for those protocol errors. Empty input is a valid zero-call trace. Assume elements are LangChain message objects.''','''def audit_trace(messages):
    raise NotImplementedError("TODO: match calls with results")''','''def audit_trace(messages):
    seen, resolved = set(), set()
    for message in messages:
        if isinstance(message, AIMessage):
            for call in message.tool_calls:
                if call["id"] in seen:
                    raise ValueError("duplicate call")
                seen.add(call["id"])
        elif isinstance(message, ToolMessage):
            key = message.tool_call_id
            if key not in seen or key in resolved:
                raise ValueError("orphan or duplicate result")
            resolved.add(key)
    if seen != resolved:
        raise ValueError("unresolved calls")
    return {"calls":len(seen), "results":len(resolved)}''','''assert audit_trace([]) == {"calls":0,"results":0}
assert audit_trace(trace["messages"]) == {"calls":1,"results":1}
call = next(m for m in trace["messages"] if isinstance(m,AIMessage) and m.tool_calls)
reply = next(m for m in trace["messages"] if isinstance(m,ToolMessage))
for bad in ([reply], [call], [call,call], [call,reply,reply]):
    try: audit_trace(bad)
    except ValueError: pass
    else: raise AssertionError("bad protocol accepted")
print("Student agent and protocol checks passed")''')
cells += [md('''### 5. Optional Gemini integration
Replace only the model adapter and retain the same tool and call-limit middleware. This uses the provider SDK through LangChain; the live answer may differ and may omit a tool call. Inspect that behavior rather than asserting an exact text match. This cell is off by default and has not been validated against a live account.'''),code('''if RUN_LIVE:
    from langchain_google_genai import ChatGoogleGenerativeAI
    key, model_name = live_config()
    live_model = ChatGoogleGenerativeAI(model=model_name, google_api_key=key, temperature=0, max_retries=0)
    live_agent = create_agent(live_model, tools=[stock], middleware=[safe_tool_errors, ModelCallLimitMiddleware(run_limit=3, exit_behavior="error")])
    live_result = live_agent.invoke({"messages":[{"role":"user", "content":"Use stock to find the number of cameras currently available."}]})
    print(live_result["messages"][-1].content)
else:
    print("Live Gemini request skipped.")'''),md('''## Checks and submission
Submit the notebook plus a comparison with Lab 7: where are tools declared, who runs the loop, how is termination bounded, and what makes a run successful? Add a multi-tool-call message to the audit tests and explain why a call-limit exception is a recorded failure, not a successful answer. Do not compare framework quality using the scripted model's success rate.

Rubric: bounded agent 35; protocol audit 35; added failure tests 15; architecture comparison 15. Estimated timing is a teaching plan, not a measured completion statistic.

## Next Steps
Evaluate live models on the same held-out cases and budgets before selecting an implementation. Keep transport retries distinct from model reasoning turns. Extend the tool boundary to use request-scoped authorization if it ever performs writes.

References checked 2026-10-06: [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents), [middleware and model-call limits](https://docs.langchain.com/oss/python/langchain/middleware/built-in), [Gemini integration](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai).''')]
save('10_langchain_middleware',cells)

cells=[md('''# Lab 11 · PydanticAI: typed output is only the first check
## Goal
Build a typed equipment quote with dependency injection, a real tool round-trip, an output validator, and bounded requests. Test it using PydanticAI's `FunctionModel`, then optionally replace that model with Gemini. Prerequisites: Lab 5 and textbook chapters 5, 11, and 12; Python dataclasses and Pydantic models.

Estimated 110 minutes: 15 contracts, 20 worked example, 40 implementation, 20 failure cases, 15 report. You will demonstrate a schema-valid but factually invalid quote and reject it using the supplied catalog. This is a proposal only: no inventory is reserved and no payment is made.'''),md(SETUP_MD),code(SETUP),md('''## Steps
### 1. Define a typed output and request-scoped data
The catalog is trusted application data in this lab. Prices are integer cents to avoid binary floating-point currency arithmetic. A valid JSON shape cannot establish that the price equals the current catalog. The validator must consult the injected dependency. The test model will first call `catalog_price`, then emit a typed output tool call.'''),code('''from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict, Field, ValidationError
import pydantic_ai
pydantic_ai.BANNER_ENABLED = False
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelResponse, ToolCallPart, ToolReturnPart
from pydantic_ai.usage import UsageLimits
from pydantic_ai.exceptions import UnexpectedModelBehavior

class Quote(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    item: str = Field(min_length=1)
    quantity: int = Field(ge=1, le=5)
    total_cents: int = Field(ge=0, le=100_000)

@dataclass(frozen=True)
class Catalog:
    prices: dict[str, int]

catalog = Catalog(prices={"camera":2500, "tripod":500})

def scripted_quote(messages, info):
    # Deterministic protocol fixture: fixed task, not natural-language understanding.
    returns = [part for message in messages for part in message.parts if isinstance(part, ToolReturnPart) and part.tool_name == "catalog_price"]
    if not returns:
        return ModelResponse(parts=[ToolCallPart("catalog_price", {"item":"camera"}, tool_call_id="price-1")])
    return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, {"item":"camera", "quantity":2, "total_cents":returns[-1].content * 2}, tool_call_id="quote-1")])

agent = Agent(FunctionModel(scripted_quote), deps_type=Catalog, output_type=Quote, retries=1)

@agent.tool
def catalog_price(ctx: RunContext[Catalog], item: str) -> int:
    """Read the unit price in cents for a catalog item."""
    if item not in ctx.deps.prices:
        raise ModelRetry("Choose an item in the supplied catalog")
    return ctx.deps.prices[item]

@agent.output_validator
def verify_quote(ctx: RunContext[Catalog], output: Quote) -> Quote:
    price = ctx.deps.prices.get(output.item)
    if price is None or output.total_cents != price * output.quantity:
        raise ModelRetry("Quote must agree with the supplied catalog")
    return output

result = await agent.run("Quote two cameras", deps=catalog, usage_limits=UsageLimits(request_limit=3))
assert result.output == Quote(item="camera",quantity=2,total_cents=5000)
print(result.output.model_dump())'''),md('''### 2. Make the semantic failure visible
The following output passes the shape constraints but contains the wrong price. Schema validation and factual validation are separate operations. The model can receive retry feedback, but a persistent error must terminate. Never catch that termination and replace the output with an invented successful quote.'''),code('''wrong = Quote(item="camera", quantity=2, total_cents=1)
assert wrong.total_cents != catalog.prices[wrong.item] * wrong.quantity

def always_wrong(messages, info):
    return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, wrong.model_dump(), tool_call_id="wrong-quote")])

with agent.override(model=FunctionModel(always_wrong)):
    try:
        await agent.run("Quote two cameras", deps=catalog, usage_limits=UsageLimits(request_limit=3))
    except UnexpectedModelBehavior:
        print("Persistent invalid price rejected after bounded retries.")
    else:
        raise AssertionError("invalid quote escaped semantic validation")

for bad in (0, 6, True, "2"):
    try: Quote(item="camera",quantity=bad,total_cents=5000)
    except ValidationError: pass
    else: raise AssertionError("invalid quantity accepted")''')]
cells+=task('''### 3. TODO: validate dependencies before inference (35 points)
Implement `checked_catalog(prices)` returning `Catalog` with a defensive dictionary copy. Accept an empty catalog. Reject non-dictionaries, empty or whitespace-only names, non-string names, booleans, non-integer cents, and prices outside 0–20,000. Raise `ValueError`. Why is `frozen=True` on a dataclass insufficient to freeze a contained dictionary?''','''def checked_catalog(prices):
    raise NotImplementedError("TODO: validate and copy dependency data")''','''def checked_catalog(prices):
    if not isinstance(prices, dict):
        raise ValueError("prices must be a dictionary")
    for key, value in prices.items():
        if not isinstance(key,str) or not key.strip() or type(value) is not int or not 0 <= value <= 20_000:
            raise ValueError("invalid catalog entry")
    return Catalog(prices=dict(prices))''','''assert checked_catalog({}).prices == {}
source = {"camera":0, "tripod":20_000}
copy_catalog = checked_catalog(source)
source["camera"] = 5
assert copy_catalog.prices["camera"] == 0
for bad in (None,[],{"":1},{"x":True},{"x":-1},{"x":20_001},{"x":float("nan")},{1:100}):
    try: checked_catalog(bad)
    except ValueError: pass
    else: raise AssertionError("bad dependency accepted")''')
cells+=task('''### 4. TODO: construct an independently testable typed agent (35 points)
Implement `make_quote_agent(model)` with the same typed dependency/output contract and bounded validation retries. Register a catalog lookup tool and a validator that enforces the item and total. Do not hard-code the fixture price; an injected catalog can change between runs. Match the tool name `catalog_price` expected by the fixture.''','''def make_quote_agent(model):
    raise NotImplementedError("TODO: create agent, register tool, register output validator")''','''def make_quote_agent(model):
    app = Agent(model, deps_type=Catalog, output_type=Quote, retries=1)
    @app.tool
    def catalog_price(ctx: RunContext[Catalog], item: str) -> int:
        """Read a unit price from the injected catalog."""
        if item not in ctx.deps.prices:
            raise ModelRetry("Unknown item")
        return ctx.deps.prices[item]
    @app.output_validator
    def validate(ctx: RunContext[Catalog], output: Quote) -> Quote:
        price = ctx.deps.prices.get(output.item)
        if price is None or output.total_cents != price * output.quantity:
            raise ModelRetry("Invalid quote for current catalog")
        return output
    return app''','''app = make_quote_agent(FunctionModel(scripted_quote))
for price in (0, 1200, 20_000):
    answer = await app.run("Quote two cameras", deps=checked_catalog({"camera":price}), usage_limits=UsageLimits(request_limit=3))
    assert answer.output.total_cents == price * 2
bad_app = make_quote_agent(FunctionModel(always_wrong))
try: await bad_app.run("Quote", deps=checked_catalog({}), usage_limits=UsageLimits(request_limit=3))
except UnexpectedModelBehavior: pass
else: raise AssertionError("unknown item accepted")
print("Student typed-agent checks passed")''')
cells += [md('''### 5. Optional Gemini integration
Use the same tool and validator with the Google model adapter. A valid result must still satisfy the catalog rule. The request cap is per run; it is not a monetary budget. Keep live results separate from deterministic fixture results.'''),code('''if RUN_LIVE:
    from pydantic_ai.models.google import GoogleModel
    from pydantic_ai.providers.google import GoogleProvider
    key, model_name = live_config()
    provider_model = GoogleModel(model_name, provider=GoogleProvider(api_key=key))
    with agent.override(model=provider_model):
        live_result = await agent.run("Use catalog_price to quote exactly two cameras.", deps=catalog, usage_limits=UsageLimits(request_limit=3))
    print(live_result.output.model_dump())
else:
    print("Live Gemini request skipped.")'''),md('''## Checks and submission
Submit the completed notebook and an explanation of schema validity, catalog consistency, and authorization. Add a test where the model requests an unknown item and exhausts retries; add an extra-field output test. Explain what would have to change if prices could change after the quote but before purchase.

Rubric: dependency validation 35; typed agent integration 35; added failure tests 15; semantic/authorization explanation 15. Neither the fixture nor its success proves that a live model will select the right item or quantity. A production contract should also validate the requested quantity and item against the user's confirmed request.

## Next Steps
Compare this agent with Lab 10 and Lab 7 using the same fixtures, budgets, and output checks. Identify one requirement each framework makes easier to express. Avoid treating API ergonomics as evidence of better model reasoning.

References checked 2026-10-06: [PydanticAI testing](https://pydantic.dev/docs/ai/guides/testing/), [agents](https://pydantic.dev/docs/ai/core-concepts/agent/), [output validation](https://pydantic.dev/docs/ai/core-concepts/output/), [Google models](https://pydantic.dev/docs/ai/models/google/). Use the pinned package implementation as the reproducibility baseline when mutable documentation changes.''')]
save('11_pydanticai_typed_agents',cells)
