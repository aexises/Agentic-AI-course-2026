# Framework lab validation

Checked 2026-10-06 using Python 3.12.14 on macOS 26.3.1 arm64. These results apply only to the added framework track. The earlier labs retain their separate dependency snapshot and validation history.

## Executed

- Installed the framework dependencies into an isolated temporary environment and ran `python -m pip check`: no broken requirements.
- Ran `python scripts/validate-framework-labs.py`: six notebooks passed in fresh Jupyter kernels. Student copies executed worked examples with TODO checks disabled; all three instructor copies also executed the exercise checks. Live provider cells remained disabled.
- Ran `python -m pytest labs/frameworks/tests -q --junitxml=labs/frameworks/validation/tests.xml`: ten tests passed. They execute the actual instructor notebook code and check single/eight-worker workloads, rejection before scheduling, worker failure propagation, order-independent merging, exact model-call caps, multiple tool calls with out-of-order results, schema/currency boundaries, unknown-item retries, request-cap exhaustion, and separation from the legacy runner.
- Inspected saved text outputs: expected fixture results and explicit live-skip messages are present; no error outputs remain. Framework promotional startup output is disabled.
- Exported the student notebooks with nbconvert 7.17.1. Export succeeded, but visual inspection did not: browser policy blocked opening local `file:` previews. HTML export and source inspection are not a visual-layout check.

[Notebook results](validation/notebook-results.json) record package versions, final notebook hashes, code-cell counts, and the student/instructor distinction. [Test results](validation/tests.xml) record the regression run. [The dependency lock](requirements-lock.txt) captures the final resolved environment, including the optional HTML exporter.

## Remaining checks

Live Gemini execution, model accuracy, cost, account-specific model availability, Colab, other operating systems, and student completion times were not tested. No overall framework superiority claim is supported by these fixtures. Tool outputs and prices are invented. Saved notebook output is evidence of the tested software path, not real inventory.

To review presentation locally after installing the track requirements:

```bash
python -m jupyter nbconvert --to html labs/frameworks/09_langgraph_parallel_workers.ipynb labs/frameworks/10_langchain_middleware.ipynb labs/frameworks/11_pydanticai_typed_agents.ipynb --output-dir /tmp/framework-preview
```

Open the three HTML files in your browser or open the `.ipynb` files in a notebook editor. Check heading hierarchy, code wrapping, visible exercise instructions, and outputs at normal reading size. No graphs or quantitative figures are included because these tutorials teach execution contracts using short traces and assertions.

For live checks, supply an account-available `GEMINI_MODEL` and the key through the kernel environment, enable the live cell in Lab 10 or 11, restart, and run all. Record provider errors as errors; do not replace them with fixture outputs. Live API behavior is a separate validation step from the verified offline workflow.
