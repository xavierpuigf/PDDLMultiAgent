import json
import numpy as np
import numpy.random as random
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
parser.add_argument("--folder_env", default='data/data_subgoals/input_envs', type=str)
parser.add_argument("--folder_out", default='data/data_subgoals/out_problems', type=str)



if __name__ == '__main__':
    args = parser.parse_args()
    os.makedirs(args.folder_out, exist_ok=True)
    envs = glob.glob('{}/*.json'.format(args.folder_env))
    info_file_env = []
    file_count = 0
    for it, env_file in enumerate(tqdm(envs)):
        with open(env_file, 'r') as f:
            env_content = json.load(f)
        if 'nodes' not in env_content.keys():
            env_content = env_content['init_graph']
        
        nodes = [x for x in env_content['nodes'] if x['class_name'] not in ['wall', 'ceiling', 'floor']]
        node_ids = [x['id'] for x in nodes]
        class_names = list(set([x['class_name'] for x in nodes]))

        # Choose 5 nodes and 5 class names
        nodes_selected = random.choice(node_ids, 5)
        classes_selected = random.choice(class_names, 5)
        goals_and_names = [('findnode_{}'.format(x), Findnode(x)) for x in nodes_selected]
        goals_and_names += [('findclass_{}'.format(x), Findclass(x)) for x in classes_selected]
        
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
