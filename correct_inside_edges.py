import glob
import pdb
from tqdm import tqdm
import json
dir_path = 'data/data_subgoals2/input_envs'
files_json = glob.glob('{}/Trimmed*.json'.format(dir_path))
for file_json in tqdm(files_json):
    with open(file_json, 'r') as f:
        graph = json.load(f)
        try:
            if 'init_graph' in graph.keys():
                graph = graph['init_graph']
        except:
            pdb.set_trace()
    id_2node = {}
    for n in graph['nodes']:
        id_2node[n['id']] = n

    node_inside = {}
    edge_inside = {}
    for edge in graph['edges']:
        if edge['from_id'] not in edge_inside.keys(): edge_inside[edge['from_id']] = []
        edge_inside[edge['from_id']].append(edge['to_id'])
        if edge['relation_type'] == 'INSIDE':
            node_to = id_2node[edge['to_id']]
            if node_to['category'] == "Rooms" or 'CAN_OPEN' in node_to['properties']:
                pass
            else:
                edge['relation_type'] = "ON"

            if node_to['category'] == 'Rooms':
                node_inside[edge['from_id']] = node_to['id']

    for node in graph['nodes']:
        if node['category'] != "Rooms" and node['id'] not in node_inside.keys():
            nodes_rel = edge_inside[node['id']]
            
    with open(file_json, 'w+') as f:
        f.write(json.dumps(graph, indent=4))
