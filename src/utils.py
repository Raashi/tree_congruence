from itertools import product

from networkx import Graph


def independent_subsets(g: Graph, subset_1, subset_2) -> bool:
    for u, v in product(subset_1, subset_2):
        if g.has_edge(u, v):
            return False
    return True


def is_tree(g: Graph) -> bool:
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


def get_independence_table(g: Graph):
    return [[not g.has_edge(u, v)] for u in g for v in g]


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
