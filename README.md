# Agentic AI Course

## What is included

- [STUDYBOOK.md](STUDYBOOK.md) - the complete conspect in one file
- [EXAM-GUIDE.md](EXAM-GUIDE.md) - comparisons, diagrams, and high-value design rules
- [SOURCE-MAP.md](SOURCE-MAP.md) - original source sequence and dated-update provenance
- [chapters/](chapters/) - 13 focused Markdown chapters
- [output/presentations/](output/presentations/) - 13 editable PowerPoint decks
- [output/studybook/](output/studybook/) - printable studybook formats
- [references/source-reference-appendix.md](references/source-reference-appendix.md) - references transcribed from the source slides
- [presentations/src/](presentations/src/) - reusable presentation source

## Course structure

1. From Language Models to Agents
2. The LLM as a Reasoning Engine
3. Agent Anatomy and ReAct
4. Agentic Design Patterns
5. Tool Use, MCP, and Frameworks
6. RAG and Agentic RAG
7. Memory, State, and Context Engineering
8. Multi-Agent Systems
9. Multi-Agent Interoperability
10. Advanced Reasoning and Planning
11. Evaluation and Observability
12. Safety and Security
13. Production, Economics, and the Frontier

## Recommended study loop

Read one chapter, review its presentation, reproduce the core flow from memory, and answer the self-test without notes. Use the exam guide after chapters 3, 7, 10, and 13 as cumulative review.

## Rebuild

The Markdown studybook and decks are generated from `presentations/src/course-data.mjs` and the dated additions in `course-update.mjs`. Deck building writes drafts; finalization validates and copies them into `output/presentations/`. Presentation rendering/finalization uses the local artifact runtime (configure `PRESENTATIONS_SKILL`, `RUNTIME_PYTHON`, and `RUNTIME_NODE_MODULES` when rebuilding elsewhere). Render the DOCX with the document runtime to update the PDF.

```bash
node scripts/build-studybook.mjs
node presentations/src/build-decks.mjs
python scripts/scrub-presentation-metadata.py tmp/course-update/drafts/*.pptx
node scripts/finalize-decks.mjs
python scripts/build-studybook-docx.py
```

## Research update and student labs

- [Course improvement plan](improvements/COURSE-IMPROVEMENT-PLAN.md): prioritized weaknesses and a chapter-by-chapter implementation plan.
- [Research update](improvements/RESEARCH-UPDATE.md): recent OpenAI and Anthropic papers/posts, checked 9 September 2026.
- [Claim ledger](improvements/CLAIM-LEDGER.md): source, support, and scope checks.
- [Student labs](labs/README.md): four notebooks using LangGraph, Gemini, and the OpenAI Agents SDK, with separate instructor solutions.
- [Validation notes](improvements/VALIDATION.md): offline execution evidence and remaining live API checks.

The dated update is integrated into all 13 chapters, decks, and the Word/PDF studybook. Each chapter includes assessed practice and evidence notes.

- [Instructor guide](teaching/INSTRUCTOR-GUIDE.md), [pilot schedule](teaching/PILOT-GUIDE.md), and [capstone rubric](teaching/CAPSTONE.md).
- [Evaluation runner](evaluation/README.md): offline fixtures and a separately enabled live Gemini path.
- [Implementation status](improvements/IMPLEMENTATION-STATUS.md): completed work and remaining classroom/live validation.
