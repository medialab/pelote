# =============================================================================
# Pelote Graph Helpers
# =============================================================================
#
# Miscellaneous helper functions to deal with networkx graphs.
#
import networkx as nx
from heapq import nlargest

from pelote.classes import DFSStack

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

    for u, v in edges_to_drop:
        graph.remove_edge(u, v)


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
