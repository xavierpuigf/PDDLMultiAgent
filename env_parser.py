import json
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
parser.add_argument("--file_out", default='example_out.pddl', type=str)
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

obj2pddl_map = {}
obj2pddl_map_id = {}

plates = []
tables = []

objects = ["(:objects"]
for elem in nodes:
    old_name = (elem['class_name'], elem['id'])
    new_name = elem['class_name'] + '_' + str(elem['id'])
    obj2pddl_map[old_name] = new_name
    obj2pddl_map_id[elem['id']] = new_name
    if 'food' in elem['class_name']:
        plates.append(new_name)
    if elem['class_name'] == 'table':
        tables.append(new_name)
    category = 'object'
    if elem['category'] == 'Characters': category = 'character'
    if elem['category'] == 'Rooms': category = 'room'
    objects.append('{} - {}'.format(new_name, category))
objects.append(")")
object_str = '    \n'.join(objects) +'\n'

init = ['(:init']
map_properties = {
        'SURFACES':'surface',
    'GRABBABLE': 'grabable',
    'CONTAINER': 'container',
    'INSIDE': 'inside',
    'CLOSE': 'close',
    'ON': 'ontop'
}
for elem in nodes:
    old_name = (elem['class_name'], elem['id'])
    new_name = obj2pddl_map[old_name]
    properties = elem['properties']
    for prop in properties:
        if prop in map_properties.keys():
            prop_name = map_properties[prop]
            init.append('({} {})'.format(prop_name, new_name))

for elem in env_content['edges']:
    if elem['from_id'] in obj2pddl_map_id.keys() and elem['to_id'] in obj2pddl_map_id.keys():
        elem1 = obj2pddl_map_id[elem['from_id']]
        elem2 = obj2pddl_map_id[elem['to_id']]
        if elem['relation_type'] in map_properties.keys():
            new_relation = map_properties[elem['relation_type']]

            relation = '({} {} {})'.format(new_relation, elem1, elem2)
            init.append(relation)
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
with open('out.pddl', 'w+') as f:
    f.write(final_pddl)

