
# usage ./planner.py domain.pddl problem.pddl plan.ipc
import os
import pdb
import utils_env_parser
import urllib.request as urllibreq
import planner
import urllib
import argparse
import json, sys


parser = argparse.ArgumentParser()
parser.add_argument("--domain_name", default='domain.pddl', type=str)
parser.add_argument("--input_file", default='out_problems/info.json', type=str)
parser.add_argument("--folder_out", default='out', type=str)

def solve_plan(info):
    problem_name = info['pddl_path']
    out_name = '{}/{}.txt'.format(args.folder_out, info['file_name'])
    planner.local_planner(args.domain_name, problem_name, out_name)

if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.input_file, 'r') as f:
        file_plans = json.load(f)
    pool = Pool(20)
    p.map(solve_plan, file_plans)
    pdb.set_trace()


