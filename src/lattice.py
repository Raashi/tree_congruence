import networkx as nx

from copy import deepcopy
from itertools import combinations
import itertools


def independent_subsets(g: nx.Graph, subset_1, subset_2) -> bool:
    for u, v in itertools.product(subset_1, subset_2):
        if g.has_edge(u, v):
            return False
    return True


def is_tree(g: nx.Graph) -> bool:
    if g.number_of_nodes() - 1 != g.number_of_edges():
        return False
    visited = set()
    queue = {next(g.nodes.__iter__())}
    while len(queue):
        current = queue.pop()
        visited.add(current)
        for v in g.neighbors(current):
            if v not in visited:
                visited.add(v)
                queue.add(v)
    return len(visited) == g.number_of_nodes()


class FactorGraph(nx.Graph):
    def __init__(self, g: nx.Graph, cong: list):
        nx.Graph.__init__(self)
        self.g = g
        self.cong = sorted(cong)
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

    def get_str_cong(self):
        return str(self.cong)

    def get_str_cong_beauty(self):
        return '\n'.join(map(str, self.cong))

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


class HalfLattice(nx.DiGraph):
    def __init__(self, g: nx.Graph):
        super(HalfLattice, self).__init__()
        self.final = []
        self.start = FactorGraph.get_default(g)
        self.add_node(self.start)
        self._build()
        self._find_finals()

        self.levels = None
        self.nodes_levels = None
        self._set_levels()

    def add_node(self, fg: FactorGraph,  **attr):
        node = fg.get_str_cong()
        super(HalfLattice, self).add_node(node, **attr)
        self.nodes[node]['fg'] = fg

    def _build(self):
        queue = [self.start.get_str_cong()]
        while len(queue):
            current = queue.pop()
            main_factors = self.nodes[current]['fg'].get_mains()
            for main_factor in main_factors:
                node = main_factor.get_str_cong()
                if node not in self.nodes:
                    self.add_node(main_factor)
                self.add_edge(current, node)
                queue.append(node)

    def _find_finals(self):
        queue = [self.start.get_str_cong()]
        while len(queue):
            current = queue.pop()
            current_fg = self.nodes[current]['fg']
            outers = list(self.successors(current))
            if not len(outers):
                if current_fg not in self.final:
                    self.final.append(current_fg)
            else:
                for u in outers:
                    queue.append(u)

    def _set_levels(self):
        self.levels = []
        self.nodes_levels = {}
        for node in self.nodes:
            level = 0
            current = node
            while len(list(self.predecessors(current))):
                current = next(self.predecessors(current))
                level += 1
            self.levels += [[] for _ in range(level + 1 - len(self.levels))]
            self.levels[level].append(node)
            self.nodes_levels[node] = level

    def get_labels(self):
        labels = {}
        for node in self.nodes:
            labels[node] = self.nodes[node]['fg'].get_str_cong_beauty()
        return labels
