import itertools
class Goal():
    def __init__(self, object_dict, graph):
        self.object_dict = object_dict
        self.graph = graph

    def compute_goal(self):
        return ''

class TableSet(Goal):
    def __init__(self, object_dict, graph, num_people):
        super().__init__(object_dict, graph)
        self.num_people = num_people

    def compute_goal(self):
        plates = []
        tables = []
        for node in self.graph['nodes']:
            if 'food' in node['class_name']:
                plates.append(self.object_dict[node['id']])
            if node['class_name'] == 'table':
                tables.append(self.object_dict[node['id']])

        comb_plates = list(itertools.combinations(plates, self.num_people))
        comb_tables = list(itertools.combinations(tables, 1))
        combinames = []
        for plates in comb_plates:
            for tables in comb_tables:
                combinames.append(
                        '(and (ontop {1} {2}) (ontop {0} {2}))'.format(
                            plates[0], plates[1], tables[0]))
        combi = '(or {})'.format(' '.join(combinames))
        return combi

