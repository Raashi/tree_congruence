import networkx as nx

from copy import deepcopy
from itertools import combinations
import itertools


def independent_subsets(g: nx.Graph, subset_1, subset_2):
    for u, v in itertools.product(subset_1, subset_2):
        if g.has_edge(u, v):
            return False
    return True


class FactorGraph(nx.Graph):
    def __init__(self, g: nx.Graph, cong: list):
        nx.Graph.__init__(self)
        self.g = g
        self.cong = cong
        self.add_nodes_from(cong)
        for cls_1, cls_2 in combinations(cong, 2):
            for u, v in itertools.product(cls_1, cls_2):
                if g.has_edge(u, v):
                    self.add_edge(cls_1, cls_2)
                    break

    def get_node_class(self, node):
        for cls in self.cong:
            if node in cls:
                return cls
        raise RuntimeError("Не найден класс вершины {}".format(node))

    @staticmethod
    def get_default(g: nx.Graph):
        if type(g) is FactorGraph:
            raise TypeError("Взятие тожественной конгруэнции возможно только для nx.Graph")
        cong = [tuple([node]) for node in g]
        return FactorGraph(g, cong)

    def get_mains(self):
        main_factors = set()
        main_factors_congs = set()
        for cls_1, cls_2 in itertools.combinations(self.cong, 2):
            if not independent_subsets(self.g, cls_1, cls_2):
                continue
            cong = deepcopy(self.cong)
            cong.remove(cls_1), cong.remove(cls_2)
            cong.append(tuple(sorted(cls_1 + cls_2)))
            cong.sort()

            factor = FactorGraph(self.g, cong)
            cong_tuple = tuple(factor.cong)
            if cong_tuple not in main_factors_congs:
                main_factors_congs.add(cong_tuple)
                main_factors.add(factor)
        return main_factors
