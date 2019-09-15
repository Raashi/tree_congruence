import networkx as nx

from copy import deepcopy
from itertools import chain
from itertools import combinations
import itertools


def format_congruence(cong_str):
    return str(cong_str).replace("'", '').replace('(', '{').replace(')', '}')


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


def get_path(g: nx.Graph, u, v):
    queue = [u]
    p = {u: None}

    while len(queue):
        current = queue.pop()
        for u in g.adj[current]:
            if u not in p:
                p[u] = current
                queue.append(u)
        if v in p:
            break

    res = [v]
    current = v
    while p[current] is not None:
        current = p[current]
        res.append(current)
    res.reverse()
    return res


def get_cycle(g: nx.Graph, node_in_cycle):
    def dfs(v, parent, stack):
        for node in g.adj[v]:
            if node == parent:
                continue
            if node in stack:
                return stack
            else:
                cycle = dfs(node, v, stack + [node])
                if cycle is not None:
                    return cycle
    return dfs(node_in_cycle, None, [node_in_cycle])


class FactorGraph(nx.Graph):
    def __init__(self, g: nx.Graph, cong: list, generators=None):
        nx.Graph.__init__(self)
        self.g = g
        self.cong = sorted(cong)
        self.add_nodes_from(cong)
        self.generators = generators
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
            return False
        return self.get_str_cong() == other.get_str_cong()

    def __hash__(self):
        return self.get_str_cong().__hash__()

    @staticmethod
    def get_default_congruence(g: nx.Graph):
        return [tuple([node]) for node in g]

    @staticmethod
    def get_default(g: nx.Graph):
        if type(g) is FactorGraph:
            raise TypeError("Взятие тожественной конгруэнции возможно только для nx.Graph")
        return FactorGraph(g, FactorGraph.get_default_congruence(g))

    def get_mains(self):
        main_factors = set()
        main_factors_congs = set()
        for cls_1, cls_2 in itertools.combinations(self.cong, 2):
            if not independent_subsets(self.g, cls_1, cls_2):
                continue
            if self.distance(cls_1, cls_2) % 2 == 1:
                continue
            cong = deepcopy(self.cong)
            cong.remove(cls_1), cong.remove(cls_2)
            cong.append(tuple(sorted(cls_1 + cls_2)))
            cong.sort()

            factor = FactorGraph(self.g, cong, (cls_1, cls_2))
            cong_tuple = tuple(factor.cong)
            if cong_tuple not in main_factors_congs:
                main_factors_congs.add(cong_tuple)
                main_factors.add(factor)
        return main_factors

    def get_labels(self):
        labels = {}
        for node in self.nodes:
            labels[node] = format_congruence(node)
        return labels


class TreeFactorGraph(FactorGraph):
    def __init__(self, g: nx.Graph, cong: list):
        super(TreeFactorGraph, self).__init__(g, cong)
        self.generated_by = ()

    def get_mains(self, allowed_nodes=None):
        main_factors = FactorGraph.get_mains(self)
        mains = {factor for factor in main_factors if is_tree(factor)}
        return mains

    @staticmethod
    def get_default(g: nx.Graph):
        if not is_tree(g):
            raise ValueError("Попытка построения тождественной древесной конгруэнции для графа, не являющимся деревом")
        if isinstance(g, FactorGraph):
            raise TypeError("Взятие тожественной конгруэнции возможно только для nx.Graph")
        return TreeFactorGraph(g, FactorGraph.get_default_congruence(g))


class HalfLattice(nx.DiGraph):
    def __init__(self, g: nx.Graph, cong_cls=FactorGraph):
        super(HalfLattice, self).__init__()
        self.final = []
        self.start = cong_cls.get_default(g)
        self.add_node(self.start)
        self._build()
        self._find_finals()

        self.levels = None
        self.nodes_levels = None
        self._set_levels()
        for idx, level in enumerate(self.levels):
            self.levels[idx] = sorted(level)

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
        def gen_distances_to_root(source, cur, length):
            if cur == self.start.get_str_cong():
                yield length
            for u in self.predecessors(cur):
                yield from gen_distances_to_root(source, u, length + 1)

        self.levels = []
        self.nodes_levels = {}
        for node in self.nodes:
            distances = [level for level in gen_distances_to_root(node, node, 0)]
            level = max(distances)

            self.levels += [[] for _ in range(level + 1 - len(self.levels))]
            self.levels[level].append(node)
            self.nodes_levels[node] = level

    def get_labels(self):
        labels = {}
        for node in self.nodes:
            gens = self.nodes[node]['fg'].generators
            if gens is None:
                labels[node] = '∆'
            else:
                gens = tuple(chain(*gens))
                labels[node] = '∆' if gens is None else format_congruence(gens)
                label = []
                for cls in self.nodes[node]['fg'].cong:
                    if len(cls) > 1:
                        label.append(format_congruence(str(cls)))
                labels[node] = ',\n'.join(label)
        return labels


class Lattice(HalfLattice):
    def __init__(self, g: nx.Graph):
        super(Lattice, self).__init__(g, TreeFactorGraph)


if __name__ == '__main__':
    _g = nx.path_graph(5)
    _g.add_edge(1, 5)
    print(get_path(_g, 2, 5))
