# =============================================================================
# Pelote Global Threshold Sparsification
# =============================================================================
#
from pelote.sparsification.utils import Sparsifier


class GlobalThresholdSparsifier(Sparsifier):
    def __init__(
        self,
        weight_threshold: float,
        edge_weight_attr: str = "weight",
        reverse: bool = False,
        keep_connected: bool = False,
    ):
        def edge_predicate_factory(_):
            if reverse:
                return lambda _u, _v, a: a[edge_weight_attr] <= weight_threshold

            return lambda _u, _v, a: a[edge_weight_attr] >= weight_threshold

        super().__init__(
            edge_predicate_factory=edge_predicate_factory, keep_connected=keep_connected
        )


def global_threshold_sparsification(
    graph,
    weight_threshold: float,
    edge_weight_attr: str = "weight",
    reverse: bool = False,
    keep_connected: bool = False,
):
    """
    Function returning a copy of the given graph without edges whose weight
    is less than a given threshold.

    Args:
        graph (nx.AnyGraph): target graph.
        weight_threshold (float): weight threshold.
        edge_weight_attr (str, optional): name of the edge weight attribute.
        reverse (bool, optional): whether to reverse the threshold condition.
            That is to say an edge would be removed if its weight is greater
            than the threshold.
        keep_connected (bool, optional): whether to keep the graph connected
            as it is using the UMST method. Defaults to False.

    Returns:
        nx.AnyGraph: the sparse graph.
    """
    return GlobalThresholdSparsifier(
        weight_threshold=weight_threshold,
        edge_weight_attr=edge_weight_attr,
        reverse=reverse,
        keep_connected=keep_connected,
    )(graph)
