# =============================================================================
# Pelote Graph Helpers
# =============================================================================
#
# Miscellaneous helper functions to deal with networkx graphs.
#
import networkx as nx
from typing import Set, Any, Optional, List

from pelote.types import AnyGraph


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
