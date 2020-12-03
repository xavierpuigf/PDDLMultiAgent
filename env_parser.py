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
parser.add_argument("--folder_env", default='data_example/input_envs', type=str)
parser.add_argument("--folder_out", default='data_example/out_problems', type=str)



if __name__ == '__main__':
    args = parser.parse_args()
    os.makedirs(args.folder_out, exist_ok=True)
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
            final_pddl, success = utils_env_parser.parse_env(env_content, goal, goal_name)
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
