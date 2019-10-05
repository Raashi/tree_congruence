from sys import argv, stdin

from networkx import Graph

from lattice import Lattice
from draw import draw_lattice, draw_lattice_images


def init_graph(io_obj):
    edges_count = int(io_obj.readline())
    edges = [tuple(io_obj.readline().strip().split(" "))
             for _ in range(edges_count)]
    g = Graph()
    for edge in edges:
        for vertex in edge:
            if vertex not in g:
                g.add_node(vertex)
    g.add_edges_from(edges)
    return g


def read_graph(args) -> Graph:
    source_possible = ["-r", "-f"]
    source = args[0]
    if source not in source_possible:
        raise RuntimeError("Введи коррекный источник ввода графа: -r или -f")
    g = None
    if source == "-r":
        g = init_graph(stdin)
    elif source == "-f":
        with open(args[1]) as src_file:
            g = init_graph(src_file)
    if g.number_of_nodes() == 0:
        g.add_node('1')
    return g


# 1, 1, 2, 5, 15, 52, 203, 877, 4140, 21 147, 115 975,
def main():
    g = read_graph(argv[1:3])
    levels_to_build = int(argv[2 if '-r' in argv else 3])
    lattice = Lattice(g, levels_to_build)
    if '-i' in argv:
        draw_lattice_images(lattice, filename='tree.png')
    if '-c' in argv:
        draw_lattice(lattice, filename='tree_cong.png', show=False)


if __name__ == '__main__':
    main()
