def convert_objects_pddl(object_nodes):
    obj2pddl_map = {}
    objects = []
    for elem in object_nodes:
        if elem['class_name'] in ['wall', 'ceiling', 'floor']:
            continue
        old_name = (elem['class_name'], elem['id'])
        new_name = elem['class_name'] + '_' + str(elem['id'])
        obj2pddl_map[elem['id']] = new_name
        category = 'object'

        if elem['category'] == 'Characters': category = 'character'
        if elem['category'] == 'Rooms': category = 'room'
        objects.append((new_name, category))
    return objects, obj2pddl_map

def obtain_states_pddl(nodes, obj2pddl_map):
    map_properties = {
        'ON': ('on', True),
        'OPEN': ('open', True),
        'OFF': ('on', False),
        'CLOSED': ('open', False)
    }
    props = []
    for elem in nodes:
        old_name = (elem['class_name'], elem['id'])
        id = elem['id']
        if id not in obj2pddl_map.keys():
            continue
        new_name = obj2pddl_map[elem['id']]
        properties = elem['states']
        for prop in properties:
            if prop in map_properties.keys():
                prop_name, is_true = map_properties[prop]
                if is_true:
                    props.append('({} {})'.format(prop_name, new_name))
                else:
                    props.append('(not ({} {}))'.format(prop_name, new_name))
    return props

def obtain_properties_pddl(nodes, obj2pddl_map):
    map_properties = {
        'SURFACES':'surface',
        'GRABBABLE': 'grabable',
        'CAN_OPEN': 'container',
        'SITTABLE': 'sittable',
        'HAS_SWITCH': 'electronics',
    }
    props = []
    for elem in nodes:
        old_name = (elem['class_name'], elem['id'])
        id = elem['id']
        if id not in obj2pddl_map.keys():
            continue
        new_name = obj2pddl_map[elem['id']]
        properties = elem['properties']
        for prop in properties:
            if prop in map_properties.keys():
                prop_name = map_properties[prop]
                props.append((prop_name, new_name))
    return props


def obtain_relations_pddl(edges, obj2pddl_map):
    map_edges = {
        'INSIDE': 'inside',
        'CLOSE': 'close',
        'ON': 'ontop',
        'FACING': 'facing'
    }
    relations = []
    for elem in edges:
        if elem['from_id'] in obj2pddl_map.keys() and elem['to_id'] in obj2pddl_map.keys():
            elem1 = obj2pddl_map[elem['from_id']]
            elem2 = obj2pddl_map[elem['to_id']]
            if elem['relation_type'] in map_edges.keys():
                new_relation = map_edges[elem['relation_type']]
                relation = (new_relation, elem1, elem2)
                relations.append(relation)
    return relations

def convert_to_virtualhome_program(action_list):
    action_list = [x[1:-1].split()[:-1] for x in action_list]
    action_list_str = []
    for action_instr in action_list:
        if len(action_instr) == 0:
            continue
        action_item = '[{}]'.format(action_instr[0].upper())
        if len(action_instr) > 1:
            objects_item = ['<{}> ({})'.format('_'.join(l.split('_')[:-1]), l.split('_')[-1]) for l in action_instr[1:]]
        action_list_str.append('{} {}'.format(action_item, ' '.join(objects_item)))
    return action_list_str


def parse_env(env_content, goal, goal_name):
    nodes = env_content['nodes']

    header = '''
    (define (problem {})
    (:domain virtualhome)\n
    '''.format(goal_name)

    obj2pddl_map_id = {}

    plates = []
    tables = []

    objects_pddl, obj2pddl_map_id = convert_objects_pddl(nodes)

    states_pddl = obtain_states_pddl(
            env_content['nodes'], 
            obj2pddl_map_id)

    properties_pddl = obtain_properties_pddl(
            env_content['nodes'], 
            obj2pddl_map_id)

    relations_pddl = obtain_relations_pddl(
            env_content['edges'], 
            obj2pddl_map_id)

    objects = ["(:objects"]
    objects += ['{} - {}'.format(x,y) for x,y in objects_pddl]
    objects.append(")")
    object_str = '    \n'.join(objects) +'\n'

    init = ['(:init']
    init += ['(= (objects_grabbed) 0)']
    init += states_pddl
    init += ['({} {})'.format(x,y) for x,y in properties_pddl]
    init += ['({} {} {})'.format(x,y,z) for x,y,z in relations_pddl]
    init.append(')')
    init_str = '    \n'.join(init) + '\n'


    goal_str, success = goal.compute_goal(obj2pddl_map_id, env_content)
    if not success:
        return '', False

    goal = ['(:goal']
    goal.append(goal_str)
    goal.append(')')
    goal_str = '    \n'.join(goal)
    final_pddl = header + object_str + init_str + goal_str + '\n)'
    return final_pddl, True
