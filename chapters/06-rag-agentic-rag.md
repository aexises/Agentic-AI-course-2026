# Retrieval and evidence-grounded answers

## Why retrieval belongs in the architecture

The equipment service maintains policies that can change independently of the language model. It also needs to explain which policy supports a recommendation. Retrieval supplies external records at inference time so the system can use current, attributable information. The original RAG work combines parametric language generation with nonparametric retrieval and evaluates particular trained models on knowledge-intensive tasks [@rag]. Modern applications use the term more broadly for systems that retrieve evidence before generating an answer.

Retrieval does not make an answer correct by construction. The corpus may be stale, the search may miss the relevant passage, the retrieved passage may be inapplicable, or the model may misread it. A useful RAG design preserves enough intermediate information to determine which of these failures occurred.

## Building the evidence collection

An ingestion pipeline acquires documents, extracts text, divides it into retrievable units, attaches metadata, and builds an index. Each step can change what the system is able to find. A PDF extractor may lose table structure. A chunk boundary may separate an exception from the rule it modifies. A document with no effective date may be hard to compare with a newer policy.

For the equipment case, every chunk should retain a stable identifier, source document, location within that document, and relevant version or date. A source ID identifies a record; it does not establish that the record is trustworthy. The application may also need ownership, access restrictions, and supersession information.

Chunk size is a tradeoff. A small chunk can isolate a precise statement but omit necessary context. A large chunk can preserve context but include unrelated rules and consume more input space. Overlap can preserve sentences across boundaries, but repeated text can occupy retrieval slots and inflate the apparent amount of independent evidence. Evaluate chunking with actual questions, including questions about exceptions and tables.

## Lexical and vector retrieval

Lexical retrieval matches words or terms. It is often valuable for exact identifiers such as C17 and policy codes. Vector retrieval maps queries and passages into numeric representations and ranks their similarity. A common similarity measure for nonzero vectors is cosine similarity:

$$
\operatorname{cos}(q,d)=\frac{q\cdot d}{\lVert q\rVert\lVert d\rVert}.
$$

The dot product measures alignment, while the denominator removes scale. A high similarity score means the vectors are close according to the representation; it is not the probability that the passage answers the question. Zero vectors require a defined implementation policy because the denominator would be zero.

A hybrid system combines lexical and vector evidence. One rank-based combination is to sum reciprocal rank terms from different retrievers, using a positive constant to moderate the influence of the top rank. The precise fusion choice is a design decision to evaluate. It is especially useful to retain an exact-identifier path rather than assume semantic similarity will preserve every alphanumeric distinction.

A reranker examines a smaller candidate set with a more expensive scoring process. It can improve ordering but cannot recover a document absent from the candidate set. This dependency is important when diagnosing poor results: changing the reranker will not repair an ingestion failure.

## Worked example: retrieval quality

Assume five policy passages are relevant to a teaching question. A retriever returns three passages, two of which are relevant. Precision at three is $2/3$; recall at three is $2/5$. Precision asks how much of the returned set is relevant. Recall asks how much of the relevant set was found. The same system can have high precision and low recall.

If the first relevant passage appears at rank three, reciprocal rank is $1/3$. Averaging reciprocal ranks across questions gives mean reciprocal rank. This measure emphasizes the first relevant result. It does not reward finding all clauses required for a multi-part policy answer.

Now suppose the answer needs both a general eligibility rule and its fieldwork exception. Retrieving only the general rule may produce an answer that is locally supported but incomplete. For this task, evaluate whether the evidence set covers all required claims, not merely whether one relevant passage appears early. Define relevance and required coverage before interpreting a score.

## From passages to supported claims

A generated answer should make claims that can be checked against the retrieved evidence. Suppose the model says, “Students may borrow C17 for five days [P4].” First check that P4 belongs to the supplied evidence set. Then inspect whether P4 actually states the five-day rule, whether it applies to students, and whether the policy is effective for the requested date.

Citation membership is a useful automated test, but it only establishes that an identifier is present. It does not establish entailment, scope, authority, or freshness. A stronger evaluation decomposes the answer into claims and asks what evidence supports each one. The level of checking should match the consequences of an incorrect claim.

Abstention should also have a clear meaning. “No supporting passage found” describes the retrieval outcome. “The policy does not exist” is a stronger claim about the corpus or institution and may not be justified. The user-facing answer should state the missing evidence and, where appropriate, identify the next action that could resolve it.

## Corrective retrieval as a state machine

A fixed RAG workflow retrieves once and answers. A corrective workflow evaluates whether the evidence is adequate, changes the query when justified, and retrieves again under a bound. Our teaching graph uses fields such as `query`, `evidence`, `repair_count`, and `status`. If the first evidence set is empty, it can attempt one repair. If the second attempt is still inadequate, it abstains.

A repair should target an identifiable retrieval problem. If the query uses an informal term such as “sound recorder,” a catalog synonym such as “audio recorder” may help. If the date is missing, rewriting the search query cannot resolve the user ambiguity. If the policy document was never indexed, repeatedly reformulating the query is also unlikely to help. Different missing-information causes require different transitions.

The graph should retain the original query, repaired query, evidence IDs, and stop reason. Without this trace, an apparent improvement could simply come from searching a broader corpus or consuming more calls. Compare against the one-pass baseline using the same task set and report the extra retrieval and generation work.

## Conflicts and authority

Suppose two passages disagree: an old handbook says a three-day limit; a newer approved policy says five days. A generic majority vote over chunks may favor the old rule if the handbook appears in several duplicate locations. The application needs a version and authority policy rather than a count of matching sentences.

If the metadata does not establish which source governs, the answer should present the conflict and avoid committing to an unsupported interpretation. A model's confidence does not create document authority. In the equipment case, unresolved policy conflict should block a reservation proposal that depends on eligibility and may require a coordinator's decision.

Retrieved content can also contain instructions aimed at the agent. Treat these as source text, not commands. Chapter 12 develops this threat model; for now, preserve the distinction between “the document contains this sentence” and “the application is authorized to obey it.”

## Graph-based retrieval and when it helps

Some questions ask about relationships across a corpus rather than one passage. A graph representation can connect entities, events, and claims. The GraphRAG work by Edge and colleagues studies graph-based query-focused summarization using extracted structure and community summaries [@graphrag]. This is a particular method; any application with a graph database is not automatically a reproduction of it.

For our service, a relationship graph might connect projects, required equipment, training certificates, and departments. It introduces new questions about extraction correctness, missing edges, update cost, and provenance of inferred relationships. Build a passage-retrieval baseline first. Use graph structure when the task requires relationships that the simpler representation fails to recover, and test those relationships directly.

## Exercises

1. A retriever returns five passages, three relevant, from a corpus with six relevant passages for the query. Compute precision and recall at five.
2. Describe a chunking failure that separates a rule from an exception. Propose a test that would reveal it.
3. Construct an answer with a valid citation ID but an unsupported claim. Explain which automated check would miss the error.
4. Implement one bounded query repair and an abstention path in Lab 6. Preserve both queries and evidence IDs in the trace.
5. Two conflicting documents have no effective dates. Write an appropriate answer and specify the evidence needed before committing a policy-dependent action.

## Further study and laboratory connection

Read [@rag] for the original retrieval/generation formulation and [@graphrag] for a different retrieval problem. Complete the repaired retrieval foundation before Lab 6. The lab's controlled corpus makes provenance and failure paths inspectable; its fixture results are not a claim about real-world retrieval quality.
