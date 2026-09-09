import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";
import { course } from "./course-data.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const outDir = path.join(root, "tmp", "course-update", "drafts");
const renderRoot = path.join(root, "tmp", "deck-build", "renders");
const pad = (n) => String(n).padStart(2, "0");

const palette = {
  ink: "#111111",
  paper: "#F7F7F2",
  white: "#FFFFFF",
  muted: "#5B5B57",
  line: "#D5D5CE",
  foundations: "#B9F15B",
  architecture: "#73C8FF",
  coordination: "#FFB45E",
  assurance: "#C4A1FF",
};

function accentFor(chapterId) {
  if (chapterId <= 3) return palette.foundations;
  if (chapterId <= 7) return palette.architecture;
  if (chapterId <= 10) return palette.coordination;
  return palette.assurance;
}

function addText(slide, name, text, position, style = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name,
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontSize: style.fontSize ?? 22,
    typeface: style.typeface ?? "Helvetica Neue",
    color: style.color ?? palette.ink,
    bold: style.bold ?? false,
    alignment: style.alignment ?? "left",
    verticalAlignment: style.verticalAlignment ?? "top",
    autoFit: style.autoFit ?? "shrinkText",
  };
  return shape;
}

function addRect(slide, name, position, fill, lineFill = fill) {
  return slide.shapes.add({
    geometry: "rect",
    name,
    position,
    fill,
    line: { style: "solid", fill: lineFill, width: 0 },
  });
}

function addChrome(slide, chapter, slideNumber, sectionLabel = "AGENTIC AI") {
  const accent = accentFor(chapter.id);
  addRect(slide, "accent-line", { left: 41, top: 32, width: 1198, height: 7 }, accent);
  addText(
    slide,
    "chapter-label",
    `${sectionLabel}  /  ${pad(chapter.id)}`,
    { left: 41, top: 49, width: 520, height: 34 },
    { fontSize: 17, bold: true, color: palette.muted, autoFit: "none" },
  );
  addText(
    slide,
    "slide-number",
    `${pad(slideNumber)}`,
    { left: 1160, top: 660, width: 78, height: 28 },
    { fontSize: 16, alignment: "right", color: palette.muted, autoFit: "none" },
  );
  addText(
    slide,
    "chapter-footer",
    chapter.title,
    { left: 41, top: 660, width: 860, height: 28 },
    { fontSize: 15, color: palette.muted, autoFit: "none" },
  );
}

function setNotes(slide, chapter, note) {
  slide.speakerNotes.textFrame.setText(
    `${note}\n\nEdition: ${course.edition}\n\n[Sources]\n- Original source presentation: ${chapter.source}\n${chapter.readings.map(r => `- ${r.id}: ${r.title}. ${r.kind}, ${r.date}. ${r.url} ${r.note}`).join("\n")}\n\n[Assessed practice]\n${chapter.activity.task}\nAcceptance: ${chapter.activity.acceptance}\nLab: ${chapter.activity.lab}`,
  );
  slide.speakerNotes.setVisible(true);
}

function addTitleSlide(presentation, chapter) {
  const slide = presentation.slides.add();
  slide.background.fill = palette.paper;
  const accent = accentFor(chapter.id);
  addRect(slide, "title-accent", { left: 0, top: 0, width: 18, height: 720 }, accent);
  addText(
    slide,
    "course-title",
    course.title.toUpperCase(),
    { left: 42, top: 42, width: 420, height: 45 },
    { fontSize: 22, bold: true, color: palette.muted, autoFit: "none" },
  );
  addText(
    slide,
    "chapter-number",
    pad(chapter.id),
    { left: 1060, top: 38, width: 176, height: 56 },
    { fontSize: 32, bold: true, alignment: "right", autoFit: "none" },
  );
  addText(
    slide,
    "deck-title",
    chapter.title,
    { left: 42, top: 160, width: 1035, height: 270 },
    { fontSize: 64, bold: true, verticalAlignment: "bottom" },
  );
  addText(
    slide,
    "deck-thesis",
    chapter.thesis,
    { left: 42, top: 484, width: 895, height: 116 },
    { fontSize: 27, color: palette.muted },
  );
  addRect(slide, "title-marker", { left: 1000, top: 484, width: 238, height: 116 }, accent);
  addText(
    slide,
    "title-marker-text",
    "STUDY\nDECK",
    { left: 1024, top: 500, width: 190, height: 82 },
    { fontSize: 25, bold: true, verticalAlignment: "middle", autoFit: "none" },
  );
  setNotes(slide, chapter, "Open with the chapter thesis and connect it to the previous chapter.");
  return slide;
}

