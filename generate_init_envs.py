import sys
from tqdm import tqdm
import ipdb
import random
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


def populate_env(info):
    env_json_file, out_path = info
    curr_id = starting_id
    curr_environment = utils.load_graph(env_json_file)
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
                curr_id += 1
                objects_added += 1
                object_placed = True

    graph_dict = curr_environment.to_dict()
    if out_path is not None:
        with open(out_path, 'w+') as f:
            f.write(json.dumps(graph_dict, indent=4))
    return graph_dict


if __name__ == '__main__':
    envs = get_initial_envs()
    envs_per_apt = 50
    graph_dir = 'input_envs'
    for env in tqdm(envs):
        env_part = env.split('/')[-1].split('.')[-2]
        inputs = [(env, '{}/{}_{}.json'.format(graph_dir, env_part, it)) for it in range(envs_per_apt)]
        for inp in inputs:
            populate_env(inp)


