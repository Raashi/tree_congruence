from io import BytesIO

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from lattice import HalfLattice


_tree_id = 0


fig_sizes = {
    3: (20, 20),
    4: (20, 20),
    5: (20, 20),
    6: (50, 50),
    7: (100, 100),
    8: (200, 200)
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


def get_tree_id():
    global _tree_id
    _tree_id += 1
    return _tree_id


def lattice_pos(g: HalfLattice, root, levels):
    currents = [0] * len(levels)
    dy = 1 / len(levels)
    top = dy / 2

    def _make_pos(pos, node):
        level = g.nodes_levels[node]
        dx = 1 / len(levels[level])
        left = dx / 2
        pos[node] = (left + dx * currents[level], -1 + top + dy * level)
        currents[level] += 1
        for outer_node in g.successors(node):
            if outer_node not in pos:
                _make_pos(pos, outer_node)

    res = {}
    _make_pos(res, root)
    return res


def draw_graph(g):
    fig, ax = plt.subplots(figsize=(3, 3))
    fig.subplots_adjust(0.3, 0, 0.7, 1)
    nx.draw_networkx(g, font_size=16, arrowsize=20, width=2.0, node_color='w',
                     labels=g.get_labels(), edge_color='red', ax=ax)
    ax.axis('off')
    plt.tight_layout()
    obj = BytesIO()
    plt.savefig(obj, bbox_inches='tight')
    plt.savefig(f'trees/test_{get_tree_id()}.png', bbox_inches='tight')
    obj.seek(0)
    plt.close(fig)
    return obj


def draw_lattice(g: HalfLattice, *, dpi=500, show=True, filename=None, ret_object=False):
    pos = lattice_pos(g, g.start.as_node, levels=g.levels)
    plt.figure(figsize=fig_sizes[len(g.levels)])
    nx.draw_networkx(g, pos=pos, node_size=3000, node_color='white', dpi=dpi,
                     labels={node: split_label(node) for node in g.nodes})
    if filename is not None:
        plt.savefig(filename)
    if show:
        plt.show()
    if ret_object:
        obj = BytesIO()
        plt.savefig(obj)
        plt.clf()
        obj.seek(0)
        return obj
    plt.clf()


def draw_lattice_images(g: HalfLattice, *, filename='tree.png'):
    images = {}
    for node in g:
        factor = g.nodes[node]['fg']
        images[node] = draw_graph(factor)

    pos = lattice_pos(g, g.start.get_str_cong(), levels=g.levels)
    fig = plt.figure(figsize=(20, 20))
    ax = plt.subplot(111)

    img_size = 1 / min(max(len(level) for level in g.levels), len(g.levels) + 1) / 3
    img_size_half = img_size / 2.0
    for node in g:
        xa, ya = pos[node]
        # noinspection PyUnresolvedReferences
        ax.imshow(mpimg.imread(images[node]), zorder=2, extent=[xa - img_size_half,
                                                                xa + img_size_half,
                                                                ya - img_size_half,
                                                                ya + img_size_half])

    nx.draw_networkx_edges(g, pos=pos, node_size=6000, ax=ax)

    # noinspection PyUnresolvedReferences
    ax.set_ylim(-1, 0)
    # noinspection PyUnresolvedReferences
    ax.axis('off')
    fig.savefig(filename, dpi=350)
