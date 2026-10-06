# Agentic AI Course

The current studybook is a full textbook in [Markdown](STUDYBOOK.md) and [LaTeX source](textbook/latex/main.tex). See [textbook build instructions](textbook/README.md). It replaces the earlier conspect; the existing Word/PDF files remain the prior concise edition.

## What is included

- [STUDYBOOK.md](STUDYBOOK.md) - the complete textbook with linked citations and selected answers
- [EXAM-GUIDE.md](EXAM-GUIDE.md) - comparisons, diagrams, and high-value design rules
- [SOURCE-MAP.md](SOURCE-MAP.md) - original source sequence and dated-update provenance
- [chapters/](chapters/) - 13 focused Markdown chapters
- [output/presentations/](output/presentations/) - 13 editable PowerPoint decks
- [output/studybook/](output/studybook/) - prior conspect formats (not the new textbook)
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

## Rebuild the textbook

Edit `chapters/*.md`, the front matter and appendices in `textbook/`, and `textbook/references.json`. Then run:

```bash
python3 scripts/build-textbook.py
python3 -m unittest discover -s tests -p test_textbook.py
```

This writes matching Markdown and LaTeX without compiling a PDF. To compile:

```bash
cd textbook/latex
xelatex main.tex
xelatex main.tex
```

Use XeLaTeX or LuaLaTeX, including when uploading the source archive to Overleaf. No BibTeX/Biber run is required. See [textbook/README.md](textbook/README.md) for dependencies and source conventions. The old `node scripts/build-studybook.mjs` command forwards to the new source builder and cannot regenerate the abbreviated chapters from slide bullets.

Presentation sources remain in `presentations/src/`. Their build process is separate: `node presentations/src/build-decks.mjs`, metadata scrubbing, then `node scripts/finalize-decks.mjs`. The previously validated decks remain companion lecture material.

## Research update and student labs

- [Course improvement plan](improvements/COURSE-IMPROVEMENT-PLAN.md): prioritized weaknesses and a chapter-by-chapter implementation plan.
- [Research update](improvements/RESEARCH-UPDATE.md): recent OpenAI and Anthropic papers/posts, checked 9 September 2026.
- [Claim ledger](improvements/CLAIM-LEDGER.md): source, support, and scope checks.
- [Student labs](labs/README.md): four notebooks using LangGraph, Gemini, and the OpenAI Agents SDK, with separate instructor solutions.
- [Current framework labs](labs/frameworks/README.md): three additional labs on LangGraph parallel workflows, LangChain middleware, and PydanticAI typed agents, checked 6 October 2026.
- [Validation notes](improvements/VALIDATION.md): offline execution evidence and remaining live API checks.

The dated research update remains in the companion decks and prior Word/PDF conspect. The current textbook develops all 13 topics in continuous prose, with worked examples, exercises, and a separate scholarly bibliography.

- [Instructor guide](teaching/INSTRUCTOR-GUIDE.md), [pilot schedule](teaching/PILOT-GUIDE.md), and [capstone rubric](teaching/CAPSTONE.md).
- [Evaluation runner](evaluation/README.md): offline fixtures and a separately enabled live Gemini path.
- [Implementation status](improvements/IMPLEMENTATION-STATUS.md): completed work and remaining classroom/live validation.
