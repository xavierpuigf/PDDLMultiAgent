import sys
from tqdm import tqdm
import ipdb
import random
import pdb
import json
import glob
sys.path.append('virtualhome/simulation/')
import evolving_graph.utils as utils
from evolving_graph import preparation
from evolving_graph.environment import Relation, GraphNode, State

# restrictions: set of objects we should be adding for sure
objects_to_add = 50
restrictions = [
    (['wine_glass', 'glass', 'drinking_glass', 'water_glass'], 5),
    (['plate'], 5),
    (['knife'], 5),
    (['remote_control'], 1)
]
starting_id = 2000

def get_nodes(environment, class_name):
    nodes = environment.get_nodes_by_attr('class_name', class_name)
    return nodes

    
def get_initial_envs():
    envs = glob.glob('virtualhome/example_graphs/Trimmed*.json')
    return envs

def get_relations(curr_environment, object_name):
    # check which locations are available
    possible_locations = graph_helper.object_placing[object_name]
    locations_in_nodes = []
    for location in possible_locations:
        nodes = get_nodes(curr_environment, location['destination'])
        nodes = list(nodes)
        num_nodes = len(nodes)
        for node in nodes:
            relation_name = graph_helper.relation_placing_simulator[location['relation'].lower()]
            locations_in_nodes.append((node, Relation[relation_name]))
    return locations_in_nodes


graph_helper = utils.graph_dict_helper()

def create_node(object_name, curr_id):
    properties = [i for i in graph_helper.properties_data[object_name]]
    states =  [State[v.default] for v in graph_helper.get_object_binary_variables(object_name)]
    category = 'added_object' 
    prefab_name = None
    bounding_box = None
    node_object = GraphNode(curr_id, object_name, properties, states, category, prefab_name, bounding_box)
    return node_object

def clean_graph(graph):
    # If x -> in z -> in y ==> x -> in z
    # If object cannot be opened, change to on
    id_between = [x for x in graph['nodes'] if x['class_name'] in ['door', 'doorjamb']]
    node_inside = {}
    edge_inside = {}
    id_2node = {}
    for n in graph['nodes']:
        id_2node[n['id']] = n

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
            room_inside = ndoe_inside[nodes_rel[0]]
            graph['edges'].append({'from_id': node['id'] , 'to_id': room_inside, 'relation_type':'INSIDE'})

    parent_node = {}
    children_node = {}
    for it, edge in enumerate(graph['edges']):
        if edge['relation_type'] == 'INSIDE':
            if edge['to_id'] not in parent_node.keys(): parent_node[edge['to_id']] = []
            parent_node[edge['to_id']].append(edge['from_id'])
            if edge['from_id'] not in children_node.keys(): children_node[edge['from_id']] = []
            children_node[edge['from_id']].append(edge['to_id'])

    final_edges = []
    for edge in graph['edges']:
        if edge['relation_type'] == 'INSIDE':
            if edge['from_id'] in id_between:
                final_edges.append(edge)
                continue
            all_parents = children_node[edge['from_id']]
            all_children = parent_node[edge['to_id']]
            if len(set(all_parents).intersection(all_children)) > 0:
                continue
        final_edges.append(edge)
    graph['edges'] = final_edges
    return graph



def populate_env(info):
    env_json_file, out_path = info
    curr_id = starting_id
    with open(env_json_file, 'r') as f:
        env_file = json.load(f)
    print('Cleaning...')
    env_file = clean_graph(env_file)
    print('Clean.')
    curr_environment = utils.EnvironmentGraph(env_file)
    objects_to_place = list(graph_helper.object_placing.keys())

    # Let's start with populating the nodes we care about
    objects_added = 0
    for restriction in restrictions:
        objects_possible, num_objects = restriction
        objects_add_restriction = random.choices(objects_possible, k=num_objects)
        for object_name in objects_add_restriction:
            # select one relation at random
            locations_in_nodes = get_relations(curr_environment, object_name)

            
            if len(locations_in_nodes) > 0:
                node_location, relation = random.choice(locations_in_nodes)
                node_object = create_node(object_name, curr_id)
                curr_environment.add_node(node_object)
                curr_environment.add_edge(node_object, relation, node_location)
                if relation == Relation['CLOSE']:
                    curr_environment.add_edge(node_location, relation, node_object)

                if relation != Relation['INSIDE']:
                    nodes_other = list(curr_environment.get_nodes_from(node_location, Relation['INSIDE']))
                    #node_room = [x for x in nodes_other if x.category == 'Rooms']
                    if len(nodes_other) != 1:
                        pdb.set_trace()

                    curr_environment.add_edge(node_object, Relation['INSIDE'], nodes_other[0])


                objects_added += 1
                curr_id += 1
            else:
                ipdb.set_trace()

    # We now add some random nodes
    for _ in range(objects_to_add-objects_added):
        object_placed = False
        while(not object_placed):
            object_name = random.choice(objects_to_place)

            locations_in_nodes = get_relations(curr_environment, object_name)

            if len(locations_in_nodes) > 0:
                node_location, relation = random.choice(locations_in_nodes)
                node_object = create_node(object_name, curr_id)
                curr_environment.add_node(node_object)
                curr_environment.add_edge(node_object, relation, node_location)
                if relation == Relation['CLOSE']:
                    curr_environment.add_edge(node_location, relation, node_object)

                if relation != Relation['INSIDE']:
                    nodes_other = list(curr_environment.get_nodes_from(node_location, Relation['INSIDE']))
                    if len(nodes_other) != 1:
                        pdb.set_trace()

                    curr_environment.add_edge(node_object, Relation['INSIDE'], nodes_other[0])


                curr_id += 1
                objects_added += 1
                object_placed = True

    graph_dict = curr_environment.to_dict()
    # Merge all nodes

    for node in graph_dict['nodes']:
        node['class_name'] = graph_helper.merge_object_name(node['class_name'])

    if out_path is not None:
        with open(out_path, 'w+') as f:
            f.write(json.dumps(graph_dict, indent=4))
    return graph_dict


if __name__ == '__main__':
    envs = get_initial_envs()
    envs_per_apt = 50
    graph_dir = 'data/data_subgoals3/input_envs'
    for env in tqdm(envs):
        env_part = env.split('/')[-1].split('.')[-2]
        inputs = [(env, '{}/{}_{}.json'.format(graph_dir, env_part, it)) for it in range(envs_per_apt)]
        for inp in inputs:
            populate_env(inp)


