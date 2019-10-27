import glob
import json
dir_path = 'data/data_subgoals/input_envs'
files_json = glob.glob('{}/*.json'.format(dir_path))
for file_json in files_json:
    with open(file_json, 'r') as f:
        graph = json.load(f)
    id_2node = {}
    for n in graph['nodes']:
        id_2node[n['id']] = n

    for edge in graph['edges']:
        if edge['relation_type'] == 'INSIDE':
            node_to = id_2node[edge['to_id']]
        if node_to['category'] == "Rooms" or 'CAN_OPEN' in node_to['properties']:
            edge['relation_type'] = "ON"

    with open(file_json, 'w+') as f:
        f.write(json.dumps(graph, indent=4))
