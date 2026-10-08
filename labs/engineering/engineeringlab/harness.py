"""Launch only temporary local teaching processes and remove their private database."""
import os,socket,subprocess,sys,tempfile,time
from contextlib import contextmanager
from pathlib import Path
import httpx
ROOT=Path(__file__).resolve().parents[1]

@contextmanager
def running_service(module='submission'):
    with tempfile.TemporaryDirectory(prefix='course-ticket-') as tmp:
        with socket.socket() as sock:
            sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        env=dict(os.environ,COURSE_SUBMISSION=module,COURSE_TICKET_DB=str(Path(tmp)/'ledger.sqlite'))
        url=f'http://127.0.0.1:{port}'
        with (Path(tmp)/'server.log').open('w') as log:
            proc=subprocess.Popen([sys.executable,'-m','uvicorn','engineeringlab.support:create_app','--factory','--host','127.0.0.1','--port',str(port)],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
            try:
                with httpx.Client(base_url=url,timeout=3) as client:
                    for _ in range(150):
                        if proc.poll() is not None:raise RuntimeError('Course server exited during startup')
                        try:
                            if client.get('/health').status_code==200:break
                        except httpx.ConnectError:pass
                        time.sleep(.1)
                    else:raise RuntimeError('Course server readiness timeout')
                yield url
            finally:
                proc.terminate()
                try:proc.wait(timeout=5)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
