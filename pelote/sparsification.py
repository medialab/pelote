# =============================================================================
# Pelote Sparsification Methods
# =============================================================================
#
# Collection of sparsification methods & helpers.
#
from typing import Optional

from pelote.types import AnyGraph
from pelote.graph import filter_edges, check_graph
from pelote.metrics import edge_disparity


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
        nx.AnyGraph: the sparse graph.
    """
    check_graph(graph)

    if reverse:

        def edge_predicate(u, v, a):
            return a[edge_weight_attr] <= weight_threshold

    else:

        def edge_predicate(u, v, a):
            return a[edge_weight_attr] >= weight_threshold

    return filter_edges(graph, edge_predicate)


def multiscale_backbone(
    graph: AnyGraph, alpha: float = 0.05, edge_weight_attr: str = "weight"
) -> AnyGraph:
    """
    Function returning the multiscale backbone of the given graph, i.e. a copy
    of the graph were we only kept "relevant" edges, as defined by a
    statistical test where we compare the likelihood of a weighted edge existing
    vs. the null model.

    Article:
        Serrano, M. Ángeles, Marián Boguná, and Alessandro Vespignani. "Extracting
        the multiscale backbone of complex weighted networks." Proceedings of the
        national academy of sciences 106.16 (2009): 6483-6488.

    References:
        - https://www.pnas.org/content/pnas/106/16/6483.full.pdf
        - https://en.wikipedia.org/wiki/Disparity_filter_algorithm_of_weighted_network

    Args:
        graph (nx.AnyGraph): target graph.
        alpha (float, optional): alpha value for the statistical test. It can
            be intuitively thought of as a p-value score for an edge to be
            kept in the resulting graph. Defaults to 0.05.
        edge_weight_attr (str, optional): name of the edge attribute holding
            the edge's weight. Defaults to "weight".

    Returns:
        nx.AnyGraph: the sparse graph.
    """
    check_graph(graph)

    # TODO: check directedness and constant weights

    disparity = edge_disparity(graph, edge_weight_attr=edge_weight_attr)

    def edge_predicate(u, v, a):
        return disparity[u, v] <= alpha

    return filter_edges(graph, edge_predicate)
