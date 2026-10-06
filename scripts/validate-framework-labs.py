"""Execute only the framework track in fresh kernels, with live inference disabled."""
from pathlib import Path
import hashlib
import json
import os
import platform
import sys
import tempfile
from importlib.metadata import version
import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / 'labs/frameworks'

def main():
    paths = sorted(TRACK.glob('*.ipynb')) + sorted((TRACK / 'instructor').glob('*.ipynb'))
    if len(paths) != 6:
        raise RuntimeError(f'Expected six notebooks, found {len(paths)}')
    results=[]
    env=dict(os.environ)
    for key in ('GEMINI_API_KEY','GOOGLE_API_KEY','OPENAI_API_KEY','LANGSMITH_API_KEY','LANGCHAIN_API_KEY'):
        env.pop(key,None)
    env.update(LANGCHAIN_TRACING_V2='false', LANGSMITH_TRACING='false', IPYTHONDIR=str(Path(tempfile.gettempdir())/'framework-ipython'))
    with tempfile.TemporaryDirectory(prefix='framework-kernels-') as tmp:
        kernel=Path(tmp)/'framework-validation'
        kernel.mkdir()
        (kernel/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Framework validation','language':'python'}))
        manager=KernelSpecManager(kernel_dirs=[tmp])
        for path in paths:
            notebook=nbformat.read(path,as_version=4)
            nbformat.validate(notebook)
            for cell in notebook.cells:
                if cell.cell_type=='code' and 'RUN_LIVE = True' in cell.source:
                    raise RuntimeError('Live calls must be disabled')
            client=NotebookClient(notebook, timeout=120, kernel_name='framework-validation', resources={'metadata':{'path':str(path.parent)}})
            client.km=client.create_kernel_manager()
            client.km.kernel_spec_manager=manager
            client.execute(env=env)
            # Keep compact worked outputs in the distributed notebook.
            nbformat.write(notebook,path)
            results.append({'notebook':str(path.relative_to(ROOT)), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'status':'passed','code_cells':sum(c.cell_type=='code' for c in notebook.cells),'exercises':'executed' if path.parent.name=='instructor' else 'disabled; worked examples executed','live_api':'not run'})
            print('PASS',path.relative_to(ROOT),flush=True)
    report={'checked':'2026-10-06','python':sys.version,'platform':platform.platform(),'packages':{p:version(p) for p in ('langgraph','langchain','langchain-google-genai','pydantic-ai-slim','pydantic','google-genai','nbformat','nbclient','ipykernel','nbconvert')},'notebooks':results}
    (TRACK/'validation/notebook-results.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__': main()
