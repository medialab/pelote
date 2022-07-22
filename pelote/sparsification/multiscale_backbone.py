# =============================================================================
# Pelote Multiscale Backbone
# =============================================================================
#
from pelote.graph import filter_edges, check_graph
from pelote.metrics import edge_disparity


def multiscale_backbone(graph, alpha: float = 0.05, edge_weight_attr: str = "weight"):
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
        paper: https://www.pnas.org/content/pnas/106/16/6483.full.pdf
        wikipedia: https://en.wikipedia.org/wiki/Disparity_filter_algorithm_of_weighted_network

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
        # NOTE: swapping because we have the guarantee the graph is undirected
        # and the edge keys are arranged with lower node first
        if u > v:
            u, v = v, u

        return disparity[(u, v)] <= alpha

    return filter_edges(graph, edge_predicate)
