"""Local ticket service scaffolding. SQLite is the action ledger; RAG stays in pgvector."""
import json
import logging
import time
import uuid
import importlib
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field

class Ticket(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    operation_id: str=Field(min_length=1,max_length=80,pattern=r'^[a-zA-Z0-9_-]+$')
    resource: str=Field(min_length=1,max_length=100)
    summary: str=Field(min_length=1,max_length=300)

class Conflict(Exception):pass
class Denied(Exception):pass

@contextmanager
def connect(path):
    conn=sqlite3.connect(path,timeout=5)
    conn.row_factory=sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()

def initialize(path):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with connect(path) as conn:
        conn.executescript('''CREATE TABLE IF NOT EXISTS schema_version(version INTEGER PRIMARY KEY);
        INSERT OR IGNORE INTO schema_version VALUES(1);
        CREATE TABLE IF NOT EXISTS approvals(tenant TEXT NOT NULL, operation_id TEXT NOT NULL, payload TEXT NOT NULL, PRIMARY KEY(tenant,operation_id));
        CREATE TABLE IF NOT EXISTS tickets(
          tenant TEXT NOT NULL, operation_id TEXT NOT NULL, payload TEXT NOT NULL,
          ticket_id TEXT NOT NULL, PRIMARY KEY(tenant, operation_id));''')

def create_app(module=None,path=None):
    implementation=importlib.import_module(module or os.environ.get('COURSE_SUBMISSION','submission'))
    path=path or os.environ.get('COURSE_TICKET_DB','student-results/tickets.sqlite')
    initialize(path)
    app=FastAPI(title='Course ticket service',version=os.environ.get('COURSE_RELEASE','dev'))
    if os.environ.get('COURSE_TRACE')=='1':
        # Enable after TODO 20.3. Route templates avoid logging path parameters.
        @app.middleware('http')
        async def observe(request,call_next):
            request_id=str(uuid.uuid4());start=time.perf_counter();status=500
            try:
                response=await call_next(request);status=response.status_code
                response.headers['X-Request-ID']=request_id
                return response
            finally:
                route=getattr(request.scope.get('route'),'path','unmatched')
                event=implementation.trace_event(request_id,route,status,(time.perf_counter()-start)*1000,app.version)
                logging.getLogger('uvicorn.error').info(json.dumps(event,sort_keys=True))
    # Public local teaching keys. This is not an OAuth or production identity system.
    identities={'alpha-demo':('alpha',{'camera'}),'beta-demo':('beta',{'microphone'})}
    def identity(key):
        if key not in identities:raise HTTPException(401,'Unknown teaching key')
        return identities[key]
    @app.get('/health')
    def health():
        with connect(path) as conn:conn.execute('SELECT 1 FROM schema_version').fetchone()
        return {'status':'ready','release':app.version}
    @app.post('/approvals')
    def approve(body:Ticket,x_api_key:str|None=Header(default=None)):
        reviewers={'alpha-reviewer-demo':('alpha',{'camera'}),'beta-reviewer-demo':('beta',{'microphone'})}
        if x_api_key not in reviewers:raise HTTPException(403,'Reviewer key required')
        tenant,resources=reviewers[x_api_key]
        if body.resource not in resources:raise HTTPException(403,'Resource denied')
        payload=json.dumps({'resource':body.resource,'summary':body.summary},sort_keys=True)
        with connect(path) as conn:
            conn.execute('INSERT INTO approvals VALUES(?,?,?) ON CONFLICT(tenant,operation_id) DO UPDATE SET payload=excluded.payload',(tenant,body.operation_id,payload))
        return {'approved_operation':body.operation_id}
    @app.post('/tickets')
    def create(body:Ticket,x_api_key:str|None=Header(default=None)):
        tenant,resources=identity(x_api_key)
        payload=json.dumps({'resource':body.resource,'summary':body.summary},sort_keys=True)
        with connect(path) as conn:
            receipt=conn.execute('SELECT payload FROM approvals WHERE tenant=? AND operation_id=?',(tenant,body.operation_id)).fetchone()
        approved=receipt is not None and receipt['payload']==payload
        if not implementation.authorize(resources,body.resource,approved):raise HTTPException(403,'Action denied')
        try:
            with connect(path) as conn:return implementation.commit_ticket(conn,tenant,body.model_dump())
        except Conflict:raise HTTPException(409,'Operation ID reused with different content') from None
    @app.get('/tickets/{operation_id}')
    def status(operation_id:str,x_api_key:str|None=Header(default=None)):
        tenant,_=identity(x_api_key)
        with connect(path) as conn:
            row=conn.execute('SELECT ticket_id FROM tickets WHERE tenant=? AND operation_id=?',(tenant,operation_id)).fetchone()
        if row is None:raise HTTPException(404,'Unknown operation')
        return {'ticket_id':row['ticket_id']}
    return app
