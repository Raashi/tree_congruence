from sys import argv, stdin
from time import time

from networkx import Graph

from lattice import Lattice
from draw import draw_lattice, draw_tree


def init_graph(io_obj):
    edges_count = int(io_obj.readline())
    edges = [tuple(io_obj.readline().strip().split(' '))
             for _ in range(edges_count)]
    g = Graph()
    for edge in edges:
        for vertex in edge:
            if vertex not in g:
                g.add_node(vertex)
    g.add_edges_from(edges)
    return g


def read_graph(args) -> Graph:
    source_possible = ['-r', '-f']
    source = args[0]
    if source not in source_possible:
        raise RuntimeError('Введи коррекный источник ввода графа: -r или -f')
    g = None
    if source == '-r':
        g = init_graph(stdin)
    elif source == '-f':
        with open(args[1]) as src_file:
            g = init_graph(src_file)
    if g.number_of_nodes() == 0:
        g.add_node('1')
    return g


# 1, 1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975,
def main(opts):
    opts = opts if opts is not None else argv
    g = read_graph(opts[1:3])
    levels_to_build = int(opts[opts.index('-l') + 1]) if '-l' in opts else None
    start = time()
    lattice = Lattice(g, levels_to_build)
    elapsed = time() - start
    lattice.save('lattice.txt')
    print('Количество построенных уровней =', lattice.levels_count)
    print('Построение заняло время =', elapsed)
    print('Количество элементов решетки =', lattice.number_of_nodes())
    if '-i' in opts:
        filename = opts[opts.index('-fn') + 1] if '-fn' in opts else 'diagram.png'
        draw_lattice(lattice, filename)
        print(f'Диаграмма построена и сохранена в файл {filename}')
    if '-it' in opts:
        filename = opts[opts.index('-tfn') + 1] if '-fn' in opts else 'tree.png'
        draw_tree(g, filename)
        print(f'Изображение дерева построено и сохранено в файл {filename}')


if __name__ == '__main__':
    main(None)
