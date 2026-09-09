// Dated curriculum additions. IDs correspond to improvements/CLAIM-LEDGER.md.
export const edition = "2026-09-09";
export const sources = {
  P1: {title:"GPT-Red: Automated Red Teaming via Self-Play at Scale",date:"2026-07-15",kind:"OpenAI technical paper",url:"https://cdn.openai.com/pdf/gpt-red-automated-red-teaming-via-self-play-at-scale.pdf",note:"Self-play and held-out adversarial evaluation. Classroom policy checks do not reproduce this training."},
  P2: {title:"Scientific computing in the age of agentic AI",date:"2026-07-28",kind:"OpenAI-affiliated exploratory field report",url:"https://cdn.openai.com/pdf/scientific-computing-in-the-age-of-agentic-ai-an-exploratory-field-report.pdf",note:"Case studies motivate verification and maintenance ownership. They do not estimate a universal productivity effect."},
  P3: {title:"Would this change your answer?",date:"2026-08-17",kind:"Anthropic/Fellows preprint, arXiv v1",url:"https://arxiv.org/abs/2608.16747",note:"CHIVE tests counterfactual prompt changes. Generated explanations remain hypotheses. Official post: August 21."},
  R1: {title:"Patterns and problems in emerging multiagent systems",date:"2026-08-13",kind:"Anthropic research post",url:"https://www.anthropic.com/research/multiagent-systems",note:"Controlled coordination experiments. Compare scope and budgets before interpreting the findings."},
  R2: {title:"How enabling two settings tripled our scores on the ARC-AGI-3 benchmark",date:"2026-07-29",kind:"OpenAI research post",url:"https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/",note:"A specific harness experiment. Its result does not estimate the effect of context changes in Gemini."},
  R3: {title:"Research acceleration: The view inside OpenAI",date:"2026-09-06",kind:"OpenAI observational research post",url:"https://openai.com/index/research-acceleration-view-inside-openai/",note:"Activity metrics do not by themselves identify causal gains in research progress."},
  S1: {title:"Gemini function calling",date:edition,kind:"Google documentation, accessed",url:"https://ai.google.dev/gemini-api/docs/function-calling",note:"Check model support and preserve complete model content when returning function responses."},
  S2: {title:"OpenAI Agents SDK model integration",date:edition,kind:"SDK documentation, accessed",url:"https://openai.github.io/openai-agents-python/models/",note:"The course uses local tools with a Gemini Chat Completions compatibility endpoint."},
  S3: {title:"LangGraph interrupts",date:edition,kind:"LangChain documentation, accessed",url:"https://docs.langchain.com/oss/python/langgraph/interrupts",note:"Resume restarts the interrupted node. Put effects after approval and make replay safe."},
  S4: {title:"Gemini structured outputs",date:edition,kind:"Google documentation, accessed",url:"https://ai.google.dev/gemini-api/docs/structured-output",note:"Supported schemas constrain structure. Application validation must check meaning and policy."},
  S5: {title:"MCP roots specification 2025-11-25",date:"2025-11-25",kind:"Versioned protocol specification",url:"https://modelcontextprotocol.io/specification/2025-11-25/client/roots",note:"The course uses this historical protocol baseline. Implementations enforce access controls."},
  S6: {title:"A2A specification 1.0.0",date:edition,kind:"Versioned protocol specification, accessed",url:"https://a2a-protocol.org/v1.0.0/specification/",note:"Separates the data model from JSON-RPC, gRPC, and HTTP/REST bindings. The course traces JSON-RPC."},
};
const updates = [
  {
    title:"A baseline makes autonomy a testable choice",
    explanation:"Choose a small task with observable success before building an agent. Compare a fixed workflow with a model-directed loop on the same inputs. Treat the decision to add autonomy as an engineering hypothesis.",
    bullets:["Write expected outputs before implementation.","Keep task inputs and resource limits comparable.","Retain the simpler design when it meets the requirements."],
    task:"Choose a catalog lookup or arithmetic task. Write six cases, including empty input and an unknown item. Define a pass condition and a call limit. Explain what dynamic decision, if any, needs a model.",
    check:"Submit the cases and an architecture choice before running a model. Credit follows the evidence, including a decision to keep a fixed workflow.",
    lab:"labs/05_gemini_bounded_tools.ipynb", reading:[], question:"How would you test whether a fixed workflow is sufficient for a task?"
  },
  {
    title:"Behavioral claims need an external check",
    explanation:"CHIVE investigates model behavior by editing prompts and measuring the resulting responses. In this course, a plausible explanation is a hypothesis to test. Schema checks, factual checks, and policy checks answer different questions.",
    bullets:["Predict the effect of one prompt edit.","Score the response with a stated criterion.","Distinguish measured behavior from a causal explanation."],
    task:"Keep a factual task fixed and add one misleading cue. Predict whether the answer will change. Record both conditions and identify which check tests structure, evidence, or policy.",
    check:"The submission contains paired inputs and a testable prediction. It does not treat verbal reasoning as ground truth.",
    lab:"labs/07_agents_sdk_evaluation.ipynb", reading:["P3","S4"], question:"Why can a valid schema and a plausible explanation still accompany a wrong answer?"
  },
  {
    title:"A complete tool cycle returns observed results",
    explanation:"A native tool request is only part of the protocol. After validation, the runtime returns each result with the matching call identity and continues the model exchange. Preserve the provider's complete response content and cap the loop.",
    bullets:["Dispatch through the supplied tool registry.","Keep model rounds and tool calls as separate budgets.","Test empty responses and multiple calls."],
    task:"Complete Lab 5. Demonstrate that the second model request contains the executed tool result and its matching ID. Replace the registry with a fake and prove that the replacement runs.",
    check:"The offline round-trip and replacement-registry tests pass. A missing result or exhausted budget yields an explicit stop reason.",
    lab:"labs/05_gemini_bounded_tools.ipynb", reading:["S1"], question:"Which state must survive the model, tool, and model round-trip?"
  },
  {
    title:"An extra stage must justify its cost",
    explanation:"A reviewer or worker adds another opportunity to help and another opportunity to fail. Use identical cases to compare a baseline with the proposed composition. Count review and coordination calls when evaluating the whole system.",
    bullets:["Use a fixed baseline before changing the architecture.","Score outcomes and failures with the same rules.","Account for overhead even when review leaves the answer unchanged."],
    task:"Compare a single catalog agent with an objective evidence check. Specify when an LLM reviewer would add information that the objective check lacks.",
    check:"Include a case where review adds no value and one where it changes an incorrect proposal. Count all calls in the live variant.",
    lab:"labs/07_agents_sdk_evaluation.ipynb", reading:["R1"], question:"How can a reviewer increase cost without increasing correctness?"
  },
  {
    title:"Tool interfaces and authority need separate checks",
    explanation:"The labs use Gemini native calls and the OpenAI Agents SDK compatibility path. They expose local functions with explicit input limits. MCP descriptions and roots convey context, while the host and server implementations enforce access.",
    bullets:["Reject unknown names and extra arguments before execution.","Bound input size and arithmetic magnitude.","Check provider features rather than assuming parity."],
    task:"Complete Lab 5's dispatch policy. For the MCP 2025-11-25 baseline, explain why a roots response cannot substitute for filesystem access controls.",
    check:"Reject booleans in numeric fields, nonfinite values, and oversized input. Name the component that enforces each permission.",
    lab:"labs/05_gemini_bounded_tools.ipynb", reading:["S1","S2","S5"], question:"Why does an advertised filesystem root still need implementation-level access controls?"
  },
  {
    title:"Provenance and abstention make retrieval auditable",
    explanation:"Carry source IDs and text through every retrieval step. Check whether the evidence supports the answer separately from whether a citation ID exists. A bounded repair attempt should end in an answer or an explicit abstention.",
    bullets:["Compare against static retrieval on the same questions.","Keep conflicting evidence visible.","Treat a rewrite as optional and measurable."],
    task:"Complete Lab 6 and add unknown, conflicting, and irrelevant records. Compare zero repair with one repair using a fixed question set.",
    check:"Report retrieval hits, unsupported answers, abstentions, and attempts separately. A known citation ID alone does not count as grounded correctness.",
    lab:"labs/06_langgraph_corrective_rag.ipynb", reading:["S4"], question:"What can a citation-membership test establish, and what remains untested?"
  },
  {
    title:"Execution state and model context serve different purposes",
    explanation:"A checkpoint stores workflow state for resumption. A context policy chooses what the next model call can see. Test these mechanisms separately. OpenAI's harness experiment motivates recording context settings as part of the evaluated system.",
    bullets:["Reopen a checkpoint before resuming approval.","Keep side effects after the approval boundary.","Compare context policies without changing the task set."],
    task:"Complete Lab 8's checkpoint test. As an extension, compare a fixed recent-history window with a structured task summary on the same lookup tasks.",
    check:"Show the pending state before resume and one committed effect after a retry. Do not generalize a context-policy result across providers.",
    lab:"labs/08_langgraph_approval_security.ipynb", reading:["S3","R2"], question:"How can a workflow resume correctly while its next model call still lacks needed context?"
  },
  {
    title:"Shared evidence matters more than agreement",
    explanation:"Anthropic's multi-agent experiments include information-sharing failures and conflicting objectives. For a classroom comparison, keep task scope and budget explicit. Agreement between agents does not establish independent evidence.",
    bullets:["Inspect which facts each role receives.","Test a misleading cue shared across agents.","Give one component responsibility for synthesis and termination."],
    task:"Complete Lab 7. Compare a single agent, an objective reviewer, and an optional model reviewer. Add one case where every role sees the same misleading cue.",
    check:"Report extra requests and shared errors. Explain any scope or information advantage before comparing outcomes.",
    lab:"labs/07_agents_sdk_evaluation.ipynb", reading:["R1","S2"], question:"Why can a team agree on an incorrect answer even when its members sample separately?"
  },
  {
    title:"Delegation needs a versioned contract",
    explanation:"This chapter uses A2A 1.0.0 and traces its JSON-RPC binding. The specification also defines gRPC and HTTP/REST bindings. Identity, permission, and the validity of a returned artifact remain separate checks.",
    bullets:["Record the protocol version and selected binding.","Authenticate the caller before assigning authority.","Treat returned content as untrusted evidence."],
    task:"Trace a delegated catalog task from discovery to completion. Identify the caller, authorization decision, timeout owner, and artifact validator. No remote service deployment is required.",
    check:"Use A2A 1.0.0 terminology and distinguish the chosen binding from the abstract task model. Explain what happens after a failed or canceled task.",
    lab:"labs/08_langgraph_approval_security.ipynb", reading:["S6"], question:"Which responsibilities remain in the application after it adopts an interoperability protocol?"
  },
  {
    title:"Reasoning strategies require controlled comparisons",
    explanation:"Compare a direct baseline with sampling or review under a declared resource budget. Separate samples can share systematic errors. Counterfactual prompt edits test a behavioral claim without establishing a complete account of internal computation.",
    bullets:["Choose a scorer before inspecting answers.","Keep held-out cases out of prompt development.","Report when extra reasoning fails to help."],
    task:"Use Lab 7's paired inputs to test a prediction about a misleading cue. Propose an equal-budget comparison with voting and identify a shared-error failure case.",
    check:"Keep predictions, observations, and interpretations separate. State the limits of a small experiment.",
    lab:"labs/07_agents_sdk_evaluation.ipynb", reading:["P3","R1"], question:"What evidence would justify spending more inference on a reasoning strategy?"
  },
  {
    title:"A run manifest makes comparisons reviewable",
    explanation:"Record the complete setup and every attempted run. A completed answer can be wrong, and an infrastructure failure is a different outcome. Fixed cases and explicit denominators make a comparison inspectable.",
    bullets:["Store model ID, prompt hash, and dependency versions.","Record attempted and completed runs separately.","Keep outcome scoring separate from resource use."],
    task:"Run the offline evaluation command, inspect its JSONL records, and test the failure path. For live inference, predeclare a model and budget before using the held-out split.",
    check:"A fresh rerun produces a manifest and one record per attempted case. Interrupted or failed requests do not disappear from the denominator.",
    lab:"labs/07_agents_sdk_evaluation.ipynb", reading:["P3","R2"], question:"How should an evaluation distinguish a wrong answer from an API failure?"
  },
  {
    title:"Security tests distinguish proposals from effects",
    explanation:"A malicious proposal and a successful unauthorized effect are different outcomes. GPT-Red motivates evaluating held-out attacks, while this course tests a small application policy. Passing these fixtures does not establish general prompt-injection robustness.",
    bullets:["Bind approval to the exact proposed action.","Measure false rejection on benign requests.","Retain held-out adversarial cases."],
    task:"Complete Lab 8. Submit one valid request, one injection-shaped proposal, and one replay with changed arguments. Identify the trusted reviewer channel.",
    check:"Rejected actions create no ledger entry. A retry with the same ID cannot duplicate the effect, and changed payload reuse fails.",
    lab:"labs/08_langgraph_approval_security.ipynb", reading:["P1","S3"], question:"Why should a security report score model proposals and executed effects separately?"
  },
  {
    title:"A maintained system needs evidence and an owner",
    explanation:"The scientific-computing field report motivates reference tests and stewardship. OpenAI's observational research post also warns that activity metrics need careful interpretation. The capstone therefore assesses validated outcomes and reproducibility.",
    bullets:["Test recovery and unexpected inputs.","Name the maintainer and escalation path.","Separate activity counts from demonstrated task success."],
    task:"Submit the capstone bundle: baseline, bounded agent, held-out evaluation, negative tests, and an operating note. Include a reproducible command and a maintenance owner.",
    check:"The reviewer can rerun the bundle in a fresh environment and trace each conclusion to saved evidence. Follow teaching/CAPSTONE.md for the rubric.",
    lab:"labs/08_langgraph_approval_security.ipynb", reading:["P2","R3"], question:"What evidence and ownership must accompany a successful agent demonstration?"
  },
];
export function applyCourseUpdate(course) {
  course.edition=edition;
  course.sourcePolicy="Original course structure with dated research, protocol clarifications, and assessed engineering tasks.";
  for(const chapter of course.chapters) {
    const update=updates[chapter.id-1];
    chapter.sections.push({title:update.title,explanation:update.explanation,bullets:update.bullets,sources:update.reading});
    chapter.activity={task:update.task,acceptance:update.check,lab:update.lab};
    chapter.readings=update.reading.map(id=>({id,...sources[id]}));
    chapter.examQuestions[5]=update.question;
  }
}
