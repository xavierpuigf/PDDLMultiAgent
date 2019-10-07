import json
from goals_env_parser import *
import utils_env_parser
import glob
import numpy as np
from multiprocessing import Pool
import os
from tqdm import tqdm
import argparse
import pdb

parser = argparse.ArgumentParser()
parser.add_argument("--folder_env", default='input_envs', type=str)
parser.add_argument("--folder_out", default='out_problems', type=str)
parser.add_argument("--problem_name", default='setuptable', type=str)


def parse_env(env_content, goal, goal_name):
    nodes = env_content['nodes']

    header = '''
    (define (problem {})
    (:domain virtualhome)\n
    '''.format(goal_name)

    obj2pddl_map_id = {}

    plates = []
    tables = []

    objects_pddl, obj2pddl_map_id = utils_env_parser.convert_objects_pddl(nodes)

    states_pddl = utils_env_parser.obtain_states_pddl(
            env_content['nodes'], 
            obj2pddl_map_id)

    properties_pddl = utils_env_parser.obtain_properties_pddl(
            env_content['nodes'], 
            obj2pddl_map_id)

    relations_pddl = utils_env_parser.obtain_relations_pddl(
            env_content['edges'], 
            obj2pddl_map_id)

    objects = ["(:objects"]
    objects += ['{} - {}'.format(x,y) for x,y in objects_pddl]
    objects.append(")")
    object_str = '    \n'.join(objects) +'\n'

    init = ['(:init']
    init += ['(= (objects_grabbed) 0)']
    init += states_pddl
    init += ['({} {})'.format(x,y) for x,y in properties_pddl]
    init += ['({} {} {})'.format(x,y,z) for x,y,z in relations_pddl]
    init.append(')')
    init_str = '    \n'.join(init) + '\n'


    goal_str, success = goal.compute_goal(obj2pddl_map_id, env_content)
    if not success:
        return '', False

    goal = ['(:goal']
    goal.append(goal_str)
    goal.append(')')
    goal_str = '    \n'.join(goal)
    final_pddl = header + object_str + init_str + goal_str + '\n)'
    return final_pddl, True

if __name__ == '__main__':
    args = parser.parse_args()
    envs = glob.glob('{}/*.json'.format(args.folder_env))
    info_file_env = []
    file_count = 0
    goals_and_names = [
            ('relax_watch_tv', Relax()), 
            ('table_for_1', TableSet(1)), 
            ('table_for_2', TableSet(2)), 
            ('table_for_3', TableSet(3))
            ] 
    for it, env_file in enumerate(envs):
        with open(env_file, 'r') as f:
            env_content = json.load(f)
        if 'nodes' not in env_content.keys():
            env_content = env_content['init_graph']
        for goal_name, goal in goals_and_names:
            final_pddl, success = parse_env(env_content, goal, goal_name)
            if not success:
                continue
            file_name = 'file_{}'.format(file_count)
            file_out = '{}/{}.pddl'.format(args.folder_out, file_name)
            curr_dict = {'file_name': file_name,
                         'pddl_path': file_out,
                         'env_path': env_file,
                         'goal': goal_name
                         }
            file_count += 1
            info_file_env.append(curr_dict)
            with open(file_out, 'w+') as f:
                f.write(final_pddl)

    with open('{}/info.json'.format(args.folder_out), 'w+') as f:
        f.write(json.dumps(info_file_env, indent=4))
