# usage ./planner.py domain.pddl problem.pddl plan.ipc
import subprocess
import os
import pdb
import utils_env_parser
import urllib.request as urllibreq
import urllib
import argparse
import json, sys


parser = argparse.ArgumentParser()
parser.add_argument("--domain_name", default='domain.pddl', type=str)
parser.add_argument("--problem_name", default='example_problem/example_problem.pddl', type=str)
parser.add_argument("--file_out", default='out', type=str)

def online_planner(domain_name, problem_name, file_out):
    data = {'domain': open(domain_name, 'r').read(),
            'problem': open(problem_name, 'r').read()}
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
    program = utils_env_parser.convert_to_virtualhome_program(program)
    program = [x+'\n' for x in program]
    with open(file_out, 'w+') as f:
        f.writelines(program)

def local_planner(domain_name, problem_name, file_out):
    # Based on: https://github.com/LAPKT-dev/LAPKT-public/tree/master/planners/siw_plus-then-bfs_f-ffparser
    # ./sw+bfsf/siw-then-bfsf --domain domain.pddl --problem example_out.pddl out_ex
    #os.system('./sw+bfsf/siw-then-bfsf --domain {} --problem {} --output {}'.format(domain_name, problem_name, file_out))
    with open(file_out + '_stats.txt', 'w+') as outfile:
        proc = subprocess.call(['./sw+bfsf/siw-then-bfsf', '--domain', domain_name, '--problem', problem_name, '--output', file_out], stdout=outfile)
    with open(file_out, 'r') as f:
        program = f.readlines()
        if len(program) == 0:
            return
        if len(program[-1]) == 0:
            program = program[:-1]
    program = utils_env_parser.convert_to_virtualhome_program(program)
    program = [x+'\n' for x in program]
    if len(program) > 0:
        with open(file_out, 'w+') as f:
            f.writelines(program)

if __name__ ==  '__main__':
    args = parser.parse_args()
    local_planner(args.domain_name, args.problem_name, args.file_out)
    #online_planner(args.domain_name, args.problem_name, args.file_out)
