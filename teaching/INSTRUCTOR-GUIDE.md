# Instructor handoff

Use the current textbook's **Exercises** and **Further study and laboratory connection** sections with the companion lecture slides. The textbook now develops each topic in continuous prose, with worked examples and selected answers. Its 35-reference bibliography is separate from the earlier P1–P3/R1–R3 reading IDs used in presentation notes. See [textbook instructions](../textbook/README.md) and [source checks](../textbook/SOURCE-CHECKS.md). Research papers, engineering reports, and API specifications remain distinct evidence types.

Distribute repaired worked examples `labs/03_react_tools_repaired.ipynb` and `labs/04_corrective_rag_repaired.ipynb` before the four assessed Labs 5–8. They are course-local replacements for the audited reference examples; the original AAI[sum26] project has not been modified. The complete native Gemini model→tool→model exercise is Lab 5. The Lab 4 search adapter is tested with an injected client; it makes no live Tavily requests.

For Labs 5–8, students first run the default worked cells, implement TODOs, enable `RUN_EXERCISES`, restart, and run all. Reference solutions in `labs/instructor/` enable checks. Use each notebook's rubric. Ask students to add an unseen failure case rather than copying only the visible tests. Do not distribute instructor solutions in the student package.

Use `evaluation/README.md` for the separate repeated-run harness. The published held-out examples demonstrate split handling; they are not secret assessment data. Create a new lecturer-owned set before grading. A perfect fixture result confirms deterministic plumbing only. Discuss why the direct catalog lookup baseline is sufficient for that toy task, and why adding an agent may be an unjustified expense.

For research discussion, ask students to identify the task, intervention, comparison, metric, and limitation before proposing a course design change. CHIVE does not make every explanation faithful; a harness improvement on one benchmark is not a universal model improvement; multi-agent failure observations do not prove all teams are worse than individual agents. Require the actual source passage for claims beyond the course's scoped summary.

Run the [pilot](PILOT-GUIDE.md) before committing to the proposed durations. Use the [capstone](CAPSTONE.md) after the four labs. Complete the [submission template](SUBMISSION-TEMPLATE.md) for each demonstration so students see what a reproducible report contains.

## Additional framework practice

Use [Labs 9–11](../labs/frameworks/README.md) after the core labs to teach LangGraph parallel state updates, LangChain middleware and termination, and PydanticAI semantic output validation. Each is planned for 110 minutes, with two graded implementation tasks and separate instructor solutions. Keep their environment separate from Labs 3–8. Ask students to compare architecture with the existing Agents SDK Lab 7 using the same task contracts, not incomparable model scores. The new track documents its own [validation scope](../labs/frameworks/VALIDATION.md).
