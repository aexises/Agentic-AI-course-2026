"""Fresh-kernel checks; no provider credentials or live model calls."""
import hashlib,json,os,sys,tempfile
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager
root=Path(__file__).resolve().parents[1]/'labs/engineering'
for key in ('GEMINI_API_KEY','GOOGLE_API_KEY','OPENAI_API_KEY','TAVILY_API_KEY'):os.environ.pop(key,None)
out=root/'validation';out.mkdir(exist_ok=True)
results=[]
with tempfile.TemporaryDirectory() as tmp:
    kernel=Path(tmp)/'course-engineering';kernel.mkdir()
    (kernel/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Engineering validation','language':'python'}))
    manager=KernelSpecManager(kernel_dirs=[tmp])
    for path in sorted(root.glob('*.ipynb'))+sorted((root/'instructor').glob('*.ipynb')):
        book=nbformat.read(path,as_version=4);nbformat.validate(book)
        client=NotebookClient(book,timeout=120,kernel_name='course-engineering',resources={'metadata':{'path':str(root)}})
        client.km=client.create_kernel_manager();client.km.kernel_spec_manager=manager
        client.execute()
        role='instructor' if path.parent.name=='instructor' else 'student'
        nbformat.write(book,out/(role+'-'+path.name))
        results.append(dict(path=str(path.relative_to(root)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),status='passed',exercises='executed' if role=='instructor' else 'disabled: setup only',live_api='not run'))
        print('PASS',path.relative_to(root),flush=True)
(out/'notebook-results.json').write_text(json.dumps({'python':sys.version,'results':results},indent=2)+'\n')
