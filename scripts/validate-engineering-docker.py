"""Isolated reference-image validation; retains its separately named test volume."""
import os,json,shutil,subprocess,tempfile,time
from pathlib import Path
import httpx
root=Path(__file__).resolve().parents[1]/'labs/engineering'
out=root/'validation';out.mkdir(exist_ok=True)
report={'scope':'instructor implementation in isolated temporary build context','checks':[]}
with tempfile.TemporaryDirectory(prefix='course-delivery-') as tmp:
    ctx=Path(tmp)
    for name in ('Dockerfile','requirements-service.txt','.dockerignore','compose.yaml'):shutil.copy(root/name,ctx/name)
    shutil.copytree(root/'engineeringlab',ctx/'engineeringlab',ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy(root/'instructor/reference.py',ctx/'submission.py')
    compose=(ctx/'compose.yaml').read_text().replace('course-engineering:${','course-engineering-validation:${')
    (ctx/'compose.yaml').write_text(compose)
    log=open(out/'docker-validation.log','w')
    def run(args,release='v1',capture=False):
        env=dict(os.environ,COURSE_RELEASE=release,COURSE_TRACE='1')
        cmd=['docker','compose','-p','course-engineering-validation']+args
        p=subprocess.run(cmd,cwd=ctx,env=env,text=True,stdout=subprocess.PIPE if capture else log,stderr=log,check=True)
        return p.stdout if capture else None
    try:
        run(['build']);run(['up','-d','--wait'])
        with httpx.Client(base_url='http://127.0.0.1:58018',timeout=5) as client:
            body={'operation_id':'docker-probe','resource':'camera','summary':'repair'}
            agent={'X-API-Key':'alpha-demo'}
            assert client.get('/health').json()['release']=='v1'
            assert client.post('/tickets',json=body,headers=agent).status_code==403
            assert client.post('/approvals',json=body,headers={'X-API-Key':'alpha-reviewer-demo'}).status_code==200
            first=client.post('/tickets',json=body,headers=agent);first.raise_for_status()
            ticket=first.json()['ticket_id'];request_id=first.headers['x-request-id']
            assert client.post('/tickets',json=body,headers=agent).json()['ticket_id']==ticket
            report['checks']+=['v1 image build and readiness','denial before approval','approved create and identical replay']
            migrate="import os; from engineeringlab.support import connect; from submission import upgrade_schema\nwith connect(os.environ['COURSE_TICKET_DB']) as c:\n upgrade_schema(c); upgrade_schema(c)\n print([tuple(r) for r in c.execute('PRAGMA table_info(tickets)')])"
            report['migration_schema']=run(['exec','-T','api','python','-c',migrate],capture=True)
            run(['build'],release='v2');run(['up','-d','--wait'],release='v2')
            assert client.get('/health').json()['release']=='v2'
            assert client.post('/tickets',json=body,headers=agent).json()['ticket_id']==ticket
            report['checks']+=['additive migration repeated','v2 replacement preserves ticket']
            run(['up','-d','--no-build','--wait'],release='v1')
            assert client.get('/health').json()['release']=='v1'
            assert client.post('/tickets',json=body,headers=agent).json()['ticket_id']==ticket
            new=dict(body,operation_id='after-rollback')
            assert client.post('/approvals',json=new,headers={'X-API-Key':'alpha-reviewer-demo'}).status_code==200
            assert client.post('/tickets',json=new,headers=agent).status_code==200
            last=client.get('/tickets/after-rollback',headers=agent)
            log_id=last.headers['x-request-id']
            logs=run(['logs','--no-color','api'],capture=True)
            assert log_id in logs and '"route": "/tickets/{operation_id}"' in logs
            assert 'alpha-demo' not in logs and 'alpha-reviewer-demo' not in logs
            report['checks']+=['rollback to v1 compatible with migrated schema','new insert after rollback','real request ID correlated with template-route JSON log']
            report['images']=subprocess.check_output(['docker','image','inspect','course-engineering-validation:v1','course-engineering-validation:v2','--format','{{.Id}}'],text=True).splitlines()
            report['note']='v1/v2 use same business implementation with different release metadata; gate contract tested separately; no broken application image deployed'
    finally:
        run(['down'])
        log.close()
report['status']='passed'
report['cleanup']='validation stack stopped; course-engineering-validation_ticket-data volume retained'
(out/'docker-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
