import networkx as nx

from sys import argv, stdin
from time import time

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


# 1, 1, 2, 5, 15, 52, 203, 877, 4140, 21 147, 115 975,
def test_partitions():
    g = read_graph(argv[1:3])
    start = time()
    print('Старт')
    division = partitions.divide(g)
    factors = []
    levels = {}
    nodes_levels = {}
    for part in partitions.partition(list(g.nodes), division):
        factor = partitions.FactorGraph(g, part)
        if is_tree(factor):
            factors.append(partitions.FactorGraph(g, part))
            if factor.level not in levels:
                levels[factor.level] = []
            levels[factor.level].append(factor)
            nodes_levels[factor.as_node] = factor.level
    levels = [levels[level] for level in sorted(levels)]
    print('Фактор-графы построены')
    for level, facs in enumerate(levels):
        print('Уровень:', level, 'Фактор-графов:', len(facs))
    print('Всего:', len(factors))

    lattice = nx.DiGraph()
    lattice.start = levels[0][0]
    lattice.levels = [[fac.as_node for fac in facs] for facs in levels]
    lattice.nodes_levels = nodes_levels
    for facs in levels:
        for fac in facs:
            lattice.add_node(fac.as_node)
    for level in range(len(levels) - 1):
        for fac_low in levels[level]:
            for fac_upper in levels[level + 1]:
                count = 0
                for cls in fac_low.cong:
                    if cls in fac_upper.cong_set:
                        count += 1
                if count == len(fac_low.cong) - 2:
                    lattice.add_edge(fac_low.as_node, fac_upper.as_node)
        print(f'Уровень {level} построен')
    print('Программа завершила работу за: {:.2f} секунд'.format(time() - start))
    if '-c' in argv:
        draw.draw_lattice(lattice, filename='tree_cong.png', show=False)


def main():
    #  test_lattice()
    test_partitions()


if __name__ == '__main__':
    main()
