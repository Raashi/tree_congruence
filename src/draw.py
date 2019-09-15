from io import BytesIO

import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from alg import HalfLattice


matplotlib.rcParams['image.composite_image'] = False


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


def draw_graph(g):
    fig = plt.figure(figsize=(3, 3))
    ax = plt.subplot(111)
    nx.draw_networkx(g,
                     font_size=20,
                     arrowsize=20,
                     width=2.0,
                     labels=g.get_labels(),
                     edge_color='red')
    ax.axis('off')
    obj = BytesIO()
    plt.savefig(obj)
    obj.seek(0)
    plt.close(fig)
    return obj


def draw_lattice(g: HalfLattice, *, dpi=500, show=True, filename=None, ret_object=False):
    pos = lattice_pos(g, g.start.get_str_cong(), levels=g.levels)
    plt.figure(figsize=(20, 20))
    nx.draw_networkx(g, pos=pos, labels=g.get_labels(), node_size=3000, node_color='white', dpi=dpi)
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

    nx.draw_networkx(g,
                     pos=pos,
                     node_size=3000,
                     with_labels=False,
                     node_color='white')

    trans = ax.transData.transform
    trans2 = fig.transFigure.inverted().transform

    piesize = 1 / min(max(len(level) for level in g.levels), len(g.levels) + 1) / 3
    p2 = piesize / 2.0
    for node in g:
        xx, yy = trans(pos[node])  # figure coordinates
        xa, ya = trans2((xx, yy))  # axes coordinates
        a = plt.axes([xa - p2, ya - p2, piesize, piesize])
        # a.set_aspect('equal')
        im = a.imshow(mpimg.imread(images[node]))
        # im.set_zorder(-1)
        a.axis('off')

    ax.axis('off')

    fig.savefig(filename, dpi=350)
