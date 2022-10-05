from ebbe import Timer
import networkx as nx
from random import random

g = nx.fast_gnp_random_graph(4000, 40000)
set_nodes = set()

for n in g.nodes:
    if random() > 0.25:
        weight = 10
    else:
        weight = 0
    g.nodes[n]["weight"] = weight

    if random() > 0.25:
        set_nodes.add(n)


def filter_nodes_iter_edges(graph, predicate):
    """
    Function returning a copy of the given networkx graph but without the nodes
    filtered out by the given predicate function

    Args:
        graph (nx.AnyGraph): a networkx graph.
        predicate (callable): a function taking each node and node attributes
            and returning True if you want to keep the node or False if you want
            to remove it.

    Returns:
        nx.AnyGraph: the filtered graph.

    Example:
        from pelote import filter_nodes

        g = nx.Graph()
        g.add_node(1, weight=22)
        g.add_node(2, weight=4)
        g.add_edge(1, 2)

        h = filter_nodes(g, lambda n, a: a["weight"] >= 10)
    """

    if not callable(predicate):
        raise TypeError("expecting a callable predicate (i.e. a function etc.)")

    copy = graph.__class__()

    for n, a in graph.nodes.data():
        if predicate(n, a):
            copy.add_node(n, **a)
    for u, v, a in graph.edges.data():
        if u in copy.nodes.data() and v in copy.nodes.data():
            copy.add_edge(u, v, **a)
    return copy


def filter_nodes_iter_nodes_edges(graph, predicate):
    """
    Function returning a copy of the given networkx graph but without the nodes
    filtered out by the given predicate function

    Args:
        graph (nx.AnyGraph): a networkx graph.
        predicate (callable): a function taking each node and node attributes
            and returning True if you want to keep the node or False if you want
            to remove it.

    Returns:
        nx.AnyGraph: the filtered graph.

    Example:
        from pelote import filter_nodes

        g = nx.Graph()
        g.add_node(1, weight=22)
        g.add_node(2, weight=4)
        g.add_edge(1, 2)

        h = filter_nodes(g, lambda n, a: a["weight"] >= 10)
    """

    if not callable(predicate):
        raise TypeError("expecting a callable predicate (i.e. a function etc.)")

    copy = graph.__class__()
    directed = graph.is_directed()
    multi = graph.is_multigraph()

    for n, a in graph.nodes.data():
        if predicate(n, a):
            copy.add_node(n, **a)
            if directed:
                if multi:
                    for u, v, k, a_edge in graph.out_edges(n, keys=True, data=True):
                        if predicate(v, graph.nodes[v]):
                            copy.add_edge(u, v, key=k, **a_edge)
                else:
                    for u, v in graph.out_edges(n):
                        if predicate(v, graph.nodes[v]):
                            copy.add_edge(u, v, **graph.out_edges[u, v])
            else:
                if multi:
                    for u, v, k, a_edge in graph.edges(n, keys=True, data=True):
                        if u > v and predicate(v, graph.nodes[v]):
                            copy.add_edge(u, v, key=k, **a_edge)
                else:
                    for u, v in graph.edges(n):
                        if u > v and predicate(v, graph.nodes[v]):
                            copy.add_edge(u, v, **graph.edges[u, v])
    return copy


with Timer("Iter on edges (keep a lot of nodes with the predicate)"):
    a = filter_nodes_iter_edges(g, lambda n, a: a["weight"] >= 10)

with Timer("Iter on nodes edges (keep a lot of nodes with the predicate)"):
    b = filter_nodes_iter_nodes_edges(g, lambda n, a: a["weight"] >= 10)

with Timer("Iter on edges (keep only a few nodes with the predicate)"):
    a = filter_nodes_iter_edges(g, lambda n, a: a["weight"] < 10)

with Timer("Iter on nodes edges (keep only a few nodes with the predicate)"):
    b = filter_nodes_iter_nodes_edges(g, lambda n, a: a["weight"] < 10)

with Timer("Iter on edges (predicate on a set"):
    a = filter_nodes_iter_edges(g, lambda n, a: n in set_nodes)

with Timer("Iter on nodes edges (predicate on a set)"):
    b = filter_nodes_iter_nodes_edges(g, lambda n, a: n in set_nodes)
