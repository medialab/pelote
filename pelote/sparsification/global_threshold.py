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
    ):
        self.weight_threshold = weight_threshold
        self.edge_weight_attr = edge_weight_attr
        self.reverse = reverse

    def _get_edge_predicate(self):
        if self.reverse:
            return lambda _u, _v, a: a[self.edge_weight_attr] <= self.weight_threshold

        return lambda _u, _v, a: a[self.edge_weight_attr] >= self.weight_threshold


def global_threshold_sparsification(
    graph,
    weight_threshold: float,
    edge_weight_attr: str = "weight",
    reverse: bool = False,
):
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
    return GlobalThresholdSparsifier(
        weight_threshold=weight_threshold,
        edge_weight_attr=edge_weight_attr,
        reverse=reverse,
    ).filter(graph)
