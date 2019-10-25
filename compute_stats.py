
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
parser.add_argument("--input_file", default='data/data_subgoals/out_problems/info.json', type=str)
parser.add_argument("--folder_plans", default='data/data_subgoals/out_plans/', type=str)
parser.add_argument("--folder_stats", default='data/data_subgoals/out_plans/stats/', type=str)



if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.input_file, 'r') as f:
        problem = json.load(f)
    achieved_program = {}
    stats_goal = {}
    for goal in problem:
        goal_name = goal['goal']
        if goal_name.split('_')[0].lower() in ['findnode', 'findclass']:
            goal_name= goal_name.split('_')[0]
        if goal_name not in stats_goal.keys():
            stats_goal[goal_name] = {
                    'success': 0,
                    'total': 0,
                    'length': 0
            }
        stats_goal[goal_name]['total'] = stats_goal[goal_name]['total'] + 1
        out_file = '{}/{}.txt'.format(args.folder_plans, goal['file_name'])
        if os.path.isfile(out_file):
            file_last = out_file.split('/')[-1]
            file_stats = args.folder_stats + file_last + '_stats.txt'
            with open(file_stats, 'r') as f:
                stats = f.readlines()
            with open(out_file, 'r') as f:
                program = f.readlines()
            if goal_name not in achieved_program.keys():
                achieved_program[goal_name] = []
            achieved_program[goal_name].append((program, stats, out_file))
    
    for goal_name in achieved_program.keys():
        nsuccess = len(achieved_program[goal_name])
        stats_goal[goal_name]['success'] = nsuccess
        total_len, total_time = 0, 0
        for prog in achieved_program[goal_name]:
            total_len += len(prog[0])
            output_planner = prog[1]
            time_line = [x for x in output_planner if x.split(':')[0] == 'Total time'][0]
            time = float(time_line.split(':')[1].strip())
            total_time += time

        stats_goal[goal_name]['length'] = total_len*1./nsuccess
        stats_goal[goal_name]['avg_time'] = total_time*1./nsuccess

    ipdb.set_trace()
    os.makedirs(args.folder_stats, exist_ok=True)

    file_stats = '{}/stats.json'.format(args.folder_stats)
    with open(file_stats, 'w+') as f:
        f.write(json.dumps(stats_goal, indent=4))
    
    ipdb.set_trace()
