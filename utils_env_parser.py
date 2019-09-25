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


def obtain_properties_pddl(nodes, obj2pddl_map)
    map_properties = {
        'SURFACES':'surface',
        'GRABBABLE': 'grabable',
        'CONTAINER': 'container',
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
                props.append(prop_name, naw_name)
    return props
                init.append('({} {})'.format(prop_name, new_name))


def obtain_relationships_pddl(edges, obj2pddl_map):
    map_edges = {
        'INSIDE': 'inside',
        'CLOSE': 'close',
        'ON': 'ontop'
    }
    for elem in edges:
        if elem['from_id'] in obj2pddl_map_id.keys() and elem['to_id'] in obj2pddl_map.keys():
            elem1 = obj2pddl_map[elem['from_id']]
            elem2 = obj2pddl_map[elem['to_id']]
            if elem['relation_type'] in map_edges.keys():
                new_relation = map_edges[elem['relation_type']]
                relation = '({} {} {})'.format(new_relation, elem1, elem2)
                init.append(relation)
