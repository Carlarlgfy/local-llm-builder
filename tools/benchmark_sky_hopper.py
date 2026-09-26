"""Fresh local-model builds; never patches generated implementation files."""
import argparse
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from local_builder import desktop as app

parser=argparse.ArgumentParser()
parser.add_argument('--model',default='qwen2.5-coder')
parser.add_argument('--runs',type=int,default=2)
args=parser.parse_args()
if not 1<=args.runs<=5:parser.error('--runs must be between 1 and 5')
results=[]
for index in range(args.runs):
    handler=object.__new__(app.Handler);handler.path='/start'
    start=time.monotonic()
    handler.action({'plan':(app.ROOT/'Try Sky Hopper.md').read_text(),'name':'Sky Hopper Validation','destination':str(app.PROJECTS),'language':'static website','model':args.model})
    print('BUILD',index+1,app.STATE['folder'],flush=True)
    seen=0
    while app.BUSY.is_set():
        entries=list(app.STATE.get('log',[]))
        for item in entries[seen:]:print(item,flush=True)
        seen=len(entries);time.sleep(1)
    result={key:app.STATE.get(key) for key in ('folder','status','tasks','error','checkpoint','evidence','verified_fingerprint','acceptance_suite_sha256')}
    result.update(model=args.model,seconds=round(time.monotonic()-start,1),assisted=False)
    results.append(result)
    print('RESULT',json.dumps(result),flush=True)
print('BENCHMARK',json.dumps(results),flush=True)
sys.exit(0 if all(r['status']=='Complete' for r in results) else 1)
