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


def get_lattice_main_elements():
    source_possible = ["-c", "-f"]
    source = argv[1]
    if source not in source_possible:
        raise RuntimeError("Введи коррекный источник ввода графа: -c или -f")

    g = None
    if source == "-c":
        g = init_graph(stdin)
    elif source == "-f":
        with open(argv[2]) as src_file:
            g = init_graph(src_file)
    # draw_graph_circular(g)

    factors = lattice.get_main_elements_common(lattice.FactorGraph.get_default(g))
    fac = next(factors.__iter__())
    factors_cool = lattice.get_main_elements_common(fac)
    print(getattr(fac, "cong"))
    print("-" * 20)
    for factor in factors_cool:
        print(getattr(factor, "cong"))


def main():
    get_lattice_main_elements()


if __name__ == '__main__':
    main()
