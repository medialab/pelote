# =============================================================================
# Pelote Multiscale Backbone
# =============================================================================
#
from pelote.metrics import edge_disparity
from pelote.sparsification.utils import Sparsifier


class MultiscaleBackboneSparsifier(Sparsifier):
    def __init__(
        self,
        alpha: float = 0.05,
        edge_weight_attr: str = "weight",
        keep_connected: bool = False,
    ):
        def edge_predicate_factory(graph):
            disparity = edge_disparity(graph, edge_weight_attr=edge_weight_attr)

            def predicate(u, v, a):
                if u > v:
                    u, v = v, u

                return disparity[u, v] <= alpha

            return predicate

        super().__init__(
            edge_predicate_factory=edge_predicate_factory, keep_connected=keep_connected
        )


def multiscale_backbone(
    graph,
    alpha: float = 0.05,
    edge_weight_attr: str = "weight",
    keep_connected: bool = False,
):
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
        keep_connected (bool, optional): whether to keep the graph connected
            as it is using the UMST method. Defaults to False.

    Returns:
        nx.AnyGraph: the sparse graph.
    """
    return MultiscaleBackboneSparsifier(
        alpha=alpha, edge_weight_attr=edge_weight_attr, keep_connected=keep_connected
    )(graph)
