import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { course } from "../presentations/src/course-data.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const chapterDir = path.join(root, "chapters");
const refsDir = path.join(root, "references");

const pad = (n) => String(n).padStart(2, "0");
const bullets = (items) => items.map((item) => `- ${item}`).join("\n");
const questions = (items) =>
  items.map((item, index) => `${index + 1}. ${item}`).join("\n");

function chapterMarkdown(chapter) {
  return `# ${pad(chapter.id)}. ${chapter.title}

> ${chapter.thesis}

## Learning objectives

${bullets(chapter.objectives)}

## Core notes

${chapter.sections
  .map(
    (section) => `### ${section.title}

${section.explanation}

${bullets(section.bullets)}`,
  )
  .join("\n\n")}

## Exam-ready summary

${bullets(chapter.takeaways)}

## Self-test

${questions(chapter.examQuestions)}

## Assessed practice

${chapter.activity.task}

**Acceptance check:** ${chapter.activity.acceptance}

**Lab:** ${chapter.activity.lab}

## Reading and evidence

${chapter.readings.length ? chapter.readings.map(r => `- **${r.id}** [${r.title}](${r.url}). ${r.kind}, ${r.date}. ${r.note}`).join("\n") : "Use the classroom baseline and its explicit acceptance tests. This activity is a teaching design."}

## Source basis

The original structure follows \`${chapter.source}\`. The ${course.edition} edition adds the readings above, protocol clarifications, and assessed practice. Research findings and classroom exercises have different scopes.
`;
}

const glossary = [
  ["A2A", "A protocol for discovery and long-running collaboration between autonomous agents."],
  ["Action", "A model-proposed tool call that the runtime validates, authorizes, and executes."],
  ["Agent", "A system that uses an LLM as a reasoning core inside a loop to pursue a goal through actions."],
  ["Agent Card", "A machine-readable manifest describing an agent's identity, skills, endpoint, and authentication."],
  ["AgentOps", "Operational practices for versioning, evaluating, tracing, guarding, deploying, and monitoring agents."],
  ["Augmented LLM", "An LLM combined with retrieval, tools, and memory."],
  ["Chain-of-thought", "A linear sequence of intermediate reasoning steps used to scaffold a multi-step answer."],
  ["Context engineering", "Selecting and arranging instructions, tools, evidence, memory, and history within a token budget."],
  ["Evaluator-optimizer", "A workflow in which an evaluator gives criteria-based feedback to a generator for revision."],
  ["GraphRAG", "Retrieval over entities and relationships in a knowledge graph."],
  ["Long-term memory", "External persistent storage for selected episodic, semantic, or procedural information."],
  ["MCP", "A protocol that standardizes connections between LLM hosts and tools, resources, and prompts."],
  ["Observation", "The real result returned by the runtime or environment after an action."],
  ["Orchestrator-workers", "A pattern in which a model dynamically decomposes work, delegates subtasks, and synthesizes results."],
  ["Profile", "The role, objective, constraints, tools, and output protocol that define an agent's behavior."],
  ["RAG", "Retrieval-augmented generation: fetching external evidence at query time and adding it to model context."],
  ["ReAct", "A loop that interleaves Thought, Action, and Observation."],
  ["Reflection", "Critiquing an attempt and using feedback to revise or guide a later attempt."],
  ["Self-consistency", "Sampling multiple reasoning chains and aggregating their answers, usually by majority vote."],
  ["Short-term memory", "The bounded current context containing instructions, evidence, and recent task history."],
  ["Tool", "A typed operation available to the model through a controlled runtime."],
  ["Trajectory evaluation", "Evaluation of tool choices, steps, cost, latency, and safety during an agent run."],
  ["Workflow", "LLM calls and tools connected by code-defined control paths."],
];

const frontMatter = `# ${course.title}: Studybook and Exam Conspect

${course.subtitle}.

This studybook develops agent architecture through implementation, evaluation, and operating decisions. The ${course.edition} edition combines the original 13-chapter structure with dated research readings and assessed labs using Gemini, LangGraph, and the OpenAI Agents SDK. Each chapter states an observable acceptance check.

## How to use this studybook

1. Follow the chapter sequence below; complete each assessed practice and self-test.
2. Use repaired Labs 3-4 before the four assessed Labs 5-8; finish with teaching/CAPSTONE.md.
3. Record failures as well as successes. Fixtures test code; live experiments test a configured system.
4. Read research findings with their stated limitations.

## Course map

| Part | Chapters | Central question |
|---|---:|---|
| Foundations | 1-3 | What is an agent, and how does its loop work? |
| Architecture | 4-7 | How should control, tools, knowledge, and state be composed? |
| Coordination | 8-10 | How should agents collaborate and reason over longer horizons? |
| Assurance | 11-13 | How do we measure, secure, operate, and govern the system? |

## The unifying mental model

An agent is not a prompt with a fashionable name. It is a controlled system:

\`goal -> context/profile -> reason/plan -> proposed action -> runtime validation -> tool/environment -> observation -> updated state\`

The loop is bounded by step, token, time, and cost budgets. Evaluation measures both the outcome and the trajectory. Security is enforced at every action and trust boundary. Production engineering versions and observes every moving part.
`;

