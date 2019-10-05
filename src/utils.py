from copy import deepcopy

from networkx import Graph


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


def build_cong(old_cong, cls_1, cls_2):
    cong = deepcopy(old_cong)

    new_class = cls_1 + cls_2
    cong.remove(cls_1)
    cong.remove(cls_2)
    cong.append(new_class)
    cong = sorted(cong)
    string = ', '.join(cls.string for cls in cong if len(cls) > 1)
    if len(string) == 0:
        return '∆'
    return cong, string


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
