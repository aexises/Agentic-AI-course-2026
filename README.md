# Agentic AI Course

## What is included

- [STUDYBOOK.md](STUDYBOOK.md) - the complete conspect in one file
- [EXAM-GUIDE.md](EXAM-GUIDE.md) - comparisons, diagrams, and high-value design rules
- [SOURCE-MAP.md](SOURCE-MAP.md) - one-to-one traceability from each supplied PDF
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

## Source policy

The factual content is derived only from the supplied course PDFs and the references already included in them. The material has been reorganized, clarified, and expanded as a learning resource without introducing external factual claims. Lecturer and institution identifiers were removed.

## Rebuild

The Markdown studybook and decks are generated from `presentations/src/course-data.mjs`.

```bash
node scripts/build-studybook.mjs
node presentations/src/build-decks.mjs
```
