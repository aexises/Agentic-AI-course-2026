# Current framework practice: Labs 9–11

Three additional Python labs teach framework APIs through executable examples, implementation tasks, failure injection, and short design reports. They extend Labs 5–8 rather than replace them. Each has a student notebook and a separate instructor solution. Planned duration is 110 minutes per lab; this has not been measured in a student pilot.

| Lab | Concrete framework work | Textbook chapters |
|---|---|---|
| [9 · LangGraph parallel workers](09_langgraph_parallel_workers.ipynb) | `StateGraph`, `Send`, reducers, empty fan-out, conflict detection, streaming updates | 4, 7, 8, 11 |
| [10 · LangChain middleware](10_langchain_middleware.ipynb) | `create_agent`, tool round-trips, error middleware, model-call caps, protocol auditing | 3, 5, 11, 12 |
| [11 · PydanticAI typed agents](11_pydanticai_typed_agents.ipynb) | Injected dependencies, typed output, semantic validators, bounded retries, test models | 5, 11, 12 |

The existing [Lab 7](../07_agents_sdk_evaluation.ipynb) supplies the OpenAI Agents SDK comparison. Labs 10 and 11 include optional Gemini adapters. Lab 9 isolates orchestration using deterministic workers. This is a selected current-framework track, not an exhaustive survey or a claim that these frameworks outperform every alternative. Selection criteria are fit to course concepts, testable public APIs, and the ability to separate orchestration from provider inference. No comparative model-performance benchmark was run.

## Start in a separate environment

From the course root:

```bash
python3.12 -m venv .venv-frameworks
source .venv-frameworks/bin/activate
python -m pip install -r labs/frameworks/requirements.txt
python -m pip check
python -m ipykernel install --user --name course-frameworks --display-name 'Course frameworks'
```

Select **Course frameworks** in your notebook editor. For exact resolved dependencies on a compatible platform, install [requirements-lock.txt](requirements-lock.txt) instead. The direct framework versions tested are LangGraph 1.2.14, LangChain 1.4.3, langchain-google-genai 4.4.0, and PydanticAI slim 2.54.0. These were resolved on 2026-10-06; the lock is the reproducibility baseline, not a promise that they remain the latest releases.

For Colab, upload the student notebook and this directory's `requirements.txt`, install with `%pip install -r /content/requirements.txt`, then restart the runtime. Colab execution has not been tested here. No files from the course repository are required by notebook cells.

Run the worked cells first. Complete the TODO functions, set `RUN_EXERCISES=True`, restart the kernel, and run all. The notebook contains explicit contracts and grading rubrics. Default student execution skips unfinished tasks; a clean student run does not mean the exercises are solved. Instructor notebooks in [instructor/](instructor/) enable all exercise checks.

## Optional live inference

Set `GEMINI_API_KEY` and `GEMINI_MODEL` in the kernel environment without saving secrets into cells. Choose a model available in your account and set `RUN_LIVE=True` only in the notebook you want to run. Live cells consume quota and are not part of the verified offline result. Request caps do not cap currency cost or all provider-level retries. Save live results separately and record model, date, input, settings, errors, and usage when available.

## Teaching sequence and assessment

1. After Lab 6, use Lab 9 to teach state updates and dynamic worker scheduling. Ask students to trace an empty workload and conflicting worker evidence.
2. After Lab 7, use Lab 10 to contrast explicit graphs, a high-level agent factory, and the Agents SDK loop. Grade the trace and budget failure behavior, not just fluent output.
3. Use Lab 11 to separate output shape from domain correctness. Change the injected catalog during assessment; hard-coded fixture prices should fail.

Each lab allocates 70 points to two implementation tasks, 15 to added tests, and 15 to explanation. Keep the instructor folder out of the student distribution. The visible checks are formative, not a hidden test set. Use new inputs for grading. No real inventory, purchases, or external messages are modified.

## Rebuild and verify

```bash
python scripts/build-framework-labs.py
python scripts/validate-framework-labs.py
python -m pytest labs/frameworks/tests -q
```

The builder regenerates the six notebooks and clears old outputs. The validator runs every notebook in a fresh kernel, removes common API credentials from the child environment, and keeps compact executed outputs in the notebooks. It records versions, hashes, and results in [validation/notebook-results.json](validation/notebook-results.json). Jupyter needs permission to open local kernel ports. The earlier `validate-labs.py` runner covers only the older track, whose dependencies remain unchanged.

See [validation details](VALIDATION.md) for exactly what was executed and what remains untested.

## Source and claim boundaries

Official documentation was inspected on 2026-10-06, and the concrete APIs were checked against the installed versions during execution:

- [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api): state, reducers, `Send`, and graph edges.
- [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents): `create_agent` and the tool loop.
- [LangChain middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in): run limits and termination behavior.
- [LangChain Gemini integration](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai): provider adapter.
- [PydanticAI testing](https://pydantic.dev/docs/ai/guides/testing/) and [agents](https://pydantic.dev/docs/ai/core-concepts/agent/): test models, typed dependencies, and outputs.
- [PydanticAI output](https://pydantic.dev/docs/ai/core-concepts/output/): output schemas and semantic validators.
- [PydanticAI Google models](https://pydantic.dev/docs/ai/models/google/): Gemini adapter.

All catalog and policy fixtures are invented teaching examples. Offline success verifies the tested code paths, not live model reasoning, overall security, or production readiness.
