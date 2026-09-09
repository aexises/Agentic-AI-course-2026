# Validation record

Checked 9 September 2026 in a clean temporary Python **3.12.14** environment on macOS arm64. Full package versions are recorded in [requirements-lock.txt](../labs/requirements-lock.txt). `pip check` reported no broken requirements in this environment.

## Completed

- Both repaired foundation notebooks executed in fresh kernels with their worked checks enabled.
- All **four student notebooks** executed from beginning to end in fresh kernels with live inference off. Their TODO checks are intentionally disabled until students implement the functions and set `RUN_EXERCISES=True`.
- All **four instructor notebooks** executed in fresh kernels with exercise checks enabled and live inference off.
- **78 pytest cases passed**, including huge integers, NaN/infinity, output overflow, booleans in numeric fields, unknown tools, multiple calls, call/round limits, empty model responses, empty retrieval, citation membership, SDK turn exhaustion, policy boundaries, and invalid schema input.
- The real Google GenAI client serialized a tool declaration and completed a model/tool round-trip through a mocked HTTP transport. The real Agents SDK Chat Completions adapter also completed a tool round-trip through a mocked Gemini-compatible HTTP transport. Neither test contacted a provider.
- Reference-lab findings were checked with source inspection, AST inspection, and isolated fake tools/search responses. See [reference-audit.json](validation/reference-audit.json).
- Notebook hashes in [notebook-results.json](validation/notebook-results.json) match the delivered notebooks. Executed copies are stored in [validation/](validation/); these include instructor answers and are for the instructor, not student distribution.

Notebook execution proves the tested scaffold and solution code run in this environment. The assertions are regression tests, not a proof of correctness for every possible input. The tiny fixture datasets do not estimate model quality.

## Integrated output checks

- All 13 editable decks passed package, layout, font-policy and artifact-import checks: 12 slides each, 156 total. Receipts are in [validation/presentations/](validation/presentations/). Native Microsoft PowerPoint rendering was not tested.
- All 52 pages of the final DOCX-to-PDF render were visually inspected. All deck contact sheets and the new research/practice, revised exam and identified correction slides were inspected at readable size. No clipping or overlap was observed.
- Chapter source links, assessed practice, notebook hashes and final artifact hashes were checked; see [release-audit.json](validation/release-audit.json).
- The evaluation runner completed 16 held-out fixture attempts with 32 scripted model requests. The injected-timeout run retained all 12 attempts: 11 completed and one failed. These are infrastructure tests, not Gemini performance measurements. See [evaluation results](../evaluation/results/).
- Added edge cases cover text-protocol ambiguity, malformed search responses, expression depth/size, invalid budgets, duplicate dataset IDs, cancellation journaling and failed-attempt denominators. The test report is [pytest-results.xml](validation/pytest-results.xml).

## Not executed

**Authenticated Gemini requests:** no model/API account was configured for this task. Provider authentication, quota, actual model tool-selection behavior, model-specific schema support, and live usage remain unverified. Mocked wire tests validate client integration, not the remote service.

**Other environments:** Colab, Windows/Linux, other Python versions, and a full process-kill recovery test were not run. Lab 8 closes/reopens its SQLite saver and recreates the graph in one process; it does not claim an external-service exactly-once guarantee.

**Pedagogical outcomes:** estimated durations and grading weights have not been piloted with students. All 13 chapters and decks were rebuilt; the studybook was rebuilt as DOCX and PDF. This does not demonstrate improved student outcomes.

## Reproduce the checks

From the course root in a fresh environment:

```bash
python3.12 -m venv .venv-labs
source .venv-labs/bin/activate
python -m pip install -r labs/requirements-lock.txt
python -m pip check
python scripts/validate-labs.py
python -m pytest tests -q
```

The notebook runner needs permission to start local Jupyter kernels. It never enables live inference. To rerun the reference audit on this machine:

```bash
python scripts/audit-reference-labs.py
```

That audit script requires the local AAI[sum26] snapshot at its documented path; it is not a student dependency.

## Live acceptance checks before classroom use

1. Choose a Gemini model available in the instructor account; configure `GEMINI_MODEL` and `GEMINI_API_KEY` outside saved notebook content.
2. Open each instructor solution, leave `RUN_EXERCISES=True`, enable `RUN_LIVE=True`, and run from the first cell.
3. Lab 5: inspect an actual tool result and final answer; check the returned trace and termination status.
4. Lab 6: check parsed output, citation membership, and semantic support independently. An ID check alone is insufficient.
5. Lab 7: retain each paired run and any failure, model ID, date, versions, actual usage, and reviewer overhead. Do not infer model quality from the scripted results.
6. Lab 8: record the model proposal and runtime-policy decision separately. The live cell deliberately executes no proposed action.
7. Remove credentials and sensitive outputs before distributing notebooks. Review current provider quotas/pricing before expanding live experiments.
