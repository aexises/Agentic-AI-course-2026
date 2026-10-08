# Course readiness for agentic AI engineering jobs

Reviewed 7–8 October 2026. This is a qualitative curriculum assessment, not a hiring-probability estimate or a representative labor-market survey. The comparison uses the MTS vacancy supplied by the user, LinkedIn employer postings, and employer career pages where accessible. Course evidence was inspected in the current checkout, including Labs 12–16.

**Conclusion:** passing the current course alone does not establish competitiveness for the sampled middle, senior, or staff roles. The course provides relevant agent/RAG implementation practice. An experienced Python/backend or ML engineer could use it as a transition into applied agent engineering; a beginner still needs software-engineering foundations, independent delivery, and evidence from realistic workloads. This judgment does not imply that every listed qualification is an absolute hiring cutoff.

**MTS comparison.** The supplied [Middle ML developer — AI agents HR MWS vacancy](https://job.mts.ru/vacancy/694191685193695543) was readable in the browser, with an application button. It lists 1–3 years of experience, Moscow, remote work, and a civil-law contract (ДГПХ). Remote is not confirmation of permission to work from any country. Duties span agent/RAG architecture, corporate-data and HR-system integration, inference efficiency, and evaluation. The following maps its technical requirements to inspected course evidence; readiness judgments are ours.

| Requirement area | Current course evidence | Judgment |
|---|---|---|
| Agent patterns and framework use | Chapters 2–5; Labs 3, 5, 9–12 | Relevant instruction and exercises; students must demonstrate independent implementation |
| RAG, indexing, fusion, reranking | Labs 6 and 12–14 | Strong topic alignment; pgvector is actually exercised |
| Tools connected to APIs/databases | Labs 5, 7, 12, 15–16 | Working teaching paths; existing enterprise integration remains unproven |
| LoRA/QLoRA | Chapter 2 distinguishes fine-tuning from prompting/retrieval | Missing practical training and adapter evaluation |
| FastAPI/Flask and Docker | FastAPI Lab 15; real database container; optional API Docker recipe | FastAPI practice exists; application-image delivery and deployment are not yet a verified graduation requirement |
| CI/CD and deployment | Chapter 13 discusses releases; Lab 16 includes operating work | No required end-to-end CI-to-deployment pipeline located |
| Quality, latency, inference cost | Evaluation runner, Labs 7/14, chapter 13 | Good methodology; live-provider and load/cost optimization evidence remains limited |
| Optional .NET/C# integration and AI coding tools | Not a dedicated assessed track | Optional targeted preparation, not a prerequisite for the entire course |

The listing names several vector databases and two web frameworks. It does not clearly demand expertise in every alternative. Our recommendation is to retain pgvector and FastAPI as the core implementations and assess architecture/portability reasoning. Adding Flask or another vector database would not close the larger delivery and fine-tuning gaps.

**Leading-company reference roles.** These are selected engineering comparators, not a ranking of companies. Experience figures refer to the kinds of experience specified in each posting, not years using a particular recent agent framework.

| Company and source | Advertised bar | Implication for the course |
|---|---|---|
| OpenAI — [API Agents, LinkedIn](https://www.linkedin.com/jobs/view/software-engineer-api-agents-at-openai-4447480154) | 7+ professional engineering years excluding internships; backend/distributed systems, safe execution, identity, operations | Agent libraries are only part of the role; a course cannot substitute for backend ownership |
| OpenAI — [Codex Core Agent, LinkedIn](https://www.linkedin.com/jobs/view/applied-ai-engineer-codex-core-agent-at-openai-4417170158), [employer page](https://openai.com/careers/applied-ai-engineer-codex-core-agent-san-francisco/) | Shipped ML/LLM products, Python, evaluation or fine-tuning or prompting, real failure analysis; no numerical experience minimum in the inspected description | Conceptually close to our evaluation teaching, but requires stronger evidence on real coding tasks and product outcomes |
| Anthropic — [Enterprise Tech, LinkedIn](https://www.linkedin.com/jobs/view/applied-ai-engineer-enterprise-tech-at-anthropic-4449784730), [employer page](https://job-boards.greenhouse.io/anthropic/jobs/5057647008) | 4+ technical-role years; production LLM work, MCP, evaluations, deployment, customer-facing engineering | Add delivery with users and architecture communication; framework exercises alone are insufficient |
| Google — [Agentic SDLC Foundations, LinkedIn](https://www.linkedin.com/jobs/view/staff-software-engineer-agentic-sdlc-foundations-at-google-4464861992) | Staff role: 8 software-development years, 5 in testing/launching and 5 in ML design/infrastructure; architecture and agent evaluation | Useful destination benchmark; not an appropriate immediate course-graduate standard |
| NVIDIA — [Local AI, Agents and Systems, LinkedIn](https://www.linkedin.com/jobs/view/senior-engineer-local-ai-agents-and-systems-at-nvidia-4471977308) | 10+ professional engineering years, including 3+ Staff/Lead Architect; Windows internals, isolation, GPU inference, C++/Python | A separate systems specialization; substantially outside this applied application course |

All five descriptions were readable when checked. Employer application pages were additionally readable for Codex Core Agent and Anthropic Enterprise Tech. A readable LinkedIn description is not independent confirmation that applications are still being accepted. NVIDIA's text guarantees acceptance only through at least 3 October; continued acceptance on 8 October was not confirmed. We did not submit applications or test application forms.

Two initially found Google roles (BigQuery Agentic AI and Cloud Security) redirected away from their LinkedIn details; the former's employer link also no longer returned the job detail. NVIDIA's Blueprints/NIM integration LinkedIn link explicitly redirected as expired. They were excluded from the primary table rather than represented as confirmed current openings. Indexed descriptions remain useful historical references, but they are weaker availability evidence.

This selected sample is weighted toward experienced hires. It does not establish that all agentic jobs require seniority, that no junior openings exist, or that these employers hire only these profiles. Eligibility, work authorization, and individualized application suitability were not assessed.

**The most consequential weakness is the meaning of “pass.”** The existing [capstone rubric](../teaching/CAPSTONE.md) permits a properly labeled fixture-only experiment to earn full marks. [Framework validation](../labs/frameworks/VALIDATION.md) verifies deterministic/scripted paths. The [RAG validation record](../labs/rag/VALIDATION.md) adds real neural models, SQL, and HTTP execution, but its corpus contains 17 invented documents; the development evaluation uses five questions. Optional Gemini generation and the API Docker image were not validated. These are sensible educational boundaries, but full course marks cannot be presented as evidence of live-agent quality or production readiness. Tests passing establishes the tested implementation behavior, not student mastery or employability.

The [evaluation runner](../evaluation/README.md) already supports explicit live runs and failure accounting. The [production chapter](../chapters/13-production-frontier.md) already discusses cost per success, latency distributions, caching, retries, release gates, and rollback. These subjects are partly present conceptually; the gap is making them required, observed engineering work.

**Proposed changes, in priority order.** These are curriculum recommendations, not changes already implemented and not employer-mandated numeric thresholds.

1. **Add a distinct professional assessment.** Keep an accessible offline course pass, and separately assess a live project with instructor-provided API access where necessary. Require an unseen evaluation set, raw traces, failed attempts, tool correctness, evidence support, latency distributions, and observed usage/cost. Compare against a simpler baseline; a defensible decision to reject the agent can pass.
2. **Extend Lab 16 into sustained service delivery.** Students own a Python package, build/run the application image, automate tests and a staging deployment, run migrations, inject a dependency failure, and demonstrate rollback. Evaluate behavior after changes over multiple review cycles. Hosting can be an instructor environment; public exposure is not necessary.
3. **Add LoRA/QLoRA practice for the MTS path.** Train a small adapter using a documented dataset and suitable compute, reload it, and compare base versus adapted behavior on held-out examples. Require memory/resource reporting and a judgment about whether prompting or retrieval was more appropriate. This is role-specific preparation; it is not a universal requirement for every agent job.
4. **Add enterprise tool integration and identity.** Connect to a separately running service with authorization, background work, duplicate-request handling, and audited effects. Exercise an actual MCP server/client. Use synthetic HR policies and a ticketing/workflow service for an MTS-oriented project; avoid needing personal employee data. Offer a .NET adapter as an elective.
5. **Make performance and operational measurement practical.** Instrument tool/model calls, test concurrent requests and timeouts, report p50/p95 and failure denominators, measure cost per successful task, and test cache invalidation. Students must show a measured tradeoff, including cases where an optimization fails.
6. **Require independent ownership.** Give an unfamiliar corpus or API change, require an implementation without copying the reference solution, review the design, and ask the student to diagnose a seeded failure. For experienced/top-company preparation, add an upstream contribution or a substantial real-user project and a written account of its outcomes.

**Suggested graduation distinction.** A course completion credential can truthfully mean that the student understands and implements the taught patterns. A stronger portfolio assessment should mean that an independent reviewer can reproduce the student's service, inspect live evidence, break a dependency, and verify recovery. Neither credential establishes years of professional experience or guarantees hiring success.

| Starting position | Defensible expectation |
|---|---|
| Beginner with limited programming experience | The course alone is insufficient; develop Python, SQL, HTTP, testing, debugging, and basic system design alongside it |
| Strong student completing independent exercises | Useful foundation for pursuing internships/junior applied-AI opportunities; this review has not measured placement outcomes |
| Existing Python/backend or ML engineer | Plausible transition curriculum for MTS-like application roles after closing specific gaps and demonstrating a deployed project |
| Experienced engineer targeting the sampled leading-company roles | Relevant specialization, supplemented by role-appropriate delivery, systems depth, research/evaluation work, or customer impact |

The highest-value next investment is a stronger evidence-based capstone plus targeted missing skills. Expanding the framework inventory alone is unlikely to change the readiness assessment.
