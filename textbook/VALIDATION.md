# Textbook validation

Checked on 2026-09-09. This report applies to the rewritten Markdown and LaTeX source edition, not the earlier compiled PDF or the separate notebook release.

## Content and evidence

The generated manifest records 13 chapters, 22,323 instructional words (including the preface and appendices), 65 chapter exercises, and 35 bibliography entries. The book includes worked examples, mathematical foundations, an end-to-end case study, and selected exercise answers. Word counts are a size measure, not a certification of teaching quality.

The evidence review used three passes: source identity and date/type; the passage supporting the cited claim; and the wording and limitations of the claim in the book. [Source checks](SOURCE-CHECKS.md) record the support and scope for each reference. This is not three independent replications of the research, and does not establish every explanatory sentence as an experimentally verified result. Research papers, engineering reports, and mutable API documentation are distinguished. Numerical case-study data are illustrative.

## Executed checks

Command: `python3 -m unittest discover -s tests -p test_textbook.py -v`.

Result: **22 tests passed**. The suite checks generated-output freshness, citation resolution, LaTeX input resolution, archive completeness, supported Markdown conversion, special-character escaping, and rejection of malformed or unsupported input. It checks the actual bounded-add Python example with valid boundaries, invalid types, very large integers, nonfinite values, and overflow. It also recalculates the worked probability, budget, cost, complexity, and selected-answer arithmetic.

The LaTeX ZIP contains the generated input files and compilation instructions. Its contents are checked against the source export. `git diff --check` passed. These checks provide source-level and executable-example evidence; they do not substitute for running a TeX compiler.

## Compilation and teaching limits

The LaTeX edition was **not compiled**, as requested. Page layout, line breaks, font availability, and compiler-specific behavior remain unverified. Use the commands in [the compilation guide](README.md); no bibliography processor is required.

No student pilot or measured learning-outcome study was performed. The textbook does not certify current model quality, API availability, or benchmark transfer to a classroom application. Live framework and provider behavior should be checked against the linked documentation when running the supplementary labs. The earlier Word/PDF files remain an archived conspect and do not contain this rewritten edition.
