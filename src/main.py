import networkx as nx

from sys import argv, stdin

from factor import FactorGraph
from lattice import HalfLattice
from utils import is_tree
import draw
import partitions


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
    if g.number_of_nodes() == 0:
        g.add_node('1')
    return g


def test_main_factors():
    g = read_graph(argv[1:3])

    factor_default = FactorGraph(g)
    factors = list(factor_default.get_mains(False))
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
    print(is_tree(g))


def test_half_lattice():
    g = read_graph(argv[1:3])
    hl = HalfLattice(g, False)
    for level, nodes_with_level in enumerate(hl.levels):
        print(level, ':', [node for node in nodes_with_level])
    if '-i' in argv:
        draw.draw_lattice(hl)


def test_lattice():
    g = read_graph(argv[1:3])
    lattice = HalfLattice(g, True)
    if '-i' in argv:
        draw.draw_lattice_images(lattice, filename='tree.png')
    if '-c' in argv:
        draw.draw_lattice(lattice, filename='tree_cong.png', show=False)


def test_partitions():
    g = read_graph(argv[1:3])
    division = partitions.divide(g)
    for part in partitions.partition(list(g.nodes), division):
        partitions.FactorGraph(g, part)


def main():
    # test_lattice()
    test_partitions()


if __name__ == '__main__':
    main()
