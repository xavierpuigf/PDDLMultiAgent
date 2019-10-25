import subprocess
import shutil
import os
import pdb
import utils_env_parser
import urllib.request as urllibreq
import urllib
import argparse
import json, sys


parser = argparse.ArgumentParser()
parser.add_argument("--dset_folder", default='data/data_subgoals/', type=str)
parser.add_argument("--file_out", default='../dataset_subgoals', type=str)



if __name__ ==  '__main__':
    args = parser.parse_args()
    info_dataset = {}
    info_file = '{}/out_problems/info.json'.format(args.dset_folder)
    with open(info_file, 'r') as f:
        info_file = json.load(f)
    
    
    os.makedirs(args.file_out, exist_ok=True)
    info = []
    for dp in info_file:
        program_file = '{}/out_plans/{}.txt'.format(args.dset_folder, dp['file_name'])
        if os.path.isfile(program_file):
            curr_env_path = dp['env_path']
            new_env_path = '{}/init_envs/{}'.format(args.file_out, curr_env_path.split('/')[-1])
            new_file_path = '{}/programs/{}'.format(args.file_out, dp['file_name'])
            info_elem = {}
            info_elem['env_path'] = curr_env_path.split('/')[-1]
            info_elem['program'] = dp['file_name']
            #info_elem['goal_file'] = dp['file_name']
            info_elem['goal'] = dp['goal']
            
            os.makedirs(os.path.dirname(new_env_path), exist_ok=True)
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            #os.makedirs(os.path.dirname(new_goal_path), exist_ok=True)
            info.append(info_elem)
            


            if not os.path.isfile(new_env_path):
                shutil.copy(curr_env_path, new_env_path)
            if not os.path.isfile(new_file_path+'.txt'):
                shutil.copy(program_file, new_file_path+'.txt')

    with open('{}/info.json'.format(args.file_out), 'w+') as f:
        f.write(json.dumps(info))
