from itertools import combinations, product

from networkx import Graph

from factor import CongruenceClass


def divide(g: Graph):
    if g.number_of_nodes() == 0:
        return {}
    node = next(iter(g.nodes))
    queue = [node]
    division = {node: True}
    while len(queue):
        u = queue.pop()
        for v in g.neighbors(u):
            if v not in division:
                division[v] = not division[u]
                queue.append(v)
    assert len(division) == g.number_of_nodes()
    return division


def partition(collection, division):
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in partition(collection[1:], division):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            if division[first] == division[subset[0]]:
                yield smaller[:n] + [[first] + subset] + smaller[n + 1:]
        # put `first` in its own subset
        yield [[first]] + smaller


class FactorGraph(Graph):
    def __init__(self, g: Graph, cong: list):
        super(FactorGraph, self).__init__(g)

        self.cong = [CongruenceClass(cls) for cls in cong]
        for cls in self.cong:
            self.add_node(cls.as_node())
        for (cls1, cls2) in combinations(self.cong, 2):
            for node1, node2 in product(cls1, cls2):
                if g.has_edge(node1, node2):
                    self.add_edge(cls1.as_node(), cls2.as_node())
                    break
