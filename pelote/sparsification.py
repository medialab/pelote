# =============================================================================
# Pelote Sparsification Methods
# =============================================================================
#
# Collection of sparsification methods & helpers.
#
from pelote.types import AnyGraph
from pelote.graph import remove_edges


def global_threshold_sparsify(
    graph: AnyGraph, threshold: float, edge_weight_attr: str = "weight"
) -> None:
    """
    Function sparsifying a networkx graph by removing all its edges
    having a weight less than a given threshold.

    Note that this function mutates the given graph.

    Args:
        graph (nx.AnyGraph): target graph.
        threshold (float): weight threshold.
    """

    def edge_predicate(u, v, a):
        return a[edge_weight_attr] >= threshold

    remove_edges(graph, edge_predicate)
