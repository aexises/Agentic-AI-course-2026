# 06. RAG and Agentic RAG

> RAG grounds generation in controlled evidence; agentic RAG adds decisions about whether, what, and how to retrieve.

## Learning objectives

- Explain the classic RAG pipeline
- Tune chunking and retrieval
- Evaluate retrieval and generation separately
- Compare vector, agentic, and graph retrieval

## Core notes

### Retrieval addresses the limits of parametric memory

Knowledge stored in weights can be outdated, unavailable for private corpora, unreliable on rare facts, and difficult to verify. RAG fetches evidence at query time and includes it in context so generation can be grounded and cited.

- Domain accuracy comes from a controlled corpus.
- Freshness comes from updating the index.
- Traceability comes from source metadata and citations.
- Privacy requires access control before retrieval reaches the model.

### Classic RAG is an ingestion and query pipeline

Documents are loaded and normalized, split into chunks, embedded, and stored. At query time the question is embedded, relevant chunks are retrieved, the prompt is augmented, and the LLM generates an answer from that evidence.

- Loaders preserve metadata such as source, date, and permissions.
- Vector indexes support semantic nearest-neighbor search.
- The generated answer should cite the retrieved source.

### Chunking sets the ceiling for retrieval

Chunks must fit budgets without cutting away the relationships needed to answer. Fixed-size windows are a practical default; hierarchical or sentence strategies fit structured or precise material. Overlap reduces boundary loss at additional index cost.

- Too-small chunks lose context.
- Too-large chunks dilute relevance.
- Answers spanning boundaries may require overlap or parent-child retrieval.
- Metadata captured during loading enables filters.

### Naive top-k retrieval is only a baseline

Semantic similarity can miss exact terms and return redundant or weak evidence. Hybrid search combines vector and lexical retrieval; reranking improves precision; query transformation, expansion, multi-query, and HyDE improve recall.

- Top-k trades missed evidence against context dilution.
- Filter permissions before semantic ranking.
- Rerank a candidate set rather than the whole corpus.

### Evaluate the retriever and generator separately

Retrieval metrics such as recall, precision, and MRR ask whether relevant evidence was fetched. Generation metrics ask whether the answer is relevant and faithful to that evidence. Diagnosing the two stages separately prevents prompt changes from hiding retrieval failures.

- Faithfulness directly measures unsupported claims.
- Citations make human verification possible.
- Production evaluation should include freshness and permission behavior.

### Agentic and graph retrieval solve different hard cases

Agentic RAG lets the model decide whether to retrieve, rewrite or decompose queries, grade evidence, and retrieve again. GraphRAG extracts entities and relationships and retrieves connected subgraphs, which helps multi-hop questions and hidden connections.

- Self-RAG decides and critiques retrieval.
- Corrective RAG grades evidence and uses a fallback when weak.
- Vector RAG finds semantically relevant text.
- GraphRAG follows relationships at higher build cost.

## Exam-ready summary

- RAG provides fresh, private, and citable evidence.
- Chunking and retrieval quality determine the maximum answer quality.
- Measure retrieval and generation as separate systems.
- Agentic RAG controls retrieval; GraphRAG retrieves relationships.

## Self-test

1. Describe the RAG pipeline from ingestion to answer.
2. How do chunk size and overlap affect retrieval?
3. Why can top-k retrieval dilute an answer?
4. Compare hybrid search, reranking, and query transformation.
5. What is faithfulness and why is it important?
6. When is GraphRAG preferable to vector RAG?

## Source basis

This chapter reorganizes and explains material from `06-rag-agentic-rag.pdf`. It adds study structure and design implications, but introduces no external factual sources.
