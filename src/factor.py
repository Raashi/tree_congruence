from itertools import combinations
from copy import deepcopy

from networkx import Graph

from utils import independent_subsets, is_tree, distance


class CongruenceClass:
    class CongruenceClassIterator:
        def __init__(self, cls):
            self.cls = cls
            self.idx = -1

        def __next__(self):
            self.idx += 1
            if self.idx < len(self.cls):
                return self.cls[self.idx]
            raise StopIteration

    def __init__(self, nodes):
        self._nodes = sorted(nodes)
        self.string = '{' + ', '.join(self._nodes) + '}'
        self.hash = self.string.__hash__()

    def __str__(self):
        return self.string

    def __add__(self, other):
        if not isinstance(other, CongruenceClass):
            raise ValueError
        return CongruenceClass(self._nodes + other._nodes)

    def __iter__(self):
        return self.CongruenceClassIterator(self)

    def __getitem__(self, item):
        return self._nodes[item]

    def __eq__(self, other):
        return str(self) == str(other)

    def __len__(self):
        return len(self._nodes)

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self):
        return self.hash

    def as_node(self):
        return str(self)


class FactorGraph(Graph):
    def __init__(self, g: Graph, *,
                 factor: "FactorGraph" = None,
                 cls_1: CongruenceClass = None,
                 cls_2: CongruenceClass = None):
        super(FactorGraph, self).__init__()

        self.g = g

        if factor is None:
            self.cong = [CongruenceClass([node]) for node in g]
            for cls in self.cong:
                self.add_node(cls.as_node())
            for (u, v) in g.edges:
                self.add_edge(CongruenceClass([u]).as_node(), CongruenceClass([v]).as_node())
            return

        self.add_nodes_from(factor)
        self.add_edges_from(factor.edges)
        self.cong = deepcopy(factor.cong)

        new_class = cls_1 + cls_2
        self.cong.remove(cls_1)
        self.cong.remove(cls_2)
        self.cong.append(new_class)
        self.cong = sorted(self.cong)

        neighbors = list(factor.neighbors(cls_1.as_node())) + list(factor.neighbors(cls_2.as_node()))
        self.remove_node(cls_1.as_node())
        self.remove_node(cls_2.as_node())
        self.add_node(new_class.as_node())

        for node in neighbors:
            self.add_edge(new_class.as_node(), node)

    def __str__(self):
        res = ', '.join(cls.as_node() for cls in self.cong if len(cls) > 1)
        if len(res) == 0:
            return '∆'
        return res

    def __eq__(self, other):
        if not isinstance(other, FactorGraph):
            raise ValueError
        return str(self) == str(other)

    def __hash__(self):
        return str(self).__hash__()

    def get_mains(self, trees: bool):
        main_factors = set()
        for cls_1, cls_2 in combinations(self.cong, 2):
            node_1 = cls_1.as_node()
            node_2 = cls_2.as_node()
            if not independent_subsets(self.g, cls_1, cls_2):
                continue
            if distance(self, node_1, node_2) % 2 == 1:
                continue
            factor = FactorGraph(self.g, factor=self, cls_1=cls_1, cls_2=cls_2)
            if trees is True and is_tree(factor):
                main_factors.add(factor)
        return main_factors

    def as_node(self):
        return str(self)
