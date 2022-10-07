# =============================================================================
# Pelote Graph Helpers
# =============================================================================
#
# Miscellaneous helper functions to deal with networkx graphs.
#
import networkx as nx
from heapq import nlargest

from pelote.classes import DFSStack, DisjointSet

GRAPH_TYPES = (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)


def is_graph(value) -> bool:
    """
    Function returning whether the given value is a networkx graph.

    Args:
        value (any): value to test.

    Returns
        bool
    """
    return isinstance(value, GRAPH_TYPES)


def check_graph(value) -> None:
    """
    Function raising if the given value is not a networkx graph.

    Args:
        value (any): value to test.
    """
    if not is_graph(value):
        raise TypeError("expected a networkx graph but got %s" % type(value).__name__)


def check_node_exists(g, n):
    if n not in g:
        raise KeyError("Node {} does not exist. {}".format(n, g.nodes))

    return n


def create_null_copy(graph):
    check_graph(graph)

    return graph.__class__(**graph.graph)


def largest_connected_component(graph):
    """
    Function returning the largest connected component of given networkx graph
    as a set of nodes.

    Note that this function will consider any given graph as undirected and
    will therefore work with weakly connected components in the directed case.

    Args:
        graph (nx.AnyGraph): target graph.

    Returns:
        set: set of nodes representing the largest connected component.
    """
    check_graph(graph)

    largest = None
    remaining_nodes = graph.order()

    components = (
        nx.connected_components
        if not graph.is_directed()
        else nx.weakly_connected_components
    )

    for component in components(graph):
        if largest is None or len(component) > len(largest):
            largest = component

        # Early exit
        remaining_nodes -= len(largest)

        if len(largest) > remaining_nodes:
            break

    return largest


def crop_to_largest_connected_component(graph) -> None:
    """
    Function mutating the given networkx graph in order to keep only the
    largest connected component.

    Note that this function will consider any given graph as undirected and
    will therefore work with weakly connected components in the directed case.

    Args:
        graph (nx.AnyGraph): target graph.
    """
    check_graph(graph)

    component = largest_connected_component(graph)

    if component is None:
        return

    nodes_to_drop = []

    for node in graph:
        if node not in component:
            nodes_to_drop.append(node)

    graph.remove_nodes_from(nodes_to_drop)


def largest_connected_component_subgraph(graph, as_view=False):
    """
    Function returning the largest connected component subgraph of the given
    networkx graph.

    Note that this function will consider any given graph as undirected and
    will therefore work with weakly connected components in the directed case.

    Args:
        graph (nx.AnyGraph): target graph.
        as_view (bool, optional): whether to return the subgraph as a view.
            Defaults to False.

    Returns:
        nx.AnyGraph: the subgraph.
    """
    check_graph(graph)

    component = largest_connected_component(graph) or set()

    if as_view:
        return graph.subgraph(component)

    subgraph = nx.create_empty_copy(graph)

    for node, attr in graph.nodes.data():
        subgraph.add_node(node, **attr)

    if not component:
        return subgraph

    for source, target, attr in graph.edges.data():

        # NOTE: we don't need to test target because we are dealing with
        # a connected component here
        if source not in component:
            continue

        subgraph.add_edge(source, target, **attr)

    return subgraph


def have_same_nodes(A, B, check_attributes: bool = False) -> bool:
    if A.order() != B.order():
        return False

    for node, attr in A.nodes.data():
        if node not in B:
            return False

        if check_attributes and attr != B.nodes[node]:
            return False

    return True


def have_same_edges(A, B, check_attributes: bool = False) -> bool:
    if A.size() != B.size():
        return False

    for u, v, attr in A.edges.data():
        if not B.has_edge(u, v):
            return False

        if check_attributes and attr != B[u][v]:
            return False

    return True


def are_same_graphs(A, B, check_attributes: bool = False) -> bool:
    return have_same_nodes(A, B, check_attributes=check_attributes) and have_same_edges(
        A, B, check_attributes=check_attributes
    )


