# =============================================================================
# Pelote Graph Helpers
# =============================================================================
#
# Miscellaneous helper functions to deal with networkx graphs.
#
import networkx as nx
from typing import Set, Any, Optional, List, Callable, Dict
from typing_extensions import TypeGuard

from pelote.types import AnyGraph

GRAPH_TYPES = (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)


def is_graph(value: Any) -> TypeGuard[AnyGraph]:
    """
    Function returning whether the given value is a networkx graph.

    Args:
        value (any): value to test.

    Returns
        bool
    """
    return isinstance(value, GRAPH_TYPES)


def check_graph(value: Any) -> None:
    """
    Function raising if the given value is not a networkx graph.

    Args:
        value (any): value to test.
    """
    if not is_graph(value):
        raise TypeError("expected a networkx graph but got %s" % type(value).__name__)


def largest_connected_component(graph: AnyGraph) -> Optional[Set[Any]]:
    """
    Function returning the largest connected component of given networkx graph
    as a set of nodes.

    Args:
        graph (nx.AnyGraph): target graph.

    Returns:
        set: set of nodes representing the largest connected component.
    """

    largest = None
    remaining_nodes = graph.order()

    for component in nx.connected_components(graph):
        if largest is None or len(component) > len(largest):
            largest = component

        # Early exit
        remaining_nodes -= len(largest)

        if len(largest) > remaining_nodes:
            break

    return largest


def crop_to_largest_connected_components(graph: AnyGraph) -> None:
    """
    Function mutating the given networkx graph in order to keep only the
    largest connected component.

    Args:
        graph (nx.AnyGraph): target graph.
    """
    component = largest_connected_component(graph)

    if component is None:
        return

    nodes_to_drop: List[Any] = []

    for node in graph:
        if node not in component:
            nodes_to_drop.append(node)

    for node in nodes_to_drop:
        graph.remove_node(node)


def have_same_nodes(A: AnyGraph, B: AnyGraph, check_attributes: bool = False) -> bool:
    if A.order() != B.order():
        return False

    for node, attr in A.nodes.data():
        if node not in B:
            return False

        if check_attributes and attr != B.nodes[node]:
            return False

    return True


def have_same_edges(A: AnyGraph, B: AnyGraph, check_attributes: bool = False) -> bool:
    if A.size() != B.size():
        return False

    for u, v, attr in A.edges.data():
        if not B.has_edge(u, v):
            return False

        if check_attributes and attr != B[u][v]:
            return False

    return True


def are_same_graphs(A: AnyGraph, B: AnyGraph, check_attributes: bool = False) -> bool:
    return have_same_nodes(A, B, check_attributes=check_attributes) and have_same_edges(
        A, B, check_attributes=check_attributes
    )


def remove_edges(
    graph: AnyGraph, predicate: Callable[[Any, Any, Dict[Any, Any]], bool]
) -> None:
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
    if not callable(predicate):
        raise TypeError("expecting a callable predicate (i.e. a function etc.)")

    edges_to_drop = []

    for u, v, a in graph.edges.data():
        if not predicate(u, v, a):
            edges_to_drop.append((u, v))

    for u, v in edges_to_drop:
        graph.remove_edge(u, v)