function addObjectivesSlide(presentation, chapter, slideNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = palette.white;
  addChrome(slide, chapter, slideNumber, "LEARNING MAP");
  addText(
    slide,
    "objectives-title",
    "By the end, you should be able to...",
    { left: 41, top: 104, width: 1120, height: 82 },
    { fontSize: 42, bold: true, autoFit: "none" },
  );
  const xs = [41, 344, 647, 950];
  chapter.objectives.forEach((objective, index) => {
    addText(
      slide,
      `objective-number-${index + 1}`,
      pad(index + 1),
      { left: xs[index], top: 250, width: 210, height: 66 },
      { fontSize: 46, bold: true, color: accentFor(chapter.id), autoFit: "none" },
    );
    addText(
      slide,
      `objective-${index + 1}`,
      objective,
      { left: xs[index], top: 330, width: 250, height: 190 },
      { fontSize: 25, bold: true },
    );
  });
  setNotes(slide, chapter, "Use these objectives as an advance organizer and as a checklist after the deck.");
  return slide;
}

function addSectionLeftRight(presentation, chapter, section, slideNumber, index) {
  const slide = presentation.slides.add();
  slide.background.fill = palette.white;
  addChrome(slide, chapter, slideNumber, `CORE IDEA ${pad(index + 1)}`);
  addText(
    slide,
    "section-title",
    section.title,
    { left: 41, top: 102, width: 1170, height: 102 },
    { fontSize: 40, bold: true },
  );
  addText(
    slide,
    "section-explanation",
    section.explanation,
    { left: 41, top: 250, width: 475, height: 305 },
    { fontSize: 25, color: palette.muted },
  );
  addRect(
    slide,
    "column-rule",
    { left: 560, top: 246, width: 5, height: 342 },
    accentFor(chapter.id),
  );
  const bulletText = section.bullets
    .map((bullet, i) => `${pad(i + 1)}  ${bullet}`)
    .join("\n\n");
  addText(
    slide,
    "section-points",
    bulletText,
    { left: 615, top: 246, width: 585, height: 360 },
    { fontSize: 23, bold: true },
  );
  setNotes(slide, chapter, "Explain the claim first, then use the numbered points as evidence and design consequences.");
  return slide;
}

function addSectionStatement(presentation, chapter, section, slideNumber, index) {
  const slide = presentation.slides.add();
  slide.background.fill = palette.paper;
  addChrome(slide, chapter, slideNumber, `CORE IDEA ${pad(index + 1)}`);
  addText(
    slide,
    "section-title",
    section.title,
    { left: 41, top: 105, width: 1170, height: 88 },
    { fontSize: 40, bold: true },
  );
  addText(
    slide,
    "section-explanation",
    section.explanation,
    { left: 120, top: 225, width: 1040, height: 150 },
    { fontSize: 28, bold: true, alignment: "center", verticalAlignment: "middle" },
  );
  const count = section.bullets.length;
  const gap = 28;
  const width = (1138 - gap * (count - 1)) / count;
  section.bullets.forEach((bullet, i) => {
    const left = 41 + i * (width + gap);
    addRect(
      slide,
      `point-band-${i + 1}`,
      { left, top: 425, width, height: 8 },
      accentFor(chapter.id),
    );
    addText(
      slide,
      `point-${i + 1}`,
      bullet,
      { left, top: 454, width, height: 145 },
      { fontSize: 21, bold: true },
    );
  });
  setNotes(slide, chapter, "Pause on the central statement, then connect the lower points as a single mental model.");
  return slide;
}

function addExamSlide(presentation, chapter, slideNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = palette.white;
  addChrome(slide, chapter, slideNumber, "EXAM CHECK");
  addText(
    slide,
    "exam-title",
    "Can you answer these without notes?",
    { left: 41, top: 103, width: 1120, height: 82 },
    { fontSize: 42, bold: true, autoFit: "none" },
  );
  chapter.examQuestions.forEach((question, index) => {
    const col = index % 2;
    const row = Math.floor(index / 2);
    const left = col === 0 ? 41 : 650;
    const top = 235 + row * 132;
    addText(
      slide,
      `exam-number-${index + 1}`,
      pad(index + 1),
      { left, top, width: 62, height: 42 },
      { fontSize: 23, bold: true, color: accentFor(chapter.id), autoFit: "none" },
    );
    addText(
      slide,
      `exam-question-${index + 1}`,
      question,
      { left: left + 72, top, width: 500, height: 94 },
      { fontSize: 21, bold: true },
    );
  });
  setNotes(slide, chapter, "Use as retrieval practice. Ask for an answer that defines, compares, traces, and evaluates.");
  return slide;
}

