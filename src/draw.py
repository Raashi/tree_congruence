from networkx import draw_networkx, Graph
from matplotlib.pyplot import figure, savefig, clf, gca, ylim

from lattice import Lattice


fig_sizes = {
    1: (2, 2),
    2: (2, 3),
    3: (3, 7),
    4: (7, 7),
    5: (12, 10),
    6: (18, 18),
    7: (40, 22),
    8: (60, 40)
}


def split_label(label: str):
    if '{' not in label:
        return label
    res = []
    while '{' in label:
        lpos = label.find('{')
        rpos = label.find('}')
        res.append(label[lpos:rpos + 1])
        label = label[rpos + 2:]
    res = '\n'.join(res)
    return res


def lattice_pos(g: Lattice, root, levels):
    currents = [0] * len(levels)
    dy = 1 / (len(levels) - 1) if len(levels) > 1 else 0.5

    def _make_pos(pos, node):
        level = g.nodes_levels[node]
        dx = 1 / len(levels[level])
        left = dx / 2
        pos[node] = (left + dx * currents[level], -1 + dy * level)
        currents[level] += 1
        for outer_node in g.successors(node):
            if outer_node not in pos:
                _make_pos(pos, outer_node)

    res = {}
    _make_pos(res, root)
    return res


def draw_lattice(g: Lattice, filename: str):
    clf()
    pos = lattice_pos(g, g.start.string, levels=g.levels)
    fig_size = fig_sizes.get(g.g.number_of_nodes(), (100, 100))
    figure(figsize=fig_size)
    labels = {node: split_label(node) for node in g.nodes}
    draw_networkx(g, pos=pos, node_size=4000, node_color='white', dpi=800, labels=labels, font_size=18)
    ylim(-1 - 1 / fig_size[1] / 2, 1 / fig_size[1] / 2)
    gca().axis('off')
    savefig(filename, bbox_inches='tight')
    clf()


def draw_tree(g: Graph, filename):
    clf()
    figure(figsize=(2, 2) if g.number_of_nodes() <= 6 else (6, 4))
    draw_networkx(g, node_color='white', font_size=14)
    gca().axis('off')
    savefig(filename, bbox_inches='tight')
    clf()
