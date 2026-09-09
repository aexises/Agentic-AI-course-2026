# Textbook source edition

The course is now written as a textbook, with a continuous equipment-service case, explanations, worked derivations, 65 chapter exercises, selected answers, and a 35-entry cited bibliography. The main narrative covers all thirteen course topics. Mathematical foundations and an end-to-end case provide additional support.

## Read or compile

Read [the complete Markdown book](../STUDYBOOK.md). For compilation, use [latex/main.tex](latex/main.tex), which includes the chapter and appendix files in the same directory tree.

```bash
cd textbook/latex
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

LuaLaTeX is an alternative. Run twice to resolve the table of contents and numbered citations. The document uses `book`, `geometry`, `fontspec`, Latin Modern fonts, `amsmath`, `amssymb`, `microtype`, `fvextra`, `xcolor`, `xurl`, and `hyperref`, normally available in a full TeX Live or MiKTeX installation. It does not use shell escape, external images, a custom commercial font, or a bibliography processor. On Overleaf, upload the LaTeX archive, choose `main.tex` as the main document, and select XeLaTeX or LuaLaTeX.

The ready-to-upload [LaTeX archive](agentic-ai-textbook-latex.zip) contains every required `.tex` input. Compilation and page-layout review were intentionally left to the user. The Word/PDF files elsewhere in the course are the earlier conspect, not this edition.

## Edit once, export both formats

The editable sources are `../chapters/*.md`, `preface.md`, `appendix-mathematics.md`, `appendix-case-study.md`, `selected-answers.md`, and `references.json`. Do not edit generated `.tex` files unless you intend to maintain a separate layout fork.

From the course root:

```bash
python3 scripts/build-textbook.py
python3 scripts/build-textbook.py --check
python3 -m unittest discover -s tests -p test_textbook.py
```

The builder requires Python 3.10 or newer and only the standard library. It does not invoke a model, use network access, or compile TeX. The compatibility entry point `node scripts/build-studybook.mjs` forwards to it. Slide sources are maintained separately and cannot regenerate the book from short slide sections.

Source syntax supports headings at levels 1–3, paragraphs, flat numbered/bulleted lists, bold spans, inline code, inline dollar math, display math on standalone double-dollar lines, and fenced `python`, `text`, or `bash` blocks. Use citation keys such as `[@react]` or `[@react; @rag]`. The builder resolves these to linked numbered references in the complete Markdown and `\cite` commands in LaTeX. Do not place citation syntax inside code examples. Unsupported tables, nested lists, block quotes, and unclosed recognized syntax fail rather than silently exporting an incorrect structure.

The current bibliography is generated as `thebibliography`, so compilation needs no BibTeX or Biber. [references.bib](references.bib) is also exported for reference managers; it is not loaded by `main.tex`. The JSON file is the source of truth. Personal author lists are abbreviated with “et al.” where appropriate; the source links provide full contributor lists. ArXiv years refer to initial preprints, not unverified publication venues. Mutable documentation uses the access year.

The old conspect and its generator are archived in `archive/conspect-2026-09-09/`. The notebooks and their instructor solutions remain supplementary implementation material. Selected textbook answers do not expose the notebook solution implementations.

## Evidence and limitations

[Source checks](SOURCE-CHECKS.md) record what each citation supports and what it does not. [Validation](VALIDATION.md) describes the source and code checks; [build manifest](build-manifest.json) records source hashes and content counts. Research claims are scoped to their sources. All equipment-service data and numerical examples are explicitly illustrative.
