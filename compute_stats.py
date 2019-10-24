
# usage ./planner.py domain.pddl problem.pddl plan.ipc
import os
import pdb
import utils_env_parser
import urllib.request as urllibreq
import planner
import urllib
import argparse
import ipdb
from multiprocessing import Pool

import json, sys


parser = argparse.ArgumentParser()
parser.add_argument("--input_file", default='data/out_problems/info.json', type=str)
parser.add_argument("--folder_plans", default='data/out_plans/', type=str)



if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.input_file, 'r') as f:
        problem = json.load(f)
    achieved_program = {}
    for goal in problem:
        goal_name = goal['goal']
        out_file = '{}/{}.txt'.format(args.folder_plans, goal['file_name'])
        if os.path.isfile(out_file):
            file_stats = out_file + '_stats.txt'
            with open(file_stats, 'r') as f:
                stats = f.readlines()
            with open(out_file, 'r') as f:
                program = f.readlines()
            if goal_name not in achieved_program.keys():
                achieved_program[goal_name] = []
            achieved_program[goal_name].append((program, stats, out_file))
    ipdb.set_trace()
