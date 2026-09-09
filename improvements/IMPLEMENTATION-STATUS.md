# Implementation status — 9 September 2026

**Edition note:** This record describes the earlier integrated conspect and lab release. The subsequent full textbook is delivered as Markdown/LaTeX; see [textbook validation](../textbook/VALIDATION.md). The existing 52-page PDF is the earlier conspect, not a compiled version of the new textbook.


The course materials and local implementation are ready for instructor review. Live model evaluation and classroom assessment remain pending.

| Plan stage | Status | Evidence and remaining gate |
|---|---|---|
| 1. Repair teaching baseline | Implemented and tested | Course-local [ReAct](../labs/03_react_tools_repaired.ipynb) and [corrective RAG](../labs/04_corrective_rag_repaired.ipynb) foundations repair registry dispatch, bounded calculation, stop forwarding and search normalization. Lab 5 supplies the complete native tool cycle. The AAI[sum26] reference snapshot remains unchanged. |
| 2. Integrate research | Implemented | All 13 chapters include dated readings, source limitations, assessed practice and revised exam questions. [Research update](RESEARCH-UPDATE.md) and [claim ledger](CLAIM-LEDGER.md) distinguish papers, preprints, field reports, posts and documentation. |
| 3. Pilot four labs | Prepared; pilot pending | Four 90–120 minute student labs, separate solutions, [instructor guide](../teaching/INSTRUCTOR-GUIDE.md) and [pilot guide](../teaching/PILOT-GUIDE.md). Actual completion times and student outcomes have not been measured. |
| 4. Empirical evaluation | Runner implemented; live evaluation pending | [Runner](../evaluation/README.md) records manifests, paired cases, request limits, failures and attempt journals. Offline held-out and injected-failure runs pass. A selected Gemini model, API access and declared budget are still needed for live results. |
| 5. Rebuild outputs | Completed and checked | 13 Markdown chapters, 13 editable decks (156 slides), Word studybook and 52-page PDF. [Validation](VALIDATION.md) records execution, visual review and hashes. |
| 6. Capstone gate | Materials prepared; assessment pending | [Capstone](../teaching/CAPSTONE.md) specifies the task, acceptance checks and 100-point rubric; [submission template](../teaching/SUBMISSION-TEMPLATE.md) supports review. No student submissions have been assessed. |

## Verification scope

The three source checks were identity/date/type, support for the stated claim, and limits of interpretation. They are not three independent empirical replications. New research and protocol additions were checked against primary sources; the original source PDFs were unavailable in this checkout, so this work does not recertify every inherited sentence. See [source map](../SOURCE-MAP.md).

All 78 automated tests and ten notebook executions passed offline in the recorded Python environment. Student TODO checks are intentionally disabled in starter notebooks and enabled in instructor solutions. Fixtures and mocked transport tests establish the tested local behavior; they do not establish live provider behavior, general security robustness or learning gains.

Start with the [instructor guide](../teaching/INSTRUCTOR-GUIDE.md). Use the course-local repaired foundations and four student notebooks for teaching; keep instructor solutions and executed validation notebooks out of student distribution.
