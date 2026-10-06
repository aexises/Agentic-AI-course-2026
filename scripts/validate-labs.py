"""Validate and execute each notebook in a fresh kernel, with all live calls off."""
import json, os, sys, tempfile, hashlib
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager

root=Path(__file__).resolve().parents[1]
results=[]
with tempfile.TemporaryDirectory(prefix='lab-kernels-') as tmp:
    kernel=Path(tmp)/'course-validation'
    kernel.mkdir()
    (kernel/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Course validation','language':'python'}))
    manager=KernelSpecManager(kernel_dirs=[tmp])
    # The framework track has its own pinned environment and validator.
    paths = sorted((root/'labs').glob('*.ipynb')) + sorted((root/'labs'/'instructor').glob('*.ipynb'))
    for path in paths:
        notebook=nbformat.read(path,as_version=4)
        nbformat.validate(notebook)
        assert all('RUN_LIVE = True' not in c.source for c in notebook.cells if c.cell_type=='code')
        client=NotebookClient(notebook,timeout=120,kernel_name='course-validation',resources={'metadata':{'path':str(path.parent)}})
        client.km=client.create_kernel_manager()
        client.km.kernel_spec_manager=manager
        client.execute()
        # Store evidence outside distributed notebooks, which stay clear of machine-specific outputs.
        dest=root/'improvements'/'validation'/(('instructor-' if path.parent.name=='instructor' else 'student-')+path.name)
        dest.parent.mkdir(exist_ok=True)
        nbformat.write(notebook,dest)
        results.append({'notebook':str(path.relative_to(root)),'status':'passed','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                        'code_cells':sum(c.cell_type=='code' for c in notebook.cells),'live_api':'not run',
                        'exercises':('executed' if path.parent.name=='instructor' else 'worked foundation checks' if path.name.startswith(('03_','04_')) else 'intentionally disabled')})
        print('PASS',path.relative_to(root),flush=True)
(root/'improvements'/'validation'/'notebook-results.json').write_text(json.dumps({'python':sys.version,'results':results},indent=2)+'\n')
