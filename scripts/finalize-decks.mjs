import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {course} from '../presentations/src/course-data.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const skill=process.env.PRESENTATIONS_SKILL || '/Users/daeron/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations';
const python=process.env.RUNTIME_PYTHON || '/Users/daeron/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const build=path.join(root,'tmp/course-update');
const runDir=await fs.mkdtemp(path.join(build,'final-'));
for(const c of course.chapters){
 const name=String(c.id).padStart(2,'0')+'-'+c.slug+'.pptx';
 await finalizePresentation({workspaceDir:root,candidatePath:path.join(build,'drafts',name),finalPath:path.join(runDir,name),
  pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],
  explicitTotalSlideCount:12,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],
  fontPolicy:{basis:'design',families:['Helvetica Neue']},verifyArtifactToolImport:true,
  receiptPath:path.join(build,name+'.validation.json')});
 await fs.copyFile(path.join(runDir,name),path.join(root,'output/presentations',name));
 console.log('Finalized',name);
}