def remove_edges(graph, predicate) -> None:
    """
    Function removing all edges that do not pass a predicate function from a
    given networkx graph.

    Note that this function mutates the given graph.

    Args:
        graph (nx.AnyGraph): a networkx graph.
        predicate (callable): a function taking each edge source, target and
            attributes and returning True if you want to keep the edge or False
            if you want to remove it.
    """
    check_graph(graph)

    if not callable(predicate):
        raise TypeError("expecting a callable predicate (i.e. a function etc.)")

    edges_to_drop = []

    for u, v, a in graph.edges.data():
        if not predicate(u, v, a):
            edges_to_drop.append((u, v))

    graph.remove_edges_from(edges_to_drop)


def filter_edges(graph, predicate):
    """
    Function returning a copy of the given networkx graph but without the edges
    filtered out by the given predicate function

    Args:
        graph (nx.AnyGraph): a networkx graph.
        predicate (callable): a function taking each edge source, target and
            attributes and returning True if you want to keep the edge or False
            if you want to remove it.

    Returns:
        nx.AnyGraph: the filtered graph.
    """
    check_graph(graph)

    if not callable(predicate):
        raise TypeError("expecting a callable predicate (i.e. a function etc.)")

    copy = nx.create_empty_copy(graph)

    for u, v, a in graph.edges.data():
        if predicate(u, v, a):
            copy.add_edge(u, v, **a)

    return copy


def remove_nodes(graph, predicate) -> None:
    """
    Function removing all nodes that do not pass a predicate function from a
    given networkx graph.

    Note that this function mutates the given graph.

    Args:
        graph (nx.AnyGraph): a networkx graph.
        predicate (callable): a function taking each node and node attributes
            and returning True if you want to keep the node or False if you want
            to remove it.

    Example:
        from pelote import remove_nodes

        g = nx.Graph()
        g.add_node(1, weight=22)
        g.add_node(2, weight=4)
        g.add_edge(1, 2)

        remove_nodes(g, lambda n, a: a["weight"] >= 10)
    """
    check_graph(graph)

    if not callable(predicate):
        raise TypeError("expecting a callable predicate (i.e. a function etc.)")

    nodes_to_drop = []

    for n, a in graph.nodes.data():
        if not predicate(n, a):
            nodes_to_drop.append(n)

    graph.remove_nodes_from(nodes_to_drop)


def filter_nodes(graph, predicate):
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

    copy = create_null_copy(graph)

    directed = graph.is_directed()
    multi = graph.is_multigraph()

    for n, a in graph.nodes.data():

        if not predicate(n, a):
            continue

        copy.add_node(n, **a)

        if directed:
            if multi:
                for u, v, k, a_edge in graph.out_edges(n, keys=True, data=True):
                    if predicate(v, graph.nodes[v]):
                        copy.add_edge(u, v, key=k, **a_edge)
            else:
                for u, v, a_edge in graph.out_edges(n, data=True):
                    if predicate(v, graph.nodes[v]):
                        copy.add_edge(u, v, **a_edge)
        else:
            if multi:
                for u, v, k, a_edge in graph.edges(n, keys=True, data=True):
                    if u > v and predicate(v, graph.nodes[v]):
                        copy.add_edge(u, v, key=k, **a_edge)
            else:
                for u, v, a_edge in graph.edges(n, data=True):
                    if u > v and predicate(v, graph.nodes[v]):
                        copy.add_edge(u, v, **a_edge)

    return copy


def remove_leaves(graph) -> None:
    """
    Function removing all leaves of the graph, i.e. the nodes incident to a
    single edge, i.e. the nodes with degree 1.

    This function is not recursive and will only remove one layer of leaves.

    Note that this function mutates the given graph.

    Args:
        graph (nx.AnyGraph): a networkx graph.

    Example:
        from pelote import remove_leaves

        g = nx.Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)

        remove_leaves(g)

        list(g.nodes)
        >>> [2]
    """
    remove_nodes(graph, lambda n, _: graph.degree(n) != 1)


def filter_leaves(graph) -> None:
    """
    Function returning a copy of the given networkx graph but without its leaves,
    i.e. the nodes incident to a single edge, i.e. the nodes with degree 1.

    This function is not recursive and will only filter only one layer of leaves.

    Args:
        graph (nx.AnyGraph): a networkx graph.

    Example:
        from pelote import remove_leaves

        g = nx.Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)

        h = filter_leaves(g)

        list(h.nodes)
        >>> [2]
    """
    return filter_nodes(graph, lambda n, _: graph.degree(n) != 1)


