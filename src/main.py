#!/usr/bin/env/ python
import networkx as nx
import matplotlib.pyplot as plt

from sys import argv, stdin

import alg
import draw


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


def test_main_factors():
    g = read_graph(argv[1:3])
    # draw_graph_circular(g)

    factor_default = alg.FactorGraph.get_default(g)
    factors = list(factor_default.get_mains())
    if not len(factors):
        print('Граф имеет только тождественную конгруэнцию')
        return
    fac = factors[0]
    factors_cool = fac.get_mains()
    print(fac.cong)
    print("-" * 20)
    for factor in factors_cool:
        print(factor.cong)


def test_tree():
    g = read_graph(argv[1:3])
    print(alg.is_tree(g))


def test_half_lattice():
    g = read_graph(argv[1:3])
    hl = alg.HalfLattice(g)
    for level, nodes_with_level in enumerate(hl.levels):
        print(level, ':', [node for node in nodes_with_level])
    draw.draw_lattice(hl)


def test_lattice():
    g = read_graph(argv[1:3])
    lattice = alg.Lattice(g)
    for level, nodes_with_level in enumerate(lattice.levels):
        print(level, ':', [node for node in nodes_with_level])
    draw.draw_lattice(lattice)


def main():
    # test_half_lattice()
    # test_tree()
    test_lattice()


if __name__ == '__main__':
    main()
