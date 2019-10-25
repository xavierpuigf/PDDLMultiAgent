import itertools
import pdb


def and_constraint(constraints):
    if len(constraints) == 1:
        return constraints[0]
    return '(and {} {})'.format(constraints[0], and_constraint(constraints[1:]))

class Goal():
    def __init__(self):
        pass

    def compute_goal(self):
        return '', True



class Findclass(Goal):
    " Find any node of a given class"
    def __init__(self, class_name):
        self.class_name = class_name

    def compute_goal(self, object_dict, graph):
        id_for_name = [x['id'] for x in graph['nodes'] if x['class_name'] == self.class_name]
        pddl_name = [object_dict[id] for id in id_for_name]
        char_node = [x for x in graph['nodes'] if x['class_name'] == 'character'][0]
        char_node = object_dict[char_node['id']]
        object_or = ['(and (observable {0} {1}) (close {0} {1}))'.format(char_node, name) for name in pddl_name]
        return '(or {})'.format(' '.join(object_or)), True




class Findnode(Goal):
    " Find a particular node"
    def __init__(self, id_num):
        self.id_num = id_num
    def compute_goal(self, object_dict, graph):
        node_name_str = object_dict[self.id_num]
        char_node = [x for x in graph['nodes'] if x['class_name'] == 'character'][0]
        char_node = object_dict[char_node['id']]
        return '(and (observable {0} {1}) (close {0} {1}))'.format(char_node, node_name_str), True


class Relax(Goal):
    def compute_goal(self, object_dict, graph):
        return '''
            (exists (?object_sofa - object ?object_tv - object ?char - character)
                    (and 
                        (on ?object_tv)
                        (sitting ?char ?object_sofa)
                        (or (facing ?object_tv ?object_sofa)
                            (facing ?object_sofa ?object_tv)))
            )
            ''', True
        # Refill this

class TableSet(Goal):
    def __init__(self, num_people):
        self.num_people = num_people
        self.allow_combinations = False

    def compute_goal(self, object_dict, graph):
        tables = []
        objects_needed = ['glass', 'plate']
        objects_needed = [(x, self.num_people) for x in objects_needed]
        objects_type = []
        for object_name, num_obj in objects_needed:
            objects_type.append([])
            for node in graph['nodes']:
                if object_name in node['class_name']:
                    objects_type[-1].append(object_dict[node['id']])

        for node in graph['nodes']:
            if node['class_name'] == 'table':
                tables.append(object_dict[node['id']])
        
        combis = []
        for (object_class, num_obj), object_nodes in zip(objects_needed, objects_type):
            list_combis = list(itertools.combinations(object_nodes, num_obj))
            if len(list_combis) > 0:
                combis.append(list_combis)    
        try:
            if not self.allow_combinations:
                combis = [[x[0]] for x in combis]
                tables = [tables[0]]
        except:
            return '', False

        comb_tables = list(itertools.combinations(tables, 1))
        
        combinames = []
        combi_final = []
        for tables in comb_tables:
            table = tables[0]
            combi_table = []
            for combi_class in combis: # for every class of object
                combior = []
                # Or between the combinations of any N objects
                for object_combination in combi_class:
                    # N objects should be on table
                    ontopconstraints = ['(ontop {} {})'.format(object_c, table) for object_c in object_combination]
                    combiand = '(and {})'.format(' '.join(ontopconstraints))
                    combior.append(combiand)
                combior = '(or {})'.format(' '.join(combior))
                combi_table.append(combior)
            combi_table = '(and {})'.format(' '.join(combi_table))
            combi_final.append(combi_table)
        combi_final = '(or {})'.format(' '.join(combi_final))
        return combi_final, True

