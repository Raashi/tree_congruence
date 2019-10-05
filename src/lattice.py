from time import time

from networkx import Graph, DiGraph

from congclass import CongruenceClass
from factor import FactorGraph
from utils import is_tree, divide


class Lattice(DiGraph):
    def __init__(self, g: Graph, levels_to_build):
        super().__init__()

        self.g = g
        self.division = divide(g)

        self.levels_to_build = levels_to_build

        self.final = []
        self.start = FactorGraph(g, sorted([CongruenceClass([node]) for node in g.nodes]), '∆')
        self.add_node(self.start)

        self.levels_count = g.number_of_nodes() - 1
        self.levels = [[] for _ in range(self.levels_count)]
        self.levels_set = [set() for _ in range(self.levels_count)]
        self.nodes_levels = {}
        self._build()

    def add_node(self, fg: FactorGraph, **attr):
        node = fg.string
        super(Lattice, self).add_node(node, **attr)
        self.nodes[node]['fg'] = fg

    def _build(self):
        print('Старт построения решетки')
        start = time()
        self.levels[0].append(self.start.string)
        self.levels_set[0].add(self.start.string)
        self.nodes_levels[self.start.string] = 0

        for level in range(min(self.levels_count - 1, self.levels_to_build - 1)):
            for node in self.levels[level]:
                factor = self.nodes[node]['fg']
                for cong, string in factor.get_mains(self.division):
                    if string in self.levels_set[level + 1]:
                        self.add_edge(node, string)
                    else:
                        sub_factor = FactorGraph(self.g, cong, string)
                        if not is_tree(sub_factor):
                            continue
                        self.add_node(sub_factor)
                        self.levels[level + 1].append(string)
                        self.levels_set[level + 1].add(string)
                        self.nodes_levels[string] = level + 1
                        self.add_edge(node, string)
            print(f'Уровень {level} построен')
        print('Построение заняло {:.2f} секунд'.format(time() - start))
