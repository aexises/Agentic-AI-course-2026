"""Visible contract checks. Add new cases; these checks are not exhaustive."""
import json,os,sys,tempfile
from pathlib import Path
import httpx
from mcp import Client,StdioServerParameters
from .support import connect,initialize,Conflict
from .harness import ROOT,running_service

def authorization(impl):
    assert impl.authorize({'camera'},'camera',True)
    for resource,approval in [('camera',False),('camera',1),('camera','yes'),('microphone',True)]:
        assert not impl.authorize({'camera'},resource,approval)

def transactions(impl):
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'ledger.sqlite';initialize(path)
        body={'operation_id':'same','resource':'camera','summary':'repair'}
        with connect(path) as conn:
            first=impl.commit_ticket(conn,'alpha',body)
            second=impl.commit_ticket(conn,'alpha',body)
            assert first['ticket_id']==second['ticket_id'] and not first['replayed'] and second['replayed']
            try:impl.commit_ticket(conn,'alpha',dict(body,summary='changed'))
            except Conflict:pass
            else:raise AssertionError('conflicting replay accepted')
            assert conn.execute('SELECT count(*) FROM tickets').fetchone()[0]==1
            third=impl.commit_ticket(conn,'beta',body)
            assert third['ticket_id']!=first['ticket_id']
        with connect(path) as conn:
            assert impl.commit_ticket(conn,'alpha',body)['ticket_id']==first['ticket_id']

async def mcp_roundtrip(module):
    with running_service(module) as url:
        body={'operation_id':'replay','resource':'camera','summary':'camera repair'}
        with httpx.Client(base_url=url,timeout=3) as http:
            assert http.post('/tickets',headers={'X-API-Key':'alpha-demo'},json=body).status_code==403
            assert http.post('/approvals',headers={'X-API-Key':'alpha-demo'},json=body).status_code==403
            assert http.post('/approvals',headers={'X-API-Key':'alpha-reviewer-demo'},json=body).status_code==200
            env=dict(os.environ,COURSE_SUBMISSION=module,COURSE_API_URL=url,COURSE_API_KEY='alpha-demo')
            params=StdioServerParameters(command=sys.executable,args=['-m','engineeringlab.server'],cwd=str(ROOT),env=env)
            async with Client(params) as client:
                tools=await client.list_tools()
                assert {'create_ticket','ticket_status'}<={t.name for t in tools.tools}
                first=await client.call_tool('create_ticket',body)
                second=await client.call_tool('create_ticket',body)
                assert not first.is_error and not second.is_error
                # Compare authoritative service state; response wrapper varies by tool schema.
                state=http.get('/tickets/replay',headers={'X-API-Key':'alpha-demo'})
                assert state.status_code==200
                assert http.get('/tickets/replay',headers={'X-API-Key':'beta-demo'}).status_code==404
                denied=await client.call_tool('create_ticket',dict(body,operation_id='unapproved'))
                assert denied.is_error
                assert http.get('/tickets/unapproved',headers={'X-API-Key':'alpha-demo'}).status_code==404
        return {'real_http':True,'real_mcp_stdio':True,'approval_checked':True,'tenant_isolation':True}

def migration(impl):
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'ledger.sqlite';initialize(path)
        with connect(path) as conn:
            body={'operation_id':'pre','resource':'camera','summary':'before migration'}
            first=impl.commit_ticket(conn,'alpha',body)
            impl.upgrade_schema(conn);impl.upgrade_schema(conn)
            row=conn.execute('SELECT * FROM tickets').fetchone()
            assert row['created_by']=='legacy' and row['ticket_id']==first['ticket_id']
            assert impl.commit_ticket(conn,'alpha',body)['replayed']
            assert not impl.commit_ticket(conn,'alpha',dict(body,operation_id='post'))['replayed']

def releases(impl):
    good={'tests':12,'failures':0,'unauthorized_effects':0,'replay_duplicates':0}
    assert impl.release_gate(good)
    for bad in [dict(good,tests=0),dict(good,tests=True),dict(good,failures=1),dict(good,unauthorized_effects=1),dict(good,replay_duplicates=1),{},None]:
        assert not impl.release_gate(bad)

def measurements(impl):
    rows=[{'success':True,'latency_ms':2.,'cost':.3},{'success':False,'latency_ms':10.,'cost':.2}]
    result=impl.summarize(rows)
    assert result=={'attempted':2,'successes':1,'success_rate':.5,'p50_ms':6.,'p95_ms':10.,'total_cost':.5,'cost_per_success':.5}
    assert impl.summarize([])['p95_ms'] is None
    assert impl.summarize([rows[1]])['cost_per_success'] is None
    for bad in [-1,float('nan'),float('inf'),True]:
        try:impl.summarize([dict(rows[0],latency_ms=bad)])
        except ValueError:pass
        else:raise AssertionError('invalid time accepted')
    assert impl.cache_key('alpha','camera',1)!=impl.cache_key('beta','camera',1)
    assert impl.cache_key('alpha','camera',1)!=impl.cache_key('alpha','camera',2)
