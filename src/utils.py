from itertools import product

from networkx import Graph


def format_congruence(cong_str):
    res = str(cong_str).replace("'", '').replace('(', '{').replace(')', '}')
    if res[-2] == ',':
        res = res[:-2] + '}'
    return res


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