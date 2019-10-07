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
        'CONTAINER': 'container',
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