const examGuide = `# Exam Preparation Guide

## Six comparisons to master

| Compare | Essential distinction |
|---|---|
| Chatbot vs workflow vs agent | Reply-only vs code-directed control vs model-directed control |
| Prompting vs RAG vs fine-tuning | Behavior in context vs external knowledge vs weight adaptation |
| ReAct vs plan-and-execute | Next-step reactive choice vs global plan followed by execution |
| Workflow vs multi-agent | Explicit control paths vs coordinated autonomous roles |
| MCP vs A2A | Agent-to-tool/data integration vs agent-to-agent collaboration |
| Outcome vs trajectory evaluation | Whether the result is correct vs how it was produced |

## Four diagrams to reproduce from memory

1. The perceive-reason-act loop with the runtime at the action boundary.
2. The classic RAG ingestion and query pipeline.
3. The two-layer MCP + A2A architecture.
4. The production loop: build -> eval gate -> guardrails -> deploy -> trace and monitor.

## High-value design rules

- Choose the least autonomy that solves the problem.
- The model proposes; the runtime validates, authorizes, and executes.
- Relevance beats context volume.
- Evaluate retrieval and generation separately.
- Add agents only for measured specialization, modularity, parallelism, or context division.
- Prefer objective and execution-based evaluation.
- You cannot prompt your way out of prompt injection.
- Version prompts, tools, models, policies, data, and evals.

## Practice method

For a coding assessment, submit the input cases, expected results, versioned setup, and observed failures. Compare a simpler baseline before adding autonomy. Distinguish a malformed response, a wrong answer, an API failure, and a denied action. The capstone rubric appears in teaching/CAPSTONE.md.

For every architecture question, answer in four passes: define the components, trace control flow, identify failure modes, then state evaluation and safety controls. This mirrors how the source course develops each topic and prevents answers that describe capability without engineering discipline.
`;

async function buildReferenceAppendix() {
  const extractedDir = path.join(root, "tmp", "extracted");
  const blocks = [];
  for (const chapter of course.chapters) {
    const txtPath = path.join(
      extractedDir,
      chapter.source.replace(/\.pdf$/, ".txt"),
    );
    let text = "";
    try {
      text = await fs.readFile(txtPath, "utf8");
    } catch {
      continue;
    }
    const pages = text.split("\f");
    const referencePages = pages.filter((page) =>
      /^\s*References(?:\s*\(|\s*$)/m.test(page),
    );
    const cleaned = referencePages
      .join("\n")
      .split("\n")
      .map((line) => line.trimEnd())
      .filter((line) => !/^\s*\d+\s*$/.test(line))
      .join("\n")
      .replace(/\n{3,}/g, "\n\n")
      .trim();
    blocks.push(`## ${pad(chapter.id)}. ${chapter.title}\n\n${cleaned}`);
  }
  return `# Source Reference Appendix

The entries below are transcribed from the reference slides in the supplied PDFs. They are retained as the evidence base for the rewritten studybook and improved presentations. The dated research additions appear in each chapter and in improvements/RESEARCH-UPDATE.md. This appendix preserves the original source references.

${blocks.join("\n\n")}
`;
}

async function main() {
  await fs.mkdir(chapterDir, { recursive: true });
  await fs.mkdir(refsDir, { recursive: true });

  const chapterFiles = [];
  for (const chapter of course.chapters) {
    const file = `${pad(chapter.id)}-${chapter.slug}.md`;
    const markdown = chapterMarkdown(chapter);
    await fs.writeFile(path.join(chapterDir, file), markdown);
    chapterFiles.push({ chapter, file, markdown });
  }

  const combined = [
    frontMatter,
    ...chapterFiles.map(({ markdown }) => markdown),
    examGuide,
    "# Glossary\n\n" +
      glossary.map(([term, definition]) => `**${term}.** ${definition}`).join("\n\n"),
  ].join("\n\n---\n\n");
  await fs.writeFile(path.join(root, "STUDYBOOK.md"), combined);
  await fs.writeFile(path.join(root, "EXAM-GUIDE.md"), examGuide);
  await fs.writeFile(
    path.join(refsDir, "source-reference-appendix.md"),
    await buildReferenceAppendix(),
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
