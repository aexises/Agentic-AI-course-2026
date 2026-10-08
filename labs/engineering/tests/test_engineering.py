import asyncio,importlib,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engineeringlab import checks
from engineeringlab.bench import measure
from engineeringlab.harness import running_service
impl=importlib.import_module(os.getenv('COURSE_SUBMISSION','submission'))

def test_authorization():checks.authorization(impl)
def test_transactions():checks.transactions(impl)
def test_mcp_real_transport():assert asyncio.run(checks.mcp_roundtrip(impl.__name__))['real_mcp_stdio']
def test_migration():checks.migration(impl)
def test_release_gate():checks.releases(impl)
def test_measurements():checks.measurements(impl)
def test_actual_http_measurement():
    with running_service(impl.__name__) as url:
        rows=measure(url,n=4,workers=2)
    assert len(rows)==4 and all(r['success'] for r in rows)
    assert impl.summarize(rows)['attempted']==4


def test_trace_allowlist():
    event=impl.trace_event('r1','/tickets/{operation_id}',403,2.5,'v1',headers={'secret':'private'},body='private')
    assert set(event)=={'request_id','route','status','latency_ms','release'}
    assert 'private' not in str(event)
    for bad in (True,99,600):
        try:impl.trace_event('r','/health',bad,1,'v1')
        except ValueError:pass
        else:raise AssertionError('invalid HTTP status accepted')

def test_concurrent_duplicate():
    import tempfile
    from concurrent.futures import ThreadPoolExecutor
    from engineeringlab.support import initialize,connect
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'ledger.sqlite';initialize(path)
        def send(_):
            with connect(path) as conn:
                return impl.commit_ticket(conn,'alpha',{'operation_id':'parallel','resource':'camera','summary':'repair'})
        with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(send,range(2)))
        assert len({r['ticket_id'] for r in results})==1
        assert sum(not r['replayed'] for r in results)==1
        with connect(path) as conn:assert conn.execute('SELECT count(*) FROM tickets').fetchone()[0]==1

def test_http_approval_binding():
    import httpx
    with running_service(impl.__name__) as url,httpx.Client(base_url=url) as client:
        body={'operation_id':'bound','resource':'camera','summary':'repair'}
        agent={'X-API-Key':'alpha-demo'}
        assert client.post('/tickets',json=body).status_code==401
        assert client.post('/tickets',json=dict(body,approved=True),headers=agent).status_code==422
        assert client.post('/approvals',json=body,headers={'X-API-Key':'alpha-reviewer-demo'}).status_code==200
        assert client.post('/tickets',json=dict(body,summary='changed'),headers=agent).status_code==403
        assert client.get('/tickets/bound',headers=agent).status_code==404
