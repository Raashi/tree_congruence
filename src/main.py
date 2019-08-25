#!/usr/bin/env/ python
import networkx as nx
import matplotlib.pyplot as plt

from sys import argv, stdin

import lattice


def draw_graph_circular(g: nx.Graph):
    nx.draw_circular(g)
    plt.show()


def init_graph(io_obj):
    edges_count = int(io_obj.readline())
    edges = [tuple(io_obj.readline().strip().split(" "))
             for _ in range(edges_count)]
    g = nx.Graph()
    for edge in edges:
        for vertex in edge:
            if vertex not in g:
                g.add_node(vertex)
    g.add_edges_from(edges)
    return g


def read_graph(args) -> nx.Graph:
    source_possible = ["-c", "-f"]
    source = args[0]
    if source not in source_possible:
        raise RuntimeError("Введи коррекный источник ввода графа: -c или -f")
    g = None
    if source == "-c":
        g = init_graph(stdin)
    elif source == "-f":
        with open(args[1]) as src_file:
            g = init_graph(src_file)
    return g


def get_lattice_main_elements():
    g = read_graph(argv[1:3])
    # draw_graph_circular(g)

    factor_default = lattice.FactorGraph.get_default(g)
    factors = factor_default.get_mains()
    fac = next(factors.__iter__())
    factors_cool = fac.get_mains()
    print(fac.cong)
    print("-" * 20)
    for factor in factors_cool:
        print(factor.cong)


def test_tree():
    g = read_graph(argv[1:3])
    print(lattice.is_tree(g))


def main():
    # get_lattice_main_elements()
    test_tree()


if __name__ == '__main__':
    main()
