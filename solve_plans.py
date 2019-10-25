
# usage ./planner.py domain.pddl problem.pddl plan.ipc
from tqdm import tqdm
import os
import pdb
import utils_env_parser
import urllib.request as urllibreq
import planner
import urllib
import argparse
from multiprocessing import Pool

import json, sys


parser = argparse.ArgumentParser()
parser.add_argument("--domain_name", default='domain.pddl', type=str)
parser.add_argument("--input_file", default='data/data_subgoals/out_problems/info.json', type=str)
parser.add_argument("--folder_out", default='data/data_subgoals/out_plans/', type=str)

def solve_plan(info):
    problem_name = info['pddl_path']
    out_name = '{}/{}.txt'.format(args.folder_out, info['file_name'])
    planner.local_planner(args.domain_name, problem_name, out_name)

if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.input_file, 'r') as f:
        file_plans = json.load(f)
    p = Pool(20)
    for _ in tqdm(p.imap_unordered(solve_plan, file_plans)):
        pass
    pdb.set_trace()


