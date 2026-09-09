# Source Map

The original course structure follows the supplied 13-PDF sequence listed below. The 9 September 2026 edition adds dated research readings, protocol corrections, and assessed engineering practice. It is no longer a PDF-only rebuild. Original source PDFs were not available in this checkout during this update; the new textbook is not certified against those absent PDFs.

The current textbook's canonical content is authored in `chapters/*.md`, with front matter and appendices in `textbook/`. Its bibliography and source checks are in [references.json](textbook/references.json) and [SOURCE-CHECKS.md](textbook/SOURCE-CHECKS.md). The chapter sequence below is a topic mapping to the original course, not a claim that the new prose was transcribed from those PDFs.

Presentation content remains in `presentations/src/course-data.mjs` and `course-update.mjs`. The decks and existing Word/PDF represent the earlier concise edition. Its Markdown and generator were archived in `textbook/archive/conspect-2026-09-09/`. The new build writes Markdown and LaTeX only, so lecture-slide rebuilding cannot overwrite the textbook. The original source-reference appendix is retained as historical reference material; the new textbook cites its own checked bibliography.

| # | Supplied source | Rebuilt chapter | Improved deck |
|---:|---|---|---|
| 01 | `01-introduction.pdf` | `chapters/01-introduction.md` | `output/presentations/01-introduction.pptx` |
| 02 | `02-llm-reasoning-engine.pdf` | `chapters/02-llm-reasoning-engine.md` | `output/presentations/02-llm-reasoning-engine.pptx` |
| 03 | `03-anatomy-react.pdf` | `chapters/03-anatomy-react.md` | `output/presentations/03-anatomy-react.pptx` |
| 04 | `04-design-patterns.pdf` | `chapters/04-design-patterns.md` | `output/presentations/04-design-patterns.pptx` |
| 05 | `05-tools-mcp.pdf` | `chapters/05-tools-mcp.md` | `output/presentations/05-tools-mcp.pptx` |
| 06 | `06-rag-agentic-rag.pdf` | `chapters/06-rag-agentic-rag.md` | `output/presentations/06-rag-agentic-rag.pptx` |
| 07 | `07-memory-context.pdf` | `chapters/07-memory-context.md` | `output/presentations/07-memory-context.pptx` |
| 08 | `08-multi-agent-systems.pdf` | `chapters/08-multi-agent-systems.md` | `output/presentations/08-multi-agent-systems.pptx` |
| 09 | `09-multi-agent-interop.pdf` | `chapters/09-multi-agent-interop.md` | `output/presentations/09-multi-agent-interop.pptx` |
| 10 | `10-reasoning-planning.pdf` | `chapters/10-reasoning-planning.md` | `output/presentations/10-reasoning-planning.pptx` |
| 11 | `11-evaluation-observability.pdf` | `chapters/11-evaluation-observability.md` | `output/presentations/11-evaluation-observability.pptx` |
| 12 | `12-safety-security.pdf` | `chapters/12-safety-security.md` | `output/presentations/12-safety-security.pptx` |
| 13 | `13-production-frontier.pdf` | `chapters/13-production-frontier.md` | `output/presentations/13-production-frontier.pptx` |

The complete reference slides were transcribed into `references/source-reference-appendix.md`. Lecturer and institution identifiers are absent from the rebuilt materials.