def connected_component_orders(
    graph,
    edge_filter=None,
):
    """
    Function yielding the given graph's connected component orders. It is
    faster than calling `len` on sets yielded by nx.connected_components and
    can use an edge filter function.

    Args:
        graph (nx.AnyGraph): a networkx graph.
        edge_filter (callable, optional): a function taking n1, n2 & the
            attributes and returning whether we should follow this edge or not.
            Defaults to None.

    Yields:
        int: the size of a connected component.
    """
    check_graph(graph)

    if edge_filter is not None and not callable(edge_filter):
        raise TypeError("edge_filter should be callable")

    # Wrapping generator to make sure type checking raises on call
    def generator():
        stack = DFSStack(graph)

        for node in stack.nodes_yet_unseen():
            stack.append(node)
            size = 0

            while len(stack) != 0:
                n1 = stack.pop()
                size += 1

                for _, n2, edge_attr in graph.edges(n1, data=True):
                    if edge_filter is not None and not edge_filter(n1, n2, edge_attr):
                        continue

                    stack.append(n2)

            yield size

    return generator()


def largest_connected_component_order(graph):
    """
    Function returning the order of the largest connected component of the given
    graph.

    Args:
        graph (nx.AnyGraph): target graph.

    Returns:
        int or None: order of the component or None if the graph is null.
    """
    if graph.order() == 0:
        return None

    return max(connected_component_orders(graph))


def second_largest_connected_component_order(graph, edge_filter=None):
    """
    Function returning the order of the second largest connected component
    of the given graph.

    Args:
        graph (nx.AnyGraph): target graph.
        edge_filter (callable, optional): a function taking n1, n2 & the
            attributes and returning whether we should follow this edge or not.
            Defaults to None.

    Returns:
        int or None: order of the component or None if the graph is null or has
            only a single component.
    """
    top2 = nlargest(2, connected_component_orders(graph, edge_filter))

    if len(top2) < 2:
        return None

    return top2[1]


WEIGHT_EPSILON = 1e-8


def union_of_maximum_spanning_trees(graph, edge_weight_attr: str = "weight"):
    """
    Generator yielding the edges belonging to any Maximum Spanning Tree (MST) of
    the given networkx graph.

    Note that this function will give to each edge with no weight a default
    weight of 1.

    Article:
        Arlind Nocaj, Mark Ortmann, and Ulrik Brandes "Untangling Hairballs.
        From 3 to 14 Degrees of Separation." Computer & Information Science,
        University of Konstanz, Germany, 2014, https://dx.doi.org/10.1007/978-3-662-45803-7_9.

    References:
        article: https://kops.uni-konstanz.de/bitstream/handle/123456789/30583/Nocaj_0-284485.pdf

    Args:
        graph (nx.AnyGraph): target graph.
        edge_weight_attr (str, optional): name of the edge weight attribute.
            Defaults to "weight".

    Yields:
        tuple: source, target, attributes
    """
    check_graph(graph)

    def generator():

        # Early exit
        if graph.size() == 0:
            return

        edges_sorted_by_decreasing_weight = sorted(
            graph.edges.data(),
            key=lambda edge: edge[2].get(edge_weight_attr, 1),
            reverse=True,
        )

        disjoint_set = DisjointSet(graph.order())
        current_bucket_weight = None
        relevant_bucket_edges = None

        for edge in edges_sorted_by_decreasing_weight:
            u, v, a = edge

            current_weight = a.get(edge_weight_attr, 1)

            # Do we change bucket?
            if (
                current_bucket_weight is None
                or current_bucket_weight - current_weight > WEIGHT_EPSILON
            ):
                if relevant_bucket_edges:
                    for relevant_edge in relevant_bucket_edges:
                        yield relevant_edge
                        disjoint_set.union(relevant_edge[0], relevant_edge[1])

                relevant_bucket_edges = []

                current_bucket_weight = current_weight

            if not disjoint_set.are_in_same_set(u, v):
                relevant_bucket_edges.append(edge)

        if relevant_bucket_edges:
            yield from relevant_bucket_edges

    return generator()
