"""Execute the ten RAG notebooks in fresh kernels; real DB/models required."""
import base64
import hashlib
import json
import os
import platform
import sys
import tempfile
from pathlib import Path
from importlib.metadata import version
import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager
ROOT=Path(__file__).resolve().parents[1]
TRACK=ROOT/'labs/rag'

def main():
    paths=sorted(TRACK.glob('*.ipynb'))+sorted((TRACK/'instructor').glob('*.ipynb'))
    if len(paths)!=10: raise RuntimeError('Expected ten student/instructor notebooks')
    results=[]
    with tempfile.TemporaryDirectory(prefix='rag-kernels-') as tmp:
        kernel=Path(tmp)/'rag-validation';kernel.mkdir()
        (kernel/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'RAG validation','language':'python'}))
        manager=KernelSpecManager(kernel_dirs=[tmp])
        env=dict(os.environ)
        for key in ('GEMINI_API_KEY','GOOGLE_API_KEY','OPENAI_API_KEY'):env.pop(key,None)
        env.update(MPLCONFIGDIR=str(Path(tmp)/'matplotlib'),IPYTHONDIR=str(Path(tmp)/'ipython'),HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
        for path in paths:
            n=nbformat.read(path,as_version=4);nbformat.validate(n)
            assert not any('RUN_GENERATION = True' in c.source for c in n.cells if c.cell_type=='code')
            client=NotebookClient(n,timeout=240,kernel_name='rag-validation',resources={'metadata':{'path':str(TRACK)}})
            client.km=client.create_kernel_manager();client.km.kernel_spec_manager=manager
            client.execute(env=env)
            nbformat.write(n,path)
            figure_count=0
            for cell in n.cells:
                for output in cell.get('outputs',[]):
                    data=output.get('data',{})
                    if 'image/png' in data and path.parent.name!='instructor':
                        figure_count+=1
                        (TRACK/'validation'/f'{path.stem}-{figure_count}.png').write_bytes(base64.b64decode(data['image/png']))
            results.append({'notebook':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'status':'passed','exercises':'executed' if path.parent.name=='instructor' else 'disabled; worked cells executed','gemini':'not run'})
            print('PASS',path.relative_to(ROOT),flush=True)
    report={'checked':'2026-10-07','python':sys.version,'platform':platform.platform(),
        'versions':{p:version(p) for p in ('llama-index-core','psycopg','pgvector','fastapi','sentence-transformers','torch','numpy','nbformat','nbclient')},'notebooks':results}
    (TRACK/'validation/notebook-results.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
