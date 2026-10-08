"""Bounded real HTTP load experiment; no model or dollar-cost claim."""
import time
from concurrent.futures import ThreadPoolExecutor
import httpx

def measure(url,n=20,workers=2):
    if type(n) is not int or not 1<=n<=100 or type(workers) is not int or not 1<=workers<=8:raise ValueError('invalid workload')
    def request(i):
        start=time.perf_counter()
        try:
            with httpx.Client(timeout=3) as client:
                response=client.get(url+'/health')
            success=response.status_code==200;error=None if success else str(response.status_code)
        except httpx.HTTPError as exc:success=False;error=type(exc).__name__
        return {'success':success,'latency_ms':1000*(time.perf_counter()-start),'cost':0.,'error':error}
    with ThreadPoolExecutor(max_workers=workers) as executor:return list(executor.map(request,range(n)))
