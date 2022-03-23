# =============================================================================
# Pelote Sparsification Methods
# =============================================================================
#
# Collection of sparsification methods & helpers.
#
from typing import Optional

from pelote.types import AnyGraph
from pelote.graph import filter_edges


def global_threshold_sparsification(
    graph: AnyGraph,
    weight_threshold: float,
    edge_weight_attr: str = "weight",
    reverse: Optional[bool] = False,
) -> AnyGraph:
    """
    Function returning a copy of the given graph without edges whose weight
    is less than a given threshold.

    Args:
        graph (nx.AnyGraph): target graph.
        weight_threshold (float): weight threshold.
        reverse (bool, optional): whether to reverse the threshold condition.
            That is to say an edge would be removed if its weight is greater
            than the threshold.

    Returns:
        nx.AnyGraph: the sparse version of the graph.
    """

    if reverse:

        def edge_predicate(u, v, a):
            return a[edge_weight_attr] <= weight_threshold

    else:

        def edge_predicate(u, v, a):
            return a[edge_weight_attr] >= weight_threshold

    return filter_edges(graph, edge_predicate)
