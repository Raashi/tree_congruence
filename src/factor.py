from itertools import combinations, product

from networkx import Graph

from congclass import CongruenceClass
from utils import build_cong


class FactorGraph(Graph):
    def __init__(self, g: Graph, cong, string):
        super().__init__()

        self.cong = [CongruenceClass(cls) for cls in cong]
        self.cong_set = set(el for el in self.cong)

        self.string = string
        self.hash = self.string.__hash__()

        self.level = 0
        for cls in self.cong:
            self.add_node(cls.string)
            if len(cls) > 1:
                self.level += len(cls) - 1
        for (cls1, cls2) in combinations(self.cong, 2):
            for node1, node2 in product(cls1, cls2):
                if g.has_edge(node1, node2):
                    self.add_edge(cls1.string, cls2.string)
                    break

    def __str__(self):
        return self.string

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return self.string == other.string

    def get_mains(self, division: dict):
        for cls_1, cls_2 in combinations(self.cong, 2):
            # проверка независимости
            if division[cls_1[0]] != division[cls_2[0]]:
                continue
            yield build_cong(self.cong, cls_1, cls_2)
