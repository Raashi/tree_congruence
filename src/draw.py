import networkx as nx
import matplotlib.pyplot as plt

from alg import HalfLattice


def lattice_pos(g: HalfLattice, root, levels, width=1., height=1.):
    currents = [0] * len(levels)
    vert_gap = height / (max([len(nodes) for nodes in levels]) + 1)

    def _make_pos(pos, node):
        level = g.nodes_levels[node]
        dx = 1 / len(levels[level])
        left = dx / 2
        pos[node] = ((left + dx * currents[level]) * width, -vert_gap * level * height)
        currents[level] += 1
        for outer_node in g.successors(node):
            if outer_node not in pos:
                _make_pos(pos, outer_node)

    res = {}
    _make_pos(res, root)
    return res


def draw_lattice(g: HalfLattice):
    pos = lattice_pos(g, g.start.get_str_cong(), levels=g.levels)
    nx.draw_networkx(g, pos=pos, labels=g.get_labels(), node_size=3000, node_color='white')
    # nx.draw_networkx_edges(g, pos=pos)
    # nx.draw_networkx_labels(g, pos, g.get_labels())
    plt.show()
