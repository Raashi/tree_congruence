from itertools import combinations, product
from copy import deepcopy

import networkx as nx

from utils import format_congruence, independent_subsets, is_tree


class FactorGraph(nx.Graph):
    def __init__(self, g: nx.Graph, cong: list, generators=None):
        nx.Graph.__init__(self)
        self.g = g
        self.cong = sorted(cong)
        self.add_nodes_from(cong)
        self.generators = generators
        for cls_1, cls_2 in combinations(cong, 2):
            for u, v in product(cls_1, cls_2):
                if g.has_edge(u, v):
                    self.add_edge(cls_1, cls_2)
                    break

    def distance(self, u, v):
        queue = [u]
        d = {u: 0}
        while len(queue):
            current = queue.pop()
            for node in self.adj[current]:
                if node == v:
                    return d[current] + 1
                elif node in d:
                    continue
                else:
                    queue.append(node)
                    d[node] = d[current] + 1
        raise ValueError("Невозможно определить расстояние между вершинами")

    def get_str_cong(self):
        return str(self.cong)

    def get_str_cong_beauty(self):
        return '\n'.join(map(str, self.cong))

    def __eq__(self, other):
        if not isinstance(other, FactorGraph):
            raise ValueError('incorrect __eq__ call')
        return self.get_str_cong() == other.get_str_cong()

    def __hash__(self):
        return self.get_str_cong().__hash__()

    @staticmethod
    def get_default_congruence(g: nx.Graph):
        return [tuple([node]) for node in g]

    @staticmethod
    def get_default(g: nx.Graph):
        if isinstance(g, FactorGraph):
            raise TypeError("Взятие тожественной конгруэнции возможно только для nx.Graph")
        return FactorGraph(g, FactorGraph.get_default_congruence(g))

    def get_mains(self):
        main_factors = set()
        for cls_1, cls_2 in combinations(self.cong, 2):
            if not independent_subsets(self.g, cls_1, cls_2):
                continue
            if self.distance(cls_1, cls_2) % 2 == 1:
                continue
            cong = deepcopy(self.cong)
            cong.remove(cls_1), cong.remove(cls_2)
            cong.append(tuple(sorted(cls_1 + cls_2)))
            cong.sort()

            factor = FactorGraph(self.g, cong, (cls_1, cls_2))
            if factor not in main_factors:
                main_factors.add(factor)
        return main_factors

    def get_labels(self):
        labels = {}
        for node in self.nodes:
            labels[node] = format_congruence(node)
        return labels


class TreeFactorGraph(FactorGraph):

    def get_mains(self, allowed_nodes=None):
        main_factors = FactorGraph.get_mains(self)
        mains = set()
        for factor in main_factors:
            if is_tree(factor):
                mains.add(TreeFactorGraph(factor.g, factor.cong, factor.generators))
        return mains

    @staticmethod
    def get_default(g: nx.Graph):
        if not is_tree(g):
            raise ValueError("Попытка построения тождественной древесной конгруэнции для графа, не являющимся деревом")
        if isinstance(g, FactorGraph):
            raise TypeError("Взятие тожественной конгруэнции возможно только для nx.Graph")
        return TreeFactorGraph(g, FactorGraph.get_default_congruence(g))
