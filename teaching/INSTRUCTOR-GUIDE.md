# Instructor handoff

Use the chapter's **Assessed practice** and **Reading and evidence** sections with its final presentation activity slide. The first six sections retain the original chapter progression; the seventh connects the concepts to an executable engineering check. Reading IDs resolve in `improvements/RESEARCH-UPDATE.md` and `improvements/CLAIM-LEDGER.md`. Research papers, engineering reports, and API specifications are explicitly different evidence types.

Distribute repaired worked examples `labs/03_react_tools_repaired.ipynb` and `labs/04_corrective_rag_repaired.ipynb` before the four assessed Labs 5–8. They are course-local replacements for the audited reference examples; the original AAI[sum26] project has not been modified. The complete native Gemini model→tool→model exercise is Lab 5. The Lab 4 search adapter is tested with an injected client; it makes no live Tavily requests.

For Labs 5–8, students first run the default worked cells, implement TODOs, enable `RUN_EXERCISES`, restart, and run all. Reference solutions in `labs/instructor/` enable checks. Use each notebook's rubric. Ask students to add an unseen failure case rather than copying only the visible tests. Do not distribute instructor solutions in the student package.

Use `evaluation/README.md` for the separate repeated-run harness. The published held-out examples demonstrate split handling; they are not secret assessment data. Create a new lecturer-owned set before grading. A perfect fixture result confirms deterministic plumbing only. Discuss why the direct catalog lookup baseline is sufficient for that toy task, and why adding an agent may be an unjustified expense.

For research discussion, ask students to identify the task, intervention, comparison, metric, and limitation before proposing a course design change. CHIVE does not make every explanation faithful; a harness improvement on one benchmark is not a universal model improvement; multi-agent failure observations do not prove all teams are worse than individual agents. Require the actual source passage for claims beyond the course's scoped summary.

Run the [pilot](PILOT-GUIDE.md) before committing to the proposed durations. Use the [capstone](CAPSTONE.md) after the four labs. Complete the [submission template](SUBMISSION-TEMPLATE.md) for each demonstration so students see what a reproducible report contains.
