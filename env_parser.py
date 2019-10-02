import json
import utils_env_parser
import itertools
import glob
import numpy as np
from multiprocessing import Pool
import os
from tqdm import tqdm
import argparse
import pdb

parser = argparse.ArgumentParser()
parser.add_argument("--file_env", default='example_env', type=str)
parser.add_argument("--file_out", default='out_problems/example_out.pddl', type=str)
parser.add_argument("--problem_name", default='setuptable', type=str)

args = parser.parse_args()
with open(args.file_env+'.json', 'r') as f:
    env_content = json.load(f)
    env_content = env_content['init_graph']
nodes = env_content['nodes']

header = '''
(define (problem {})
(:domain virtualhome)\n
'''.format(args.problem_name, args.file_env)

obj2pddl_map_id = {}

plates = []
tables = []

objects_pddl, obj2pddl_map_id = utils_env_parser.convert_objects_pddl(nodes)

# Obtain plates and food
plates = []
tables = []
for node in env_content['nodes']:
    if 'food' in node['class_name']:
        plates.append(obj2pddl_map_id[node['id']])
    if node['class_name'] == 'table':
        tables.append(obj2pddl_map_id[node['id']])

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
init += ['({} {})'.format(x,y) for x,y in properties_pddl]
init += ['({} {} {})'.format(x,y,z) for x,y,z in relations_pddl]
init.append(')')
init_str = '    \n'.join(init) + '\n'

comb_plates = list(itertools.combinations(plates, 2))
comb_tables = list(itertools.combinations(tables, 1))


goal = ['(:goal']
combinames = []
for plates in comb_plates:
    for tables in comb_tables:
        combinames.append('(and (ontop {1} {2}) (ontop {0} {2}))'.format(plates[0], plates[1], tables[0]))
print(len(combinames))
combi = '(or {})'.format(' '.join(combinames))
goal.append(combi)
goal.append(')')
goal_str = '    \n'.join(goal)
import pdb
pdb.set_trace()
final_pddl = header + object_str + init_str + goal_str + '\n)'
with open(args.file_out, 'w+') as f:
    f.write(final_pddl)

