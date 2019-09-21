from networkx import Graph, DiGraph

from factor import FactorGraph


class HalfLattice(DiGraph):
    def __init__(self, g: Graph, trees: bool):
        super(HalfLattice, self).__init__()
        self.trees = trees

        self.final = []
        self.start = FactorGraph(g)
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
        node = fg.as_node()
        super(HalfLattice, self).add_node(node, **attr)
        self.nodes[node]['fg'] = fg

    def _build(self):
        queue = [self.start.as_node()]
        while len(queue):
            current = queue.pop()
            main_factors = self.nodes[current]['fg'].get_mains(self.trees)
            for main_factor in main_factors:
                node = main_factor.as_node()
                if node not in self.nodes:
                    self.add_node(main_factor)
                self.add_edge(current, node)
                queue.append(node)

    def _find_finals(self):
        queue = [self.start.as_node()]
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
            if cur == self.start.as_node():
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
