import networkx as nx

from copy import deepcopy
from itertools import combinations
import itertools


class FactorGraph(nx.Graph):
    def __init__(self, g: nx.Graph, cong: list):
        nx.Graph.__init__(self)
        self.g = g
        self.cong = cong
        self.add_nodes_from(cong)
        for cls_1, cls_2 in combinations(cong, 2):
            for u, v in itertools.product(cls_1, cls_2):
                if g.has_edge(u, v):
                    self.add_edge(cls_1, cls_2)
                    break

    def get_class_of_node(self, node):
        for cls in self.cong:
            if node in cls:
                return cls
        raise RuntimeError("Не найден класс вершины {}".format(node))

    @staticmethod
    def get_default(g: nx.Graph):
        if type(g) is FactorGraph:
            raise TypeError("Взятие тожественной конгруэнции возможно только для nx.Graph")
        cong = [tuple([node]) for node in g]
        return FactorGraph(g, cong)


def independent_subsets(g: nx.Graph, subset_1, subset_2):
    for u, v in itertools.product(subset_1, subset_2):
        if g.has_edge(u, v):
            return False
    return True


def get_class_of_node(cong: list, node):
    for cls in cong:
        if node in cls:
            return cls
    raise RuntimeError("Не найден класс вершины {}".format(node))


def get_default_cong(g: nx.Graph) -> nx.Graph:
    factor = nx.Graph()
    factor.cong = [tuple([node]) for node in g]
    for u, v in g.edges:
        factor.add_edge(tuple([u]), tuple([v]))
    return factor


def build_factor_graph(g: nx.Graph, cong: list) -> nx.Graph:
    factor = nx.Graph()
    factor.cong = cong
    factor.add_nodes_from(cong)
    for cls_1 in cong:
        for cls_2 in cong:
            if cls_1 == cls_2:
                continue
            stop = False
            for u in cls_1:
                for v in cls_2:
                    if g.has_edge(u, v):
                        factor.add_edge(cls_1, cls_2)
                        stop = True
                        break
                if stop:
                    break
    return factor


def get_main_elements(g: nx.Graph):
    default_cong = FactorGraph.get_default(g)
    main_factors = set()
    main_factors_congs = set()
    for node_1, node_2 in combinations(g, 2):
        if node_1 == node_2 or g.has_edge(node_1, node_2):
            continue
        cong = deepcopy(getattr(default_cong, "cong"))
        cls1 = get_class_of_node(cong, node_1)
        cls2 = get_class_of_node(cong, node_2)
        cong.remove(cls1), cong.remove(cls2)
        cong.append(tuple(sorted(cls1 + cls2)))
        cong.sort()

        factor = build_factor_graph(default_cong, cong)
        cong_tuple = tuple(getattr(factor, "cong"))
        if cong_tuple not in main_factors_congs:
            main_factors_congs.add(cong_tuple)
            main_factors.add(factor)
    return main_factors


def get_main_elements_common(g: FactorGraph):
    main_factors = set()
    main_factors_congs = set()
    for cls_1, cls_2 in itertools.combinations(g.cong, 2):
        if not independent_subsets(g.g, cls_1, cls_2):
            continue
        cong = deepcopy(g.cong)
        cong.remove(cls_1), cong.remove(cls_2)
        cong.append(tuple(sorted(cls_1 + cls_2)))
        cong.sort()

        factor = FactorGraph(g.g, cong)
        cong_tuple = tuple(getattr(factor, "cong"))
        if cong_tuple not in main_factors_congs:
            main_factors_congs.add(cong_tuple)
            main_factors.add(factor)
    return main_factors
