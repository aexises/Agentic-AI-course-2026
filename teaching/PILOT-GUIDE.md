# Four-session lab pilot

Status: prepared; no student pilot has been conducted for this update. Times below are teaching estimates. Use the four student notebooks in `labs/`; keep `labs/instructor/` out of the student distribution.

Before class, a teaching assistant should install the pinned environment, run every notebook offline in a fresh kernel, and test the classroom's own notebook editor. Ask students to reproduce one foundation example from repaired Labs 3–4. Do not assume previous experience with asynchronous Python, typed dictionaries, or tool-call IDs; use their setup exercise to identify missing prerequisites.

| Session | Suggested allocation | Student evidence | Observe |
|---|---|---|---|
| 5 · Gemini tools, 100 minutes | Setup 15; trace 15; dispatch/protocol task 40; edge tests 20; reflection 10 | Tool call/result trace; invalid arguments and budget tests | Confusion between proposed calls and executed effects; missing IDs |
| 6 · LangGraph RAG, 110 minutes | Recall 10; state trace 20; correction task 40; conflict/abstention tests 25; reflection 15 | Source IDs, termination reason, static retrieval comparison | Treating source membership as proof of entailment |
| 7 · Agents SDK evaluation, 120 minutes | Baseline 15; SDK trace 20; metric task 35; paired evaluation 30; critique 20 | Attempted/completed counts; failure rows; experiment manifest | Treating scripted output as a model-quality result |
| 8 · LangGraph approval, 110 minutes | Threat model 15; checkpoint trace 20; policy task 35; replay tests 25; reflection 15 | Denied cases; reopened checkpoint; effect count under replay | Treating a model approval sentence as authorization |

Record one observation per student or pair: anonymous ID, session, environment, setup minutes, task minutes, completed checks, first blocking concept, assistance needed, rubric score, and suggested revision. Do not record credentials or personal conversation traces. Collect actual time even when work is unfinished; reporting only finishers biases the timing estimate.

After each session, classify failures as environment, instructions, prerequisite, implementation, or test ambiguity. Fix any reproducible blocker before the next group. Report median and range of observed times with the number of participants and unfinished submissions; retain the original estimates until measured evidence supports changing them. Re-run the offline suite after notebook edits and preserve the previous notebook hash with the pilot notes.

The pilot is complete only when a lecturer records the observed results and revision decisions. A passing software test suite is not evidence that students can finish a lab in the allotted time.
