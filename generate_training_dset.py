import subprocess
import shutil
import os
import pdb
import utils_env_parser
from tqdm import tqdm
import urllib.request as urllibreq
import urllib
import argparse
import json, sys


parser = argparse.ArgumentParser()
parser.add_argument("--dset_folder", default='data/data_toy3', type=str)
parser.add_argument("--file_out", default='../dataset_toy3', type=str)



if __name__ ==  '__main__':
    args = parser.parse_args()
    info_dataset = {}
    info_file = '{}/out_problems/info.json'.format(args.dset_folder)
    with open(info_file, 'r') as f:
        info_file = json.load(f)
    
    
    os.makedirs(args.file_out, exist_ok=True)
    info = []
    for dp in tqdm(info_file):
        program_file = '{}/out_plans/{}.txt'.format(args.dset_folder, dp['file_name'])
        #if not os.path.isfile(program_file):
        #    print(program_file)
        #continue
        if os.path.isfile(program_file):
            with open(program_file, 'r') as f:
                nfp = f.readlines()
                if len(nfp) == 0: continue
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
            


            with open(curr_env_path, 'r') as f:
                aux = json.load(f)
            with open(new_env_path, 'w+') as f:
                f.write(json.dumps({'init_graph': aux}, indent=4))
            if not os.path.isfile(new_file_path+'.txt'):
                shutil.copy(program_file, new_file_path+'.txt')

    with open('{}/info.json'.format(args.file_out), 'w+') as f:
        f.write(json.dumps(info))
