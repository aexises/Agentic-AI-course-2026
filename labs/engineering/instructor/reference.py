import json, math, statistics, uuid
from engineeringlab.support import Conflict

def authorize(resources,resource,approved):
    return type(approved) is bool and approved and isinstance(resource,str) and resource in resources

def commit_ticket(conn,tenant,body):
    payload=json.dumps({'resource':body['resource'],'summary':body['summary']},sort_keys=True)
    try:
        conn.execute('BEGIN IMMEDIATE')
        old=conn.execute('SELECT payload,ticket_id FROM tickets WHERE tenant=? AND operation_id=?',(tenant,body['operation_id'])).fetchone()
        if old:
            if old['payload']!=payload:raise Conflict()
            result={'ticket_id':old['ticket_id'],'replayed':True}
        else:
            ticket_id=str(uuid.uuid4())
            conn.execute('INSERT INTO tickets(tenant,operation_id,payload,ticket_id) VALUES(?,?,?,?)',(tenant,body['operation_id'],payload,ticket_id))
            result={'ticket_id':ticket_id,'replayed':False}
        conn.commit()
        return result
    except Exception:
        conn.rollback();raise

def register_tools(server,client):
    @server.tool()
    def create_ticket(operation_id:str,resource:str,summary:str)->dict:
        response=client.post('/tickets',json={'operation_id':operation_id,'resource':resource,'summary':summary})
        response.raise_for_status();return response.json()
    @server.tool()
    def ticket_status(operation_id:str)->dict:
        response=client.get('/tickets/'+operation_id)
        response.raise_for_status();return response.json()

def release_gate(report):
    required={'tests','failures','unauthorized_effects','replay_duplicates'}
    return (isinstance(report,dict) and set(report)==required
            and all(type(report[k]) is int and report[k]>=0 for k in required)
            and report['tests']>0 and all(report[k]==0 for k in required-{'tests'}))

def summarize(rows):
    for row in rows:
        if type(row['success']) is not bool:raise ValueError('invalid success')
        for key in ('latency_ms','cost'):
            v=row[key]
            if type(v) not in (int,float) or not math.isfinite(v) or v<0:raise ValueError('invalid measurement')
    n=len(rows);successes=sum(r['success'] for r in rows)
    times=sorted(r['latency_ms'] for r in rows);total=sum(r['cost'] for r in rows)
    return {'attempted':n,'successes':successes,'success_rate':successes/n if n else None,
            'p50_ms':statistics.median(times) if n else None,'p95_ms':times[math.ceil(.95*n)-1] if n else None,
            'total_cost':total,'cost_per_success':total/successes if successes else None}

def cache_key(tenant,resource,version):
    if any(not isinstance(v,str) or not v.strip() for v in (tenant,resource)) or type(version) is not int or version<1:
        raise ValueError('invalid cache identity')
    return tenant,resource,version

def upgrade_schema(conn):
    try:
        conn.execute('BEGIN IMMEDIATE')
        names={r['name'] for r in conn.execute('PRAGMA table_info(tickets)')}
        if 'created_by' not in names:
            conn.execute("ALTER TABLE tickets ADD COLUMN created_by TEXT NOT NULL DEFAULT 'legacy'")
        conn.execute('INSERT OR IGNORE INTO schema_version VALUES(2)')
        conn.commit()
    except Exception:conn.rollback();raise


def trace_event(request_id,route,status,latency_ms,release,**untrusted):
    if any(not isinstance(v,str) or not v.strip() for v in (request_id,route,release)):
        raise ValueError('invalid trace identity')
    if type(status) is not int or not 100<=status<=599:raise ValueError('invalid status')
    if type(latency_ms) not in (int,float) or not math.isfinite(latency_ms) or latency_ms<0:
        raise ValueError('invalid duration')
    return dict(request_id=request_id,route=route,status=status,latency_ms=latency_ms,release=release)
