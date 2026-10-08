"""Local teaching service. API keys select tenants; caller input cannot select one."""
import hmac
import json
import os
import threading
from contextlib import asynccontextmanager
from typing import Annotated, Literal
from fastapi import FastAPI, Header, HTTPException, Depends, Request
from pydantic import BaseModel, ConfigDict, Field, field_validator
from psycopg_pool import ConnectionPool, PoolTimeout
from psycopg import OperationalError
from psycopg.errors import QueryCanceled
from psycopg.rows import dict_row
from pgvector.psycopg import register_vector
from .config import database_url
from . import models
from .retrieval import retrieve

class SearchRequest(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    query: str = Field(min_length=1,max_length=1000)
    k: int = Field(default=5,ge=1,le=20)
    mode: Literal['dense','lexical','hybrid']='hybrid'
    rerank: bool=False
    @field_validator('query')
    @classmethod
    def nonblank(cls,value):
        if not value.strip(): raise ValueError('query cannot be blank')
        return value.strip()

class Hit(BaseModel):
    chunk_id: str
    doc_id: str
    text: str

class SearchResponse(BaseModel):
    hits: list[Hit]
    mode: str
    reranked: bool


def api_keys():
    raw=os.getenv('RAG_API_KEYS')
    if not raw: raise RuntimeError('Set RAG_API_KEYS to a JSON object of key:tenant mappings')
    keys=json.loads(raw)
    if not isinstance(keys,dict) or not keys or any(not isinstance(k,str) or not k or not isinstance(v,str) or not v for k,v in keys.items()):
        raise ValueError('invalid API key configuration')
    return keys

def configure_connection(conn):
    register_vector(conn)
    conn.commit()

def create_app(keys=None):
    keys=api_keys() if keys is None else keys
    @asynccontextmanager
    async def lifespan(app):
        models.encoder(); models.cross_encoder()
        with ConnectionPool(database_url(),min_size=1,max_size=4,timeout=2,
                            kwargs={'row_factory':dict_row,'connect_timeout':5},
                            configure=configure_connection,open=True) as pool:
            pool.wait(timeout=10)
            app.state.pool=pool
            app.state.slots=threading.BoundedSemaphore(2)
            yield
    app=FastAPI(title='Course retrieval service',lifespan=lifespan)
    def tenant(x_api_key: Annotated[str | None, Header()]=None):
        if x_api_key is not None:
            for key,value in keys.items():
                if hmac.compare_digest(x_api_key.encode(),key.encode()): return value
        raise HTTPException(401,'Invalid API key')
    app.state.tenant_dependency=tenant

    @app.get('/health')
    def health(request:Request):
        try:
            with request.app.state.pool.connection() as conn: conn.execute('SELECT 1')
        except (OperationalError,PoolTimeout): raise HTTPException(503,'Database unavailable') from None
        return {'status':'ready'}

    @app.post('/search',response_model=SearchResponse)
    def search(body:SearchRequest,request:Request,owner:Annotated[str,Depends(tenant)]):
        if not request.app.state.slots.acquire(blocking=False): raise HTTPException(503,'Server busy')
        try:
            with request.app.state.pool.connection() as conn:
                rows=retrieve(conn,owner,body.query,body.k,body.mode,body.rerank)
            return SearchResponse(hits=[Hit(**{k:r[k] for k in Hit.model_fields}) for r in rows],mode=body.mode,reranked=body.rerank)
        except (OperationalError,PoolTimeout,QueryCanceled):
            raise HTTPException(503,'Retrieval temporarily unavailable') from None
        finally:
            request.app.state.slots.release()
    return app
