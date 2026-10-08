# Agent engineering labs

The required route is **Labs 3–16, then 18–20** (17 labs). [Lab 17](17_OPTIONAL_FINE_TUNING.md) is an optional fine-tuning project brief. Numbering preserves the AAI[sum26] reference sequence. Use the [6–8-hour self-study schedule](../teaching/SELF-STUDY-GUIDE.md). Durations are teaching estimates, not observed completion times.

## Core assignments (Labs 3–8)

| Notebook | Chapters | Student work | Estimated time |
|---|---|---|---|
| [3 · Manual ReAct](03_react_tools_repaired.ipynb) | 3, 5 | Parse protocol, dispatch, bounded loop | 90–120 min |
| [4 · Corrective retrieval](04_corrective_rag_repaired.ipynb) | 6, 7 | Retrieval, repair, valid evidence-backed answers | 90–120 min |
| [5 · Bounded Gemini tools](05_gemini_bounded_tools.ipynb) | 3, 5, 12 | Dispatch validation, complete native tool round-trip, budgets | 100 min |
| [6 · Corrective RAG](06_langgraph_corrective_rag.ipynb) | 6, 7, 11 | Evidence grading, query repair, provenance, abstention | 110 min |
| [7 · Agents SDK evaluation](07_agents_sdk_evaluation.ipynb) | 8, 10, 11 | Run metrics, paired counterfactuals, reviewer baseline | 120 min |
| [8 · Durable approval](08_langgraph_approval_security.ipynb) | 7, 12, 13 | Authorization policy, checkpoint resume, replay tests | 110 min |

All notebook fixtures are invented. Offline results demonstrate software behavior, not model quality. The notebooks use real LangGraph, Google GenAI data types, and the OpenAI Agents SDK. A scripted model substitutes for network inference in Lab 7. The Gemini API is the optional live provider; no OpenAI key is needed.

## Additional framework track

[Labs 9–11](frameworks/README.md) add LangGraph parallel workers, LangChain agent middleware, and PydanticAI typed agents. They have separate pinned dependencies, student notebooks, instructor solutions, and an execution report. Use a separate environment; the commands below apply to Labs 3–8.

## Practical RAG and FastAPI track

[Labs 12–16](rag/README.md) use a real PostgreSQL/pgvector database, LlamaIndex ingestion, local embedding and reranking models, and FastAPI. They require a separate environment and the complete track folder. The capstone integrates the same pgvector stack, with optional backend portability afterward.

## Engineering and optional extension

[Labs 18–20](engineering/README.md) add actual MCP tools, local Docker Compose, transactions, migrations, rollback, request logs and measured HTTP experiments. Use their separate environment and backend primer. Required deployment stays local; hosted CI and cloud are optional. [Optional Lab 17](17_OPTIONAL_FINE_TUNING.md) does not affect completion.

## Repaired foundation assignments

Labs 3–5 leave core implementation work to students. Lab 3 supplies calculator utilities but requires parser, dispatcher and loop work. Lab 4 supplies record validators but requires retrieval and corrective decisions. Lab 5 requires both dispatch validation and the native Gemini continuation. Small TODOs guide the longer functions. Separate instructor notebooks contain answers; the original reference project is unchanged.

## Local setup

Use a fresh Python 3.11+ environment. Validation used Python 3.12.14 on macOS arm64; other platforms and Python versions have not been executed here. The full resolved dependency snapshot is in `requirements-lock.txt`; direct dependencies are pinned in `requirements.txt`.

From the course root:

```bash
python3.12 -m venv .venv-labs
source .venv-labs/bin/activate
python -m pip install -r labs/requirements.txt
python -m pip check
python -m ipykernel install --user --name agentic-labs --display-name 'Agentic labs'
```

Open a notebook in an existing Jupyter-compatible editor and select **Agentic labs**. If you need a browser notebook interface, install JupyterLab separately. Do not install these requirements over the reference project's environment: that environment contains additional integrations with their own dependency constraints.

For exact dependency replay on a compatible platform, install `labs/requirements-lock.txt` instead of `labs/requirements.txt`.

## Colab setup

Upload one student `.ipynb` and `requirements.txt`. Labs 3–8 notebooks are self-contained; other tracks require their complete support directories. Run `%pip install -r /content/requirements.txt` in a temporary setup cell, restart the runtime if needed, and run the notebook. Colab itself has not been tested here; its preinstalled packages may require a fresh runtime.

## Student workflow

For assessed Labs 3–8:

1. Run the notebook with `RUN_LIVE=False` and `RUN_EXERCISES=False` to inspect setup and provided scaffolding.
2. Implement TODO functions; set `RUN_EXERCISES=True`; restart the kernel and run all cells.
3. Add the requested edge cases and complete the report in a Markdown cell.
4. Optionally enable live inference after configuring a model and key. Never submit credentials.

Instructor solution copies are in [instructor/](instructor/). They enable exercise checks. Distribute student copies without instructor folders, reference_support.py, build scripts, or executed instructor validation copies. The solutions are reference implementations, not a hidden or exhaustive grader.

## Optional live Gemini setup

Use your account's available model ID. Set `GEMINI_MODEL` and `GEMINI_API_KEY` in the environment before starting the kernel, or use a transient password prompt:

```python
import os, getpass
os.environ['GEMINI_API_KEY'] = getpass.getpass('Gemini API key: ')
os.environ['GEMINI_MODEL'] = input('Available Gemini model ID: ').strip()
```

Rerun the notebook setup cell, then enable `RUN_LIVE=True`. Account access, quotas, billing, and feature support must be checked for the chosen model. No assumption of free API access is made. Live calls were not executed during delivery validation; no account/model was configured for this task.

Lab 5 allows at most four model rounds and four tool calls. Labs 6 and 8 make one model request each. Lab 7's live section makes six agent runs with at most three model turns each, then one reviewer run with one turn. These are request limits, not monetary guarantees. Inspect actual provider usage and pricing before larger experiments. Stop and diagnose API errors rather than repeatedly rerunning the notebook.

## Validation and rebuilding

From the course root in the test environment:

```bash
python scripts/build-foundation-labs.py
python scripts/build-labs.py
python scripts/validate-labs.py
python -m pytest tests -q
```

The notebook runner uses a fresh kernel per notebook and records executed copies and hashes in `improvements/validation/`. Student TODO checks are intentionally disabled in the default copies; instructor copies execute them. See [current revision checks](../improvements/COURSE-REVISION-2026-10-08.md) and the earlier [validation notes](../improvements/VALIDATION.md) for tested scope and remaining live checks.

The separate [evaluation runner](../evaluation/README.md) adds persistent manifests, failure accounting, request caps, and development/assessment split handling. The [instructor guide](../teaching/INSTRUCTOR-GUIDE.md) explains classroom use.
