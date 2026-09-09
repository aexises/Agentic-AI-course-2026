import { applyCourseUpdate } from "./course-update.mjs";

export const course = {
  title: "Agentic AI",
  subtitle: "From language models to reliable autonomous systems",
  sourcePolicy:
    "Derived only from the 13 supplied course presentations and their embedded references.",
  chapters: [
    {
      id: 1,
      slug: "introduction",
      title: "From Language Models to Agents",
      thesis:
        "Agency appears when an LLM is placed inside a bounded loop with tools, memory, and control logic.",
      objectives: [
        "Define classical and LLM-based agents",
        "Distinguish chatbots, workflows, and agents",
        "Explain the perceive-reason-act loop",
        "Choose the least autonomy that solves a task",
      ],
      sections: [
        {
          title: "The composition changed, not the model paradigm",
          explanation:
            "A classifier maps text to a label and a chatbot maps conversation to a reply. An agent maps a goal to a sequence of actions in an environment and chooses those actions as the task unfolds. The practical shift is the composition LLM + tools + loop + memory.",
          bullets: [
            "Instruction following and function calling make outputs executable.",
            "Explicit reasoning helps choose and order actions.",
            "Context and retrieval carry task state and external evidence.",
          ],
        },
        {
          title: "Classical agency still supplies the core definition",
          explanation:
            "An agent perceives an environment through sensors and acts through actuators. A rational agent selects actions expected to maximize a performance measure given its percepts and knowledge. LLM agents replace a hand-written or learned policy with in-context natural-language reasoning.",
          bullets: [
            "Properties: autonomy, reactivity, pro-activeness, social ability.",
            "Hard environments are partially observable, stochastic, dynamic, and sequential.",
            "LLM agents gain generality but inherit reliability, cost, and evaluation problems.",
          ],
        },
        {
          title: "Four components recur in every implementation",
          explanation:
            "The profile defines identity, constraints, tools, and output protocol. Memory supplies short- and long-term state. Planning turns goals into steps. Action exposes controlled effects through tools. Frameworks mainly differ in how they wire and persist these parts.",
          bullets: [
            "Profile is the behavioral contract.",
            "Memory is information re-supplied to a stateless model.",
            "Planning selects the next step or an explicit plan.",
            "Action is mediated by a validating runtime.",
          ],
        },
        {
          title: "Agency is a loop, not a single forward pass",
          explanation:
            "The agent observes the goal and environment, reasons about the next step, acts through a tool, receives a new observation, and repeats until completion or a budget limit. The loop turns model output into state-changing behavior.",
          bullets: [
            "Observe: user goal, tool results, environment state.",
            "Reason: choose the next action from current evidence.",
            "Act: request a tool call through the runtime.",
            "Stop: final answer, step cap, cost cap, time cap, or human escalation.",
          ],
        },
        {
          title: "Control flow separates chatbots, workflows, and agents",
          explanation:
            "A chatbot produces a reply without actions. A workflow follows code-defined paths that may contain LLM calls and tools. An agent lets the model dynamically direct process and tool use. This is a spectrum rather than a binary label.",
          bullets: [
            "Workflows are more predictable, testable, and economical.",
            "Agents are more flexible when the correct path cannot be written in advance.",
            "Moving toward autonomy raises variance, latency, cost, and safety surface.",
          ],
        },
        {
          title: "The engineering rule is minimum sufficient autonomy",
          explanation:
            "Start with a single call or fixed workflow and add model-directed decisions only when the task requires them. Narrow scope, explicit evaluation, and human checkpoints are more reliable than an open-ended agent that can do anything.",
          bullets: [
            "Use execution-grounded tasks where success can be checked.",
            "Bound long horizons because errors compound.",
            "Treat the production agent as a stack: model, tools, state, orchestration, eval, and guardrails.",
          ],
        },
      ],
      takeaways: [
        "Agent = LLM reasoning core + tools + loop + memory.",
        "Profile, memory, planning, and action are the reusable anatomy.",
        "Autonomy is a design variable; choose the leftmost workable point.",
        "Reliability comes from the system around the model.",
      ],
      examQuestions: [
        "Give the classical definition of an agent and reframe it for an LLM system.",
        "Why is an agent a composition rather than a new model paradigm?",
        "Compare chatbot, workflow, and agent by control flow and tool use.",
        "Name the four agent components and the responsibility of each.",
        "Why are typical LLM-agent environments difficult?",
        "Explain the principle of minimum sufficient autonomy.",
      ],
      source: "01-introduction.pdf",
    },
    {
      id: 2,
      slug: "llm-reasoning-engine",
      title: "The LLM as a Reasoning Engine",
      thesis:
        "Agents inherit the stochastic, token-based nature of LLMs; prompting, structured output, retrieval, and adaptation compensate for different limitations.",
      objectives: [
        "Explain next-token prediction and sampling",
        "Use major prompting strategies appropriately",
        "Distinguish prompting, RAG, and fine-tuning",
        "Design machine-readable outputs for control loops",
      ],
      sections: [
        {
          title: "The engine predicts one token at a time",
          explanation:
            "An autoregressive LLM defines a probability distribution for the next token given previous tokens, samples one, appends it, and repeats. This makes agent behavior stochastic, gives the model no built-in persistent state, and represents plans, actions, and observations as tokens.",
          bullets: [
            "Low temperature favors predictable control-loop behavior.",
            "Top-p limits sampling to a probability-mass nucleus.",
            "Input and output tokens both affect latency and cost.",
          ],
        },
        {
          title: "The context window is a shared budget",
          explanation:
            "System instructions, tool definitions, retrieved evidence, memory, conversation, and generated reasoning all compete for a fixed window. Agent loops resend a growing transcript, so relevance and compression matter.",
          bullets: [
            "Long contexts cost more and take longer.",
            "Evidence in the middle may be underused.",
            "The cheapest token is the one the system does not send.",
          ],
        },
        {
          title: "The prompt programs behavior in context",
          explanation:
            "In-context learning teaches a task through instructions and examples without changing model weights. A robust prompt separates instruction, context, input, and output indicator; an agent profile also includes tool contracts and the protocol the harness parses.",
          bullets: [
            "Zero-shot is fast but can be brittle on edge cases.",
            "Few-shot demonstrations stabilize task pattern and format.",
            "Clear output examples reduce parse failures.",
          ],
        },
        {
          title: "Different reasoning techniques buy different guarantees",
          explanation:
            "Chain-of-thought externalizes intermediate steps. Self-consistency samples several chains and votes. Program-aided language models generate code and delegate exact computation to an interpreter. Reasoning models spend additional test-time compute on difficult problems.",
          bullets: [
            "Compare direct answers and reasoning prompts on the target task.",
            "Test voting against a baseline with a declared call budget.",
            "Use executable programs when exact computation matters.",
            "Pay for deliberate reasoning only on hard steps.",
          ],
        },
        {
          title: "Structured output closes the software loop",
          explanation:
            "Structured-output support varies by provider, model, and schema. Native function calling supplies a protocol for tool requests. The application must validate arguments, check policy, and handle invalid or incomplete responses.",
          bullets: [
            "Schema validity is not semantic correctness.",
            "Tool descriptions steer selection and argument filling.",
            "The model requests; application code executes.",
          ],
        },
        {
          title: "Prompting, retrieval, and fine-tuning solve different problems",
          explanation:
            "Prompting changes behavior quickly. RAG injects current or private knowledge at query time. Fine-tuning changes model behavior in weights; LoRA learns small low-rank adapters and QLoRA combines adapters with a quantized base. Alignment methods such as SFT, RLHF, and DPO target preferred behavior.",
          bullets: [
            "Choose prompting for format, role, or rapidly changing behavior.",
            "Choose RAG for fresh, private, or citable knowledge.",
            "Choose fine-tuning for stable behavior at sufficient scale.",
            "Ground hallucination; do not expect prompting alone to remove it.",
          ],
        },
      ],
      takeaways: [
        "An LLM is stochastic and stateless; the agent harness supplies control and state.",
        "Prompt structure and examples are the cheapest adaptation lever.",
        "Structured output and function calling make generations programmable.",
        "Prompting, RAG, and fine-tuning are complements, not substitutes.",
      ],
      examQuestions: [
        "How do temperature and top-p affect an agent loop?",
        "What competes for space in the context window?",
        "Compare zero-shot, few-shot, chain-of-thought, self-consistency, and PAL.",
        "Why is valid JSON insufficient as a security guarantee?",
        "When should an engineer choose RAG rather than fine-tuning?",
        "What do LoRA and QLoRA change about fine-tuning economics?",
      ],
      source: "02-llm-reasoning-engine.pdf",
    },
    {
      id: 3,
      slug: "anatomy-react",
      title: "Agent Anatomy and ReAct",
      thesis:
        "ReAct operationalizes agency as a bounded Thought-Action-Observation cycle whose evidence comes from the runtime, not the model.",
      objectives: [
        "Engineer the four agent components",
        "Trace a ReAct episode",
        "Implement safe parsing and termination",
        "Recognize horizon and format failures",
      ],
      sections: [
        {
          title: "The profile is an executable contract",
          explanation:
            "The system prompt defines role, objective, tool menu, output protocol, constraints, stopping behavior, and escalation. It should read like a precise specification for a careful colleague, with examples where the protocol is easy to misunderstand.",
          bullets: [
            "State success before listing implementation details.",
            "Give each tool a description and example call.",
            "Specify an exact output protocol and stopping condition.",
            "Add guardrails and human escalation rules.",
          ],
        },
        {
          title: "Memory turns a stateless model into a stateful system",
          explanation:
            "Short-term memory is the running context; long-term memory is an external store read and written through tools. The transcript is the immediate state of ReAct because each next decision depends on prior actions and observations.",
          bullets: [
            "The application or provider must carry the bounded conversation state.",
            "Long-term memory is scalable but requires explicit retrieval.",
            "Only re-supplied information can influence the next model call.",
          ],
        },
        {
          title: "Planning ranges from next-step choice to search",
          explanation:
            "Decomposition creates subgoals, reasoning chooses actions, reflection critiques progress, and search explores alternatives. ReAct uses the simplest planner: decide only the next action from current evidence.",
          bullets: [
            "Reactive planning adapts quickly to observations.",
            "One-step lookahead is efficient but myopic.",
            "Reflection and plan-and-execute address longer horizons.",
          ],
        },
        {
          title: "The runtime owns the action boundary",
          explanation:
            "The model proposes a tool and arguments. The runtime parses or receives the structured call, validates types and policy, authorizes it, executes the tool, and appends the real result as an observation. The model must never fabricate the observation.",
          bullets: [
            "Use supported stop sequences as format controls in text protocols.",
            "Prefer native tool calling in production when available.",
            "Sandbox, scope permissions, and confirm consequential actions.",
          ],
        },
        {
          title: "ReAct interleaves deliberation and grounding",
          explanation:
            "Each iteration contains a Thought from the model, an Action from the model, and an Observation from the environment. Acting grounds later reasoning in evidence, while reasoning improves tool selection compared with an act-only policy.",
          bullets: [
            "Thought chooses the next step.",
            "Action names and parameterizes a tool.",
            "Observation records the runtime result.",
            "Final Answer ends the episode.",
          ],
        },
        {
          title: "A correct loop is bounded and observable",
          explanation:
            "Termination must include a final-answer condition plus hard step, token, cost, or time budgets. The trace should be captured so evaluators can inspect tool choice, observations, errors, efficiency, and whether the final claim is grounded.",
          bullets: [
            "Common failures: format drift, greedy parsing, fabricated observations.",
            "Long horizons compound errors and can make the agent lose the goal.",
            "No backtracking means a bad line may persist.",
            "Native schemas reduce format drift but not reasoning errors.",
          ],
        },
      ],
      takeaways: [
        "The model proposes actions; the runtime validates and executes.",
        "ReAct alternates Thought, Action, and real Observation.",
        "Validate the complete protocol and enforce runtime budgets.",
        "Tracing reveals both outcome and trajectory failures.",
      ],
      examQuestions: [
        "What belongs in a robust agent profile?",
        "Who produces each part of Thought-Action-Observation?",
        "What can a supported stop sequence prevent, and what must the runtime still check?",
        "Compare text parsing with native function calling.",
        "List the required termination conditions for a safe loop.",
        "Why does ReAct reduce hallucination yet remain myopic?",
      ],
      source: "03-anatomy-react.pdf",
    },
    {
      id: 4,
      slug: "design-patterns",
      title: "Agentic Design Patterns",
      thesis:
        "The best architecture keeps control in code when possible and hands decisions to models only where dynamic judgment adds value.",
      objectives: [
        "Recognize five workflow patterns",
        "Compare workflow and agentic control",
        "Compose patterns into a system",
        "Estimate reliability and cost trade-offs",
      ],
      sections: [
        {
          title: "The augmented LLM is the reusable building block",
          explanation:
            "Retrieval, tools, and memory turn a plain model call into an augmented LLM. Design patterns connect one or more augmented LLMs with control flow. The central design question is whether code or the model decides what happens next.",
          bullets: [
            "Code-directed workflows are predictable and testable.",
            "Model-directed agents are flexible but variable.",
            "Add autonomy only when decisions cannot be enumerated reliably.",
          ],
        },
        {
          title: "Chaining and routing encode known structure",
          explanation:
            "Prompt chaining applies fixed ordered steps and can place validation gates between them. Routing classifies an input and selects a specialized handler. Both retain explicit control paths.",
          bullets: [
            "Chaining fits outline-draft-polish style sequences.",
            "Gates can check schema, rules, or quality.",
            "Routing needs calibrated accuracy and a fallback lane.",
            "Hard or low-confidence cases can escalate.",
          ],
        },
        {
          title: "Parallelization trades compute for speed or reliability",
          explanation:
            "Sectioning divides independent work and aggregates results, reducing wall-clock time. Voting runs the same task several times and aggregates answers, increasing cost in exchange for robustness.",
          bullets: [
            "Parallelize only independent subtasks.",
            "Aggregation is a distinct step that can fail.",
            "Reserve voting for decisions where redundancy is worth the cost.",
          ],
        },
        {
          title: "Orchestrator-workers creates subtasks dynamically",
          explanation:
            "An orchestrator decomposes the current input, dispatches variable subtasks to workers, and synthesizes their outputs. Unlike a chain, the exact work plan is not known in advance.",
          bullets: [
            "Workers may be prompts, tools, or complete agents.",
            "The orchestrator must track state and integrate results.",
            "Dynamic decomposition increases flexibility and evaluation burden.",
          ],
        },
        {
          title: "Evaluator-optimizer and reflection require grounded criteria",
          explanation:
            "A generator produces an attempt, an evaluator checks it, and feedback drives revision. The loop improves reliably when criteria are externally verifiable, such as tests, schemas, calculations, rubrics, or reference answers.",
          bullets: [
            "Vague 'is this good?' critics may rubber-stamp outputs.",
            "Tool-grounded critics can verify objective properties.",
            "Every refinement loop needs a stop and cost budget.",
          ],
        },
        {
          title: "Patterns compose, so failure controls must compose too",
          explanation:
            "A router can select an agent, an orchestrator can dispatch ReAct workers, and an evaluator can check the synthesis. Humans can approve, correct, or receive escalations at consequential boundaries.",
          bullets: [
            "Anti-patterns: agent where workflow suffices, too many tools, unbounded loops.",
            "Each additional model call increases cost and failure opportunity.",
            "Use the simplest pattern whose control assumptions match the task.",
          ],
        },
      ],
      takeaways: [
        "Patterns connect augmented LLMs with different control structures.",
        "Chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer are workflows.",
        "Tool use, reflection, planning, and multi-agent systems hand more control to models.",
        "Ground checks and budgets at every loop boundary.",
      ],
      examQuestions: [
        "What distinguishes a workflow from an agent?",
        "Compare prompt chaining and orchestrator-workers.",
        "Name the two forms of parallelization and their goals.",
        "Why do evaluator-optimizer loops need verifiable criteria?",
        "Give a valid composition of three patterns.",
        "List four common agentic anti-patterns.",
      ],
      source: "04-design-patterns.pdf",
    },
    {
      id: 5,
      slug: "tools-mcp",
      title: "Tool Use, MCP, and Frameworks",
      thesis:
        "Tools are typed prompts at a security boundary; MCP standardizes their integration, while frameworks organize control and state.",
      objectives: [
        "Design reliable tool schemas",
        "Explain the model-runtime-tool cycle",
        "Describe MCP primitives and transports",
        "Choose raw APIs or a framework",
      ],
      sections: [
        {
          title: "A tool is a typed contract, not direct model access",
          explanation:
            "A tool definition names an operation, explains when to use it, and defines typed parameters. The model emits a name and arguments; the runtime validates, authorizes, executes, and returns the result to context.",
          bullets: [
            "The model never directly touches the external API.",
            "Schema validity must be followed by policy validation.",
            "Tool results are untrusted inputs to the next model step.",
          ],
        },
        {
          title: "Tool descriptions are prompts",
          explanation:
            "Models select and fill tools from their specifications, so names, descriptions, examples, parameter types, and error messages directly affect behavior. Good granularity avoids both excessive micro-calls and confusing mega-tools.",
          bullets: [
            "Prefer minimal parameters and enums over unconstrained text.",
            "Return actionable errors rather than stack traces.",
            "Make retry-prone operations idempotent.",
            "Gate destructive or irreversible actions.",
          ],
        },
        {
          title: "The runtime is the security boundary",
          explanation:
            "Model-generated arguments must be treated as attacker-controlled input. Runtime controls include sanitization, least-privilege credentials, read-only defaults, sandboxing, rate limits, audit logs, and confirmation.",
          bullets: [
            "Do not execute raw model strings with unsafe evaluators.",
            "Restrict filesystem and network scopes.",
            "Separate proposing an action from authorizing it.",
          ],
        },
        {
          title: "MCP replaces bespoke N-by-M integration",
          explanation:
            "Without a standard, every agent must be wired separately to every tool. The Model Context Protocol provides a shared JSON-RPC interface so hosts can connect to reusable servers, changing integration growth from N multiplied by M toward N plus M.",
          bullets: [
            "Tools expose actions with possible side effects.",
            "Resources expose read-only context.",
            "Prompts expose reusable interaction templates.",
          ],
        },
        {
          title: "MCP capabilities depend on the selected version",
          explanation:
            "For the MCP 2025-11-25 baseline, servers expose tools, resources, and prompts. Clients can support sampling, roots, and elicitation. This edition discusses stdio and Streamable HTTP and requires implementations to enforce access controls.",
          bullets: [
            "Sampling lets a server request host-model generation.",
            "Roots advertise filesystem context. Implementations enforce access.",
            "Elicitation asks the user for input during a task.",
            "Transport choice changes deployment and trust assumptions.",
          ],
        },
        {
          title: "Frameworks package orchestration, not understanding",
          explanation:
            "Frameworks provide loops or state graphs, persistence, streaming, tool integration, observability, memory, and human-in-the-loop hooks. Raw APIs suit simple or highly controlled agents; frameworks help when state and coordination become first-class.",
          bullets: [
            "LangGraph represents nodes, edges, conditional control, and shared state.",
            "Crew-style systems emphasize role-based multi-agent work.",
            "Understand prompts and boundaries before adding framework abstraction.",
            "MCP standardizes tools; A2A standardizes agent-to-agent collaboration.",
          ],
        },
      ],
      takeaways: [
        "A model requests a tool call; a runtime decides whether to execute it.",
        "Tool ergonomics strongly influence model reliability.",
        "MCP standardizes reusable tools, resources, and prompts.",
        "Frameworks are justified by stateful orchestration needs.",
      ],
      examQuestions: [
        "Walk through the complete function-call cycle.",
        "What makes a tool specification model-friendly?",
        "Why must tool results be treated as untrusted?",
        "Explain the N-by-M problem and MCP's answer.",
        "List server-side and client-side MCP primitives.",
        "When is a framework preferable to a raw model API?",
      ],
      source: "05-tools-mcp.pdf",
    },
    {
      id: 6,
      slug: "rag-agentic-rag",
      title: "RAG and Agentic RAG",
      thesis:
        "RAG grounds generation in controlled evidence; agentic RAG adds decisions about whether, what, and how to retrieve.",
      objectives: [
        "Explain the classic RAG pipeline",
        "Tune chunking and retrieval",
        "Evaluate retrieval and generation separately",
        "Compare vector, agentic, and graph retrieval",
      ],
      sections: [
        {
          title: "Retrieval addresses the limits of parametric memory",
          explanation:
            "Knowledge stored in weights can be outdated, unavailable for private corpora, unreliable on rare facts, and difficult to verify. RAG fetches evidence at query time and includes it in context so generation can be grounded and cited.",
          bullets: [
            "Domain accuracy comes from a controlled corpus.",
            "Freshness comes from updating the index.",
            "Traceability comes from source metadata and citations.",
            "Privacy requires access control before retrieval reaches the model.",
          ],
        },
        {
          title: "Classic RAG is an ingestion and query pipeline",
          explanation:
            "Documents are loaded and normalized, split into chunks, embedded, and stored. At query time the question is embedded, relevant chunks are retrieved, the prompt is augmented, and the LLM generates an answer from that evidence.",
          bullets: [
            "Loaders preserve metadata such as source, date, and permissions.",
            "Vector indexes support semantic nearest-neighbor search.",
            "The generated answer should cite the retrieved source.",
          ],
        },
        {
          title: "Chunking sets the ceiling for retrieval",
          explanation:
            "Chunks must fit budgets without cutting away the relationships needed to answer. Fixed-size windows are a practical default; hierarchical or sentence strategies fit structured or precise material. Overlap reduces boundary loss at additional index cost.",
          bullets: [
            "Too-small chunks lose context.",
            "Too-large chunks dilute relevance.",
            "Answers spanning boundaries may require overlap or parent-child retrieval.",
            "Metadata captured during loading enables filters.",
          ],
        },
        {
          title: "Naive top-k retrieval is only a baseline",
          explanation:
            "Semantic similarity can miss exact terms and return redundant or weak evidence. Hybrid search combines vector and lexical retrieval; reranking improves precision; query transformation, expansion, multi-query, and HyDE improve recall.",
          bullets: [
            "Top-k trades missed evidence against context dilution.",
            "Filter permissions before semantic ranking.",
            "Rerank a candidate set rather than the whole corpus.",
          ],
        },
        {
          title: "Evaluate the retriever and generator separately",
          explanation:
            "Retrieval metrics such as recall, precision, and MRR ask whether relevant evidence was fetched. Generation metrics ask whether the answer is relevant and faithful to that evidence. Diagnosing the two stages separately prevents prompt changes from hiding retrieval failures.",
          bullets: [
            "Faithfulness directly measures unsupported claims.",
            "Citations make human verification possible.",
            "Production evaluation should include freshness and permission behavior.",
          ],
        },
        {
          title: "Agentic and graph retrieval solve different hard cases",
          explanation:
            "Agentic RAG lets the model decide whether to retrieve, rewrite or decompose queries, grade evidence, and retrieve again. GraphRAG extracts entities and relationships and retrieves connected subgraphs, which helps multi-hop questions and hidden connections.",
          bullets: [
            "Self-RAG decides and critiques retrieval.",
            "Corrective RAG grades evidence and uses a fallback when weak.",
            "Vector RAG finds semantically relevant text.",
            "GraphRAG follows relationships at higher build cost.",
          ],
        },
      ],
      takeaways: [
        "RAG provides fresh, private, and citable evidence.",
        "Chunking and retrieval quality determine the maximum answer quality.",
        "Measure retrieval and generation as separate systems.",
        "Agentic RAG controls retrieval; GraphRAG retrieves relationships.",
      ],
      examQuestions: [
        "Describe the RAG pipeline from ingestion to answer.",
        "How do chunk size and overlap affect retrieval?",
        "Why can top-k retrieval dilute an answer?",
        "Compare hybrid search, reranking, and query transformation.",
        "What is faithfulness and why is it important?",
        "When is GraphRAG preferable to vector RAG?",
      ],
      source: "06-rag-agentic-rag.pdf",
    },
    {
      id: 7,
      slug: "memory-context",
      title: "Memory, State, and Context Engineering",
      thesis:
        "Memory is an engineered system that curates a bounded context, persists selected experience, and governs recall, expiry, and access.",
      objectives: [
        "Classify agent memory",
        "Manage short-term context",
        "Design deliberate long-term writes and reads",
        "Evaluate memory quality and governance",
      ],
      sections: [
        {
          title: "Stateless models require explicit state engineering",
          explanation:
            "An LLM knows only the current context. Long tasks and multiple sessions therefore need a system that decides what stays in the window, what moves to external storage, and what is retrieved later.",
          bullets: [
            "The context is bounded, costly, and imperfectly used.",
            "Nothing persists across calls unless the application stores it.",
            "Memory architecture is a set of selection policies.",
          ],
        },
        {
          title: "Short-term and long-term memory have different mechanics",
          explanation:
            "Short-term memory is working context: instructions, tools, evidence, and recent trace. Long-term memory is external and can hold episodic events, semantic facts, and procedural knowledge across sessions.",
          bullets: [
            "Episodic: past interactions and outcomes.",
            "Semantic: facts and stable preferences.",
            "Procedural: instructions or learned methods.",
            "Long-term storage is useful only if recall is selective.",
          ],
        },
        {
          title: "Short-term memory must be actively compressed",
          explanation:
            "Truncation drops old turns, summaries compress them, selective recall retrieves only relevant history, and a structured scratchpad keeps the plan and current state visible. These mechanisms can be combined.",
          bullets: [
            "Rolling summaries preserve gist but may drift.",
            "Recent detail can remain verbatim.",
            "Conversation retrieval is RAG over history.",
            "A scratchpad reduces repeated reasoning and goal loss.",
          ],
        },
        {
          title: "Long-term memory needs write and read policies",
          explanation:
            "Store durable signal rather than every event. Writes can occur on explicit request, at task completion, through reflection, or continuously for changing state. Reads can use keys, recency, or semantic similarity.",
          bullets: [
            "Prefer stable preferences, durable facts, outcomes, and lessons.",
            "Deduplicate and resolve contradictions.",
            "Attach timestamps, provenance, and expiry.",
            "Reflective consolidation turns noisy episodes into higher-level memories.",
          ],
        },
        {
          title: "Context engineering treats tokens as scarce capacity",
          explanation:
            "More context is not automatically better. Low-relevance history raises cost and latency and can create context rot. Long-context models provide more room but do not create cross-session persistence, selective recall, consent, or governance.",
          bullets: [
            "Relevance beats volume.",
            "Place critical instructions and evidence deliberately.",
            "Virtual-context architectures page information between window and store.",
            "Retrieval-based architectures recall memories by relevance.",
          ],
        },
        {
          title: "Memory is also a privacy and security system",
          explanation:
            "Persistent data requires consent, minimization, retention limits, deletion, and access control. Memory can become stale, contradictory, poisoned, or unbounded, so it needs evaluation and maintenance.",
          bullets: [
            "Recall: retrieve the right memory at the right time.",
            "Faithfulness: use the memory correctly.",
            "Forgetting: expire stale or irrelevant items.",
            "Security: prevent unauthorized access and malicious persistence.",
          ],
        },
      ],
      takeaways: [
        "Memory is context plus external stores and policies.",
        "Short-term memory is curated; long-term memory is deliberate.",
        "Long context complements but does not replace memory.",
        "Recall, consolidation, expiry, consent, and access control are first-class.",
      ],
      examQuestions: [
        "Why does an LLM need an application-level memory system?",
        "Compare episodic, semantic, and procedural memory.",
        "What are four ways to manage a full context window?",
        "When should an agent write a long-term memory?",
        "Why does a million-token context not eliminate memory architecture?",
        "How should memory be evaluated and governed?",
      ],
      source: "07-memory-context.pdf",
    },
    {
      id: 8,
      slug: "multi-agent-systems",
      title: "Multi-Agent Systems",
      thesis:
        "Multiple agents add specialization, modularity, parallelism, and context division only when coordination costs are explicitly designed.",
      objectives: [
        "Decide when multiple agents help",
        "Design roles, communication, and coordination",
        "Compare centralized, decentralized, and hierarchical topologies",
        "Bound multi-agent cost and termination",
      ],
      sections: [
        {
          title: "More agents are useful only for separable work",
          explanation:
            "A focused role, prompt, tool set, and context can outperform one overloaded agent. Multiple agents also allow modular testing, parallel tasks, and divided context. These gains disappear when work is tightly coupled or one well-equipped agent already succeeds.",
          bullets: [
            "Specialization narrows behavior and tool choice.",
            "Modularity makes agents independently replaceable.",
            "Parallelism reduces time only for independent subtasks.",
            "Context division keeps each working set relevant.",
          ],
        },
        {
          title: "Coordination is the price of specialization",
          explanation:
            "Each agent adds model calls and communication. Errors can propagate through handoffs, disagreement needs resolution, and someone must decide when the team is done. Multi-agent designs are harder to trace and secure.",
          bullets: [
            "Cost grows with agents, turns, and coordination rounds.",
            "Messages consume context and can carry errors or injections.",
            "Termination needs shared budgets and a clear owner.",
            "Start with a single agent and add roles for measured reasons.",
          ],
        },
        {
          title: "Design collaboration along four dimensions",
          explanation:
            "Roles define responsibility; communication defines information exchange; coordination selects the next actor and completion rule; evolution determines whether agents adapt through feedback or reflection.",
          bullets: [
            "Give roles distinct objectives and tool scopes.",
            "Choose shared state or explicit messages deliberately.",
            "Define handoff contracts and synthesis ownership.",
            "Keep adaptation separate from uncontrolled drift.",
          ],
        },
        {
          title: "A runtime supplies identity, lifecycle, and delivery",
          explanation:
            "The application sits on a runtime that creates and retires agent instances, uniquely addresses them, and routes messages. Standalone runtimes are simpler; distributed runtimes add process, machine, language, isolation, and operations concerns.",
          bullets: [
            "Use one process for development and simple applications.",
            "Distribute only for scale, isolation, or polyglot requirements.",
            "Persist state intentionally across instance lifecycles.",
          ],
        },
        {
          title: "Communication can be shared-state or message-based",
          explanation:
            "A blackboard lets agents read and update common state. Direct messaging targets a specific agent. Publish-subscribe decouples publishers from subscribers through topics. Topic scope is also a security boundary.",
          bullets: [
            "Shared state simplifies synthesis but can create coupling.",
            "Direct messaging makes ownership explicit.",
            "Pub-sub supports fan-out and looser coupling.",
            "Partition topics by user, session, or tenant to prevent leakage.",
          ],
        },
        {
          title: "Topology determines control and failure shape",
          explanation:
            "A centralized supervisor decomposes, routes, and synthesizes with clear accountability but becomes a bottleneck. Peer-to-peer systems remove the single boss but are harder to control. Hierarchies compose teams at scale while multiplying coordination layers.",
          bullets: [
            "Supervisors behave like LLM routers over shared state.",
            "Peers need negotiation, consensus, and termination rules.",
            "Hierarchies need bounded delegation at every level.",
            "Measure handoffs, agent-specific failures, and total call budget.",
          ],
        },
      ],
      takeaways: [
        "Use multiple agents for genuine specialization or parallelism.",
        "A runtime provides identity, lifecycle, and messaging.",
        "Communication and topology determine security and debugging complexity.",
        "Every team needs an owner of synthesis, budget, and completion.",
      ],
      examQuestions: [
        "List four benefits and four costs of multi-agent systems.",
        "What are the four dimensions of collaboration?",
        "Compare shared state, direct messaging, and publish-subscribe.",
        "When is a distributed runtime justified?",
        "Compare centralized, decentralized, and hierarchical topologies.",
        "How does a supervisor pattern terminate safely?",
      ],
      source: "08-multi-agent-systems.pdf",
    },
    {
      id: 9,
      slug: "multi-agent-interop",
      title: "Multi-Agent Interoperability",
      thesis:
        "A2A treats agents as discoverable services with long-running task lifecycles, while MCP connects each agent to tools and data.",
      objectives: [
        "Explain the agent interoperability problem",
        "Describe Agent Cards and A2A task objects",
        "Separate MCP and A2A responsibilities",
        "Threat-model cross-agent delegation",
      ],
      sections: [
        {
          title: "Agent ecosystems recreate the integration problem one layer up",
          explanation:
            "Real agents use different frameworks, vendors, organizations, endpoints, and security domains. Bespoke pairwise integrations do not scale. An interoperable agent must publish capabilities and accept work without exposing its internal reasoning implementation.",
          bullets: [
            "An agent resembles a service with discovery, endpoint, and authentication.",
            "Unlike a simple API, it reasons and may run for minutes or days.",
            "The protocol must cover status, streaming, and artifacts.",
          ],
        },
        {
          title: "A2A 1.0.0 separates operations from bindings",
          explanation:
            "A2A 1.0.0 defines a task and message model with JSON-RPC, gRPC, and HTTP/REST bindings. This course traces JSON-RPC over HTTP. Select a binding and version explicitly when implementing discovery, streaming, and authentication.",
          bullets: [
            "This course uses the JSON-RPC binding over HTTP.",
            "Other defined bindings include gRPC and HTTP/REST.",
            "The JSON-RPC streaming path uses server-sent events.",
            "The application authenticates and authorizes each caller.",
          ],
        },
        {
          title: "Agent Cards make capabilities discoverable",
          explanation:
            "An Agent Card is a machine-readable manifest containing identity, provider, version, skills, endpoint, and authentication information. Clients can fetch a well-known URL, use a registry, or follow a referral.",
          bullets: [
            "Discovery avoids hard-coding every remote capability.",
            "Cards should be authenticated or signed before trust.",
            "Capabilities should be described at agent-level granularity.",
          ],
        },
        {
          title: "Tasks organize long-running collaboration",
          explanation:
            "A task has a lifecycle such as submitted, working, waiting for input, completed, failed, or canceled. Messages contain parts such as text or files; artifacts are the produced deliverables. Streaming exposes progress without pretending the work is one synchronous call.",
          bullets: [
            "Messages carry conversation turns.",
            "Parts carry multimodal content.",
            "Artifacts carry completed outputs.",
            "Lifecycle state enables pause, input, retry, and completion.",
          ],
        },
        {
          title: "MCP and A2A form two different layers",
          explanation:
            "MCP connects an agent to schema-defined tools and data sources. A2A connects one autonomous, reasoning agent to another through a task lifecycle. A remote agent may itself use MCP servers to complete delegated work.",
          bullets: [
            "Use MCP for vertical integration with tools and data.",
            "Use A2A for horizontal collaboration across agent boundaries.",
            "Do not model a long-running autonomous service as a micro-tool.",
          ],
        },
        {
          title: "Delegation crosses trust and governance boundaries",
          explanation:
            "Every cross-agent edge raises questions about identity, authorization, prompt injection, over-delegation, data retention, compliance, cost, and audit. Remote outputs must be handled as untrusted content even after authentication.",
          bullets: [
            "Authenticate the agent and verify its card.",
            "Scope delegated authority by task, spend, action, and time.",
            "Confirm high-stakes actions with a human.",
            "Log context leaving the organization and artifacts returning.",
          ],
        },
      ],
      takeaways: [
        "A2A standardizes discovery and long-running work between agents.",
        "Agent Cards advertise identity, skills, endpoint, and authentication.",
        "MCP serves tools and data; A2A serves agent collaboration.",
        "Cross-agent trust requires authentication, least privilege, bounds, and audit.",
      ],
      examQuestions: [
        "Why is an agent not equivalent to a simple REST endpoint?",
        "What information belongs in an Agent Card?",
        "Define task, message, part, and artifact.",
        "How does A2A support long-running work?",
        "Compare MCP and A2A with a concrete example.",
        "Threat-model a delegated task across organizations.",
      ],
      source: "09-multi-agent-interop.pdf",
    },
    {
      id: 10,
      slug: "reasoning-planning",
      title: "Advanced Reasoning and Planning",
      thesis:
        "Reasoning strategies trade inference compute for exploration, correction, or structure; the correct strategy depends on task difficulty and verifiability.",
      objectives: [
        "Compare linear, sampled, searched, and reflective reasoning",
        "Choose a planning strategy",
        "Explain test-time compute scaling",
        "Recognize overthinking and faithfulness limits",
      ],
      sections: [
        {
          title: "A single chain is useful but commits early",
          explanation:
            "Chain-of-thought provides one linear path. It can make intermediate work inspectable, but a greedy chain has no exploration or recovery and its verbalized explanation is not guaranteed to be a faithful record of internal computation.",
          bullets: [
            "Compare a direct baseline with explicit reasoning on the task.",
            "Verify outputs externally where possible.",
            "Do not treat stated reasoning as ground truth.",
          ],
        },
        {
          title: "Self-consistency widens exploration by sampling",
          explanation:
            "Self-consistency samples multiple reasoning paths and aggregates their answers. Separately sampled outputs may share systematic errors. Measure whether voting improves the target task under a declared budget.",
          bullets: [
            "Cost grows roughly with the number of samples.",
            "Voting requires an answer that can be aggregated.",
            "Measure shared errors rather than assuming independence.",
          ],
        },
        {
          title: "Tree- and Graph-of-Thoughts add explicit search",
          explanation:
            "Tree-of-Thoughts generates candidate partial states, evaluates them, and expands promising branches using a search strategy, enabling lookahead and backtracking. Graph-of-Thoughts also merges and refines ideas rather than keeping a strict tree.",
          bullets: [
            "Search needs a useful evaluator.",
            "Branching can grow exponentially.",
            "Graphs support aggregation and refinement loops.",
            "Use search when alternatives and dead ends matter.",
          ],
        },
        {
          title: "Reflection improves one path over time",
          explanation:
            "Reflexion converts evaluation into a verbal lesson stored for another attempt. Self-Refine repeats critique and revision. Reflection deepens one trajectory, whereas search widens across trajectories.",
          bullets: [
            "A test or grounded critic makes reflection reliable.",
            "Vague self-critique can reinforce errors.",
            "Revision loops need quality and cost stops.",
          ],
        },
        {
          title: "Planning changes when and how decisions are made",
          explanation:
            "ReAct decides step by step and suits short uncertain tasks. Plan-and-execute decomposes first and can reduce repeated planning on long tasks. Re-planning repairs a plan after new evidence. DAG planning runs independent steps in parallel.",
          bullets: [
            "Reactive plans adapt but can be myopic.",
            "Up-front plans add global structure but can become stale.",
            "Parallel plans lower latency only when dependencies permit.",
            "Every planner needs execution feedback.",
          ],
        },
        {
          title: "Reasoning models internalize deliberate inference",
          explanation:
            "RL-trained reasoning models generate extended internal deliberation and spend test-time compute according to task difficulty. Strong models can serve as planners or orchestrators while cheaper models handle routine extraction, routing, and tool calls.",
          bullets: [
            "More thinking raises latency and cost.",
            "Easy problems can suffer from overthinking.",
            "Beyond a point, additional compute may reduce accuracy.",
            "Escalate selectively instead of using maximum reasoning everywhere.",
          ],
        },
      ],
      takeaways: [
        "Self-consistency samples; search branches; reflection revises.",
        "ReAct, plan-and-execute, re-planning, and DAG execution solve different control problems.",
        "Reasoning compute should be allocated by difficulty.",
        "Verbal reasoning is a scaffold, not proof of correctness.",
      ],
      examQuestions: [
        "Compare chain-of-thought and self-consistency.",
        "What are generate, evaluate, and search in Tree-of-Thoughts?",
        "How does Graph-of-Thoughts extend a tree?",
        "Compare reflection with search.",
        "When should an agent use ReAct, plan-and-execute, or parallel planning?",
        "Why can more reasoning hurt?",
      ],
      source: "10-reasoning-planning.pdf",
    },
    {
      id: 11,
      slug: "evaluation-observability",
      title: "Evaluation and Observability",
      thesis:
        "Agent quality requires systematic measurement of both final outcomes and the trajectories that produced them, supported by complete traces.",
      objectives: [
        "Design outcome and trajectory metrics",
        "Read benchmarks critically",
        "Use LLM judges with safeguards",
        "Build offline, online, and CI evaluation",
      ],
      sections: [
        {
          title: "Agent evaluation is difficult for structural reasons",
          explanation:
            "Runs are non-deterministic, outputs are open-ended, tasks are multi-step, and correctness, cost, latency, and safety can conflict. Models, tools, and prompts also change, so anecdotal testing cannot distinguish progress from regression.",
          bullets: [
            "Use repeated runs where variance matters.",
            "Define several metrics rather than one headline score.",
            "Version the complete system under evaluation.",
          ],
        },
        {
          title: "Outcome and trajectory answer different questions",
          explanation:
            "Outcome evaluation asks whether the final answer or task result is correct. Trajectory evaluation asks whether the agent used appropriate tools, safe actions, efficient steps, and acceptable time and cost.",
          bullets: [
            "Exact match suits unambiguous answers.",
            "Execution tests suit code and queries.",
            "Trajectory metrics localize the failing step.",
            "Safety and policy adherence belong in trajectory evaluation.",
          ],
        },
        {
          title: "Objective scorers are preferable where available",
          explanation:
            "Execution-based and exact scoring are easier to reproduce than reference similarity or an LLM judge. For RAG, retrieval and generation need separate metrics; for memory and multi-agent systems, evaluate recall, handoffs, agent-specific errors, and total cost.",
          bullets: [
            "RAG: retrieval recall/precision/MRR plus faithfulness and relevance.",
            "Memory: right item, right time, correct use, appropriate forgetting.",
            "Multi-agent: handoff quality, ownership, synthesis, and call budget.",
          ],
        },
        {
          title: "Benchmarks measure systems, not just base models",
          explanation:
            "GAIA tests multi-step assistant behavior, SWE-bench Verified tests repository issue resolution through execution, and tool-dialogue benchmarks test policy adherence. Scores depend on the model, prompt, tools, interface, scaffold, and evaluation harness.",
          bullets: [
            "Watch for training-data contamination.",
            "Weak tests may accept incorrect solutions.",
            "Benchmark tasks may not match production distribution.",
            "Ask whose system produced the number.",
          ],
        },
        {
          title: "LLM-as-judge is flexible but biased",
          explanation:
            "A judge model can score open-ended work at scale, but may favor position, verbosity, style, or its own outputs. Explicit rubrics, pairwise comparisons, swapped order, calibration against humans, and multiple judges reduce these risks.",
          bullets: [
            "Prefer checkable criteria over a vague quality score.",
            "Blind the judge to irrelevant identity information.",
            "Audit disagreements and drift.",
          ],
        },
        {
          title: "Tracing turns evaluation into engineering",
          explanation:
            "A run trace is a tree of spans for model calls, tools, retrieval, and agents. Each span records inputs, outputs, timing, tokens, cost, errors, and relevant metadata. Offline eval protects releases; online eval monitors live behavior; CI gates block regressions.",
          bullets: [
            "Build representative tasks with expected outcomes.",
            "Include hard, edge, adversarial, and safety cases.",
            "Run the same set on prompt, model, tool, or dependency changes.",
            "Alert on quality, latency, cost, and safety drift.",
          ],
        },
      ],
      takeaways: [
        "Evaluation is continuous system steering, not a final phase.",
        "Measure both task success and the path taken.",
        "Treat benchmark scores as scaffold-dependent evidence.",
        "Trace every model, tool, retrieval, and agent step.",
      ],
      examQuestions: [
        "Why is agent evaluation harder than single-answer evaluation?",
        "Give four outcome metrics and four trajectory metrics.",
        "What makes execution-based evaluation strong?",
        "How can benchmark contamination and weak tests mislead?",
        "What biases affect LLM-as-judge?",
        "What should a trace span record, and how does eval-in-CI use it?",
      ],
      source: "11-evaluation-observability.pdf",
    },
    {
      id: 12,
      slug: "safety-security",
      title: "Safety and Security",
      thesis:
        "Action amplifies model errors and attacks, so safety must be enforced through defense-in-depth at the model-runtime boundary and throughout the lifecycle.",
      objectives: [
        "Separate adversarial security from responsible-AI harms",
        "Explain prompt injection and excessive agency",
        "Apply defense-in-depth",
        "Design runtime guardrails and safety evaluation",
      ],
      sections: [
        {
          title: "Tools change the threat model",
          explanation:
            "A model that only produces text has limited direct effect; an agent can send messages, execute code, modify files, or make transactions. Autonomy may remove per-step review, and untrusted web pages, documents, emails, and tool results enter the same context as instructions.",
          bullets: [
            "The model proposes; the runtime authorizes.",
            "Real-world effects require stronger controls than content generation.",
            "Consequential actions need explicit policy and confirmation.",
          ],
        },
        {
          title: "Security and responsible AI overlap but are distinct",
          explanation:
            "Security addresses adversaries exploiting the agent through prompt injection, tool misuse, data exfiltration, memory poisoning, and excessive agency. Responsible AI addresses harmful, biased, toxic, false, or otherwise unsafe outputs.",
          bullets: [
            "Least privilege and sandboxing reduce adversarial impact.",
            "Alignment and content filters reduce harmful output.",
            "A jailbreak can connect the two categories.",
          ],
        },
        {
          title: "Prompt injection exploits the shared instruction-data channel",
          explanation:
            "Direct injection is supplied by a user. Indirect injection is hidden in content the agent retrieves. Because instructions and data enter the same context, the model may follow malicious text as if it were authorized guidance.",
          bullets: [
            "Indirect attacks require only control of content the agent reads.",
            "Tool results must never automatically become trusted instructions.",
            "There is no complete prompt-only fix.",
          ],
        },
        {
          title: "Excessive agency amplifies every successful exploit",
          explanation:
            "An injected instruction inherits the agent's available tools and credentials. Too many tools, broad scopes, persistent secrets, and unreviewed autonomy increase maximum harm.",
          bullets: [
            "Grant minimum tools and scopes.",
            "Default to read-only and short-lived credentials.",
            "Bound actions, time, spend, and network access.",
            "Require confirmation for destructive or irreversible operations.",
          ],
        },
        {
          title: "Defense-in-depth must be structural",
          explanation:
            "Input validation, untrusted-content quarantine, tool-call policy, sandboxing, output filtering, monitoring, and human approval provide independent layers. A guardrail prompt or guardrail model can be fooled and therefore cannot be the sole defense.",
          bullets: [
            "Validate before the model and again before tool execution.",
            "Separate trusted control data from retrieved content.",
            "Sanitize tool output before execution or rendering.",
            "Log and detect abnormal trajectories.",
          ],
        },
        {
          title: "Responsible output needs training-time and runtime controls",
          explanation:
            "Bias and toxicity can originate in web-scale training data; alignment methods such as RLHF and DPO shape preferred behavior. Runtime classifiers and guardrails screen inputs and outputs. Hallucination requires grounding, citations, abstention, and verification.",
          bullets: [
            "Measure toxicity and bias rather than assuming alignment solved them.",
            "Use RAG and tools for factual grounding.",
            "Apply safety controls across MCP servers and A2A delegation.",
            "Include injection and disallowed-action cases in evaluation.",
          ],
        },
      ],
      takeaways: [
        "Action moves safety enforcement into code and infrastructure.",
        "Prompt injection cannot be solved by a stronger prompt alone.",
        "Least privilege limits blast radius.",
        "Security, responsible AI, evaluation, and observability must work together.",
      ],
      examQuestions: [
        "Why does agent action raise the stakes compared with a chatbot?",
        "Differentiate security risks and responsible-AI harms.",
        "Compare direct and indirect prompt injection.",
        "What is excessive agency and how is it mitigated?",
        "Design a defense-in-depth stack for a tool-using agent.",
        "How should hallucination and toxic output be mitigated and tested?",
      ],
      source: "12-safety-security.pdf",
    },
    {
      id: 13,
      slug: "production-frontier",
      title: "Production, Economics, and the Frontier",
      thesis:
        "Production success is determined by the versioned, observable, economical, and secure system around the model rather than a one-off demo.",
      objectives: [
        "Close the prototype-to-production gap",
        "Engineer cost, latency, and reliability",
        "Explain AgentOps and safe rollout",
        "Connect current successes to open problems",
      ],
      sections: [
        {
          title: "A product must work repeatedly under constraints",
          explanation:
            "A prototype needs one successful demonstration; a production service must work safely, reliably, economically, and at scale. Prompts, tools, models, retrieval, memory, policies, and evals become versioned system components.",
          bullets: [
            "Reliability includes retries, timeouts, fallbacks, and idempotency.",
            "Compliance and security join functional correctness.",
            "The runtime, tools, and operating process need their own tests.",
          ],
        },
        {
          title: "Cost and latency compound across agent steps",
          explanation:
            "Agent loops make multiple model and tool calls, so per-token and per-call costs accumulate. Routing sends ordinary work to cheaper models and hard work to stronger reasoning models. Caching, smaller models, fine-tuning, and bounded loops reduce spend.",
          bullets: [
            "Cache embeddings, retrievals, results, and prompt prefixes.",
            "Parallelize independent steps.",
            "Stream progress to reduce perceived latency.",
            "Set token, step, time, and spend budgets.",
          ],
        },
        {
          title: "AgentOps combines service operations with LLM-specific controls",
          explanation:
            "Production agents need traces, dashboards, alerts, prompt and model versioning, evaluation gates, guardrails, and human checkpoints in addition to normal service reliability patterns.",
          bullets: [
            "Trace model, tool, retrieval, memory, and agent spans.",
            "Monitor quality, cost, latency, error, and safety metrics.",
            "Use circuit breakers and fallbacks for unstable dependencies.",
            "Preserve reproducibility across silent model or tool changes.",
          ],
        },
        {
          title: "Rollout should be reversible",
          explanation:
            "Agents can ship as services, batch workers, or embedded assistants. Canary releases, feature flags, gradual traffic, evaluation gates, and rapid rollback reduce the impact of behavioral regressions.",
          bullets: [
            "Test on representative and adversarial tasks before deployment.",
            "Require approval for consequential actions.",
            "Keep a human-owned escalation path.",
            "Audit actions after deployment.",
          ],
        },
        {
          title: "Execution-grounded domains reveal the clearest wins",
          explanation:
            "Coding agents can inspect repositories, edit files, and run tests; their Agent-Computer Interface exposes compact actions and concise feedback. Computer-use agents generalize to GUIs through screenshots or accessibility trees but remain more brittle.",
          bullets: [
            "Interface design can matter as much as the base model.",
            "Execution tests make coding outcomes verifiable.",
            "Human review remains essential.",
            "High benchmark scores do not guarantee open-world reliability.",
          ],
        },
        {
          title: "The frontier and the open problems advance together",
          explanation:
            "Reasoning models, longer autonomous horizons, computer use, multimodality, MCP, and A2A expand capability. Reliability over long horizons, evaluation leakage, prompt injection, cost, accountability, labor impact, and misuse remain unresolved constraints.",
          bullets: [
            "Clear ownership is required for deployed agents.",
            "Audit trails document what happened and why.",
            "Economics differ from fixed-cost traditional software.",
            "Launch only the least autonomous system that passes eval and safety gates.",
          ],
        },
      ],
      takeaways: [
        "Production is disciplined engineering around the model.",
        "Routing, caching, bounds, and parallelism control cost and latency.",
        "AgentOps versions, evaluates, traces, guards, and rolls back the whole system.",
        "Frontier capability does not remove reliability, security, or accountability limits.",
      ],
      examQuestions: [
        "What distinguishes an agent demo from a production product?",
        "Give four methods for reducing cost and four for reducing latency.",
        "What artifacts must be versioned for reproducibility?",
        "What does AgentOps add to ordinary service operations?",
        "Why are coding agents comparatively successful?",
        "Create a production launch checklist for an autonomous agent.",
      ],
      source: "13-production-frontier.pdf",
    },
  ],
};

applyCourseUpdate(course);