function addClosingSlide(presentation, chapter, slideNumber) {
  const slide = presentation.slides.add();
  slide.background.fill = palette.paper;
  addChrome(slide, chapter, slideNumber, "CHAPTER SYNTHESIS");
  addText(
    slide,
    "closing-title",
    "What must remain after the details fade",
    { left: 41, top: 110, width: 1080, height: 94 },
    { fontSize: 42, bold: true },
  );
  chapter.takeaways.forEach((takeaway, index) => {
    const top = 245 + index * 92;
    addText(
      slide,
      `takeaway-number-${index + 1}`,
      pad(index + 1),
      { left: 41, top, width: 74, height: 52 },
      { fontSize: 30, bold: true, color: accentFor(chapter.id), autoFit: "none" },
    );
    addText(
      slide,
      `takeaway-${index + 1}`,
      takeaway,
      { left: 132, top: top - 2, width: 1000, height: 68 },
      { fontSize: 26, bold: true },
    );
  });
  setNotes(slide, chapter, "Close by restating the four durable ideas and linking forward to the next chapter.");
  return slide;
}

function addPracticeSlide(presentation, chapter, slideNumber) {
  const slide=presentation.slides.add();
  slide.background.fill=palette.white;
  addChrome(slide,chapter,slideNumber,"PRACTICE AND READING");
  addText(slide,"practice-title","Evidence to submit",{left:41,top:105,width:1170,height:70},{fontSize:40,bold:true});
  addText(slide,"practice-task",chapter.activity.task,{left:41,top:210,width:1150,height:130},{fontSize:26});
  addText(slide,"practice-check",chapter.activity.acceptance,{left:41,top:355,width:1150,height:115},{fontSize:24,color:palette.muted});
  const reading=chapter.readings.map(r=>`${r.id}  ${r.title}`).join("\n");
  addText(slide,"practice-readings",reading || "Reading: classroom baseline and acceptance tests",{left:41,top:490,width:1150,height:105},{fontSize:19});
  addText(slide,"practice-lab",chapter.activity.lab,{left:41,top:615,width:1150,height:28},{fontSize:17,color:palette.muted});
  setNotes(slide,chapter,"Assess the submitted evidence with the stated acceptance check. Reading links and limitations follow.");
  return slide;
}

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

async function buildChapter(chapter) {
  const presentation = Presentation.create({
    slideSize: { width: 1280, height: 720 },
  });
  addTitleSlide(presentation, chapter);
  addObjectivesSlide(presentation, chapter, 2);
  chapter.sections.forEach((section, index) => {
    const slideNumber = index + 3;
    if (index % 2 === 0) {
      addSectionLeftRight(presentation, chapter, section, slideNumber, index);
    } else {
      addSectionStatement(presentation, chapter, section, slideNumber, index);
    }
  });
  addExamSlide(presentation, chapter, chapter.sections.length + 3);
  addClosingSlide(presentation, chapter, chapter.sections.length + 4);
  addPracticeSlide(presentation, chapter, chapter.sections.length + 5);

  const deckName = `${pad(chapter.id)}-${chapter.slug}.pptx`;
  const deckPath = path.join(outDir, deckName);
  const renderDir = path.join(renderRoot, `${pad(chapter.id)}-${chapter.slug}`);
  await fs.mkdir(renderDir, { recursive: true });

  for (const [index, slide] of presentation.slides.items.entries()) {
    const layout = await slide.export({format:"layout"});
    await fs.writeFile(path.join(renderDir, `slide-${pad(index+1)}.layout.json`), await layout.text());
    const png = await presentation.export({ slide, format: "png", scale: 1 });
    await writeBlob(path.join(renderDir, `slide-${pad(index + 1)}.png`), png);
  }
  const montage = await presentation.export({
    format: "webp",
    montage: true,
    scale: 1,
  });
  await writeBlob(path.join(renderDir, "montage.webp"), montage);

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(deckPath);
  return { deckPath, slides: presentation.slides.items.length };
}

async function main() {
  await fs.mkdir(outDir, { recursive: true });
  await fs.mkdir(renderRoot, { recursive: true });
  const results = [];
  for (const chapter of course.chapters) {
    results.push(await buildChapter(chapter));
    console.log(`Built ${path.basename(results.at(-1).deckPath)} (${results.at(-1).slides} slides)`);
  }
  await fs.writeFile(
    path.join(renderRoot, "build-results.json"),
    JSON.stringify(results, null, 2),
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

