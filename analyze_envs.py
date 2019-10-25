import json
import sys
sys.path.append('virtualhome/simulation/')
from evolving_graph import utils
import glob


files = glob.glob('data/data_complex/input_envs/*')

g_helper = utils.graph_dict_helper()
all_objects = []
for file in files:
    with open(file, 'r') as f:
        graph = json.load(f)
        obj_names = [x['class_name'] for x in graph['nodes']]
        all_objects += obj_names
        all_objects = list(set(all_objects))

print(len(all_objects))
for obj in all_objects:
    transformed = g_helper.merge_object_name(obj)
    if transformed != obj:
        print('{} --> {}'.format(obj, transformed))



