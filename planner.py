# usage ./planner.py domain.pddl problem.pddl plan.ipc
import pdb
import urllib.request as urllibreq
import urllib
import json, sys

data = {'domain': open(sys.argv[1], 'r').read(),
        'problem': open(sys.argv[2], 'r').read()}

req = urllibreq.Request('http://solver.planning.domains/solve')
req.add_header('Content-Type', 'application/json; charset=utf-8')
data_pddl = json.dumps(data)
data = data_pddl.encode("utf-8")
resp = json.loads(urllibreq.urlopen(req, data).read())
program = []
if resp['status'] == 'ok':
    plan = resp['result']['plan']
    print('Plan succeeded:')
    for x in plan:
        if type(x) == str:
            program.append(x)
        else:
            program.append(x['name'])
else:
    print(resp['result'])
pdb.set_trace()
with open(sys.argv[3], 'w') as f:
    f.write('\n'.join(program))
