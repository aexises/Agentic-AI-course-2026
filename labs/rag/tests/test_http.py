"""Real TCP smoke test; start only a temporary course Uvicorn process."""
import os
import socket
import subprocess
import sys
import time
import httpx


def test_uvicorn_network_round_trip(tmp_path):
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0))
        port=sock.getsockname()[1]
    env=dict(os.environ,RAG_API_KEYS='{"network-alpha":"alpha","network-beta":"beta"}',HF_HUB_OFFLINE='1')
    log=tmp_path/'uvicorn.log'
    with log.open('w') as stream:
        process=subprocess.Popen([sys.executable,'-m','uvicorn','raglab.service:create_app','--factory','--host','127.0.0.1','--port',str(port)],env=env,stdout=stream,stderr=subprocess.STDOUT)
        try:
            with httpx.Client(base_url=f'http://127.0.0.1:{port}',timeout=10) as client:
                for _ in range(300):
                    if process.poll() is not None:
                        raise AssertionError('Uvicorn failed: '+log.read_text()[-2000:])
                    try:
                        if client.get('/health').status_code==200:break
                    except httpx.ConnectError:pass
                    time.sleep(.1)
                else:raise AssertionError('Uvicorn readiness timeout')
                assert client.get('/openapi.json').status_code==200
                response=client.post('/search',headers={'X-API-Key':'network-alpha'},json={'query':'E-204','k':3,'rerank':True})
                assert response.status_code==200,response.text
                assert response.json()['hits']
                assert all('BETA-ONLY-MARKER' not in h['text'] for h in response.json()['hits'])
                assert client.post('/search',json={'query':'camera'}).status_code==401
        finally:
            process.terminate()
            try:process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill();process.wait(timeout=5)
