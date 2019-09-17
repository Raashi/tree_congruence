import networkx as nx

from itertools import chain

from factor import FactorGraph, TreeFactorGraph
from utils import format_congruence


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
        # noinspection PyTypeChecker
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
                labels[node] = '\n'.join(label)
        return labels


class Lattice(HalfLattice):
    def __init__(self, g: nx.Graph):
        super(Lattice, self).__init__(g, TreeFactorGraph)
