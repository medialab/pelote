# =============================================================================
# Pelote Simmelian Backbone
# =============================================================================
#

from pelote.sparsification.utils import Sparsifier
from pelote.metrics import edge_redundancy


class SimmelianBackboneSparsifier(Sparsifier):
    def __init__(
        self,
        edge_strength_ranking_threshold: int = 0,
        edge_redundancy_threshold: int = 0,
        edge_weight_attr: str = "triangular_strength",
        keep_connected: bool = False,
        in_or_out_edge: str = "both",
        reciprocity: bool = False,
    ):
        def edge_predicate_factory(graph):
            redundancy = edge_redundancy(
                graph,
                edge_strength_ranking_threshold=edge_strength_ranking_threshold,
                edge_weight_attr=edge_weight_attr,
                in_or_out_edge=in_or_out_edge,
                reciprocity=reciprocity,
            )

            def predicate(u, v, a):
                return redundancy[u, v] >= edge_redundancy_threshold

            return predicate

        super().__init__(
            edge_predicate_factory=edge_predicate_factory, keep_connected=keep_connected
        )


def simmelian_backbone(
    graph,
    edge_strength_ranking_threshold: int = 0,
    edge_redundancy_threshold: int = 0,
    edge_weight_attr: str = "triangular_strength",
    keep_connected: bool = False,
    in_or_out_edge: str = "both",
    reciprocity: bool = False,
):
    """
    Function returning the simmelian backbone of the given graph, i.e. a copy
    of the graph were we only kept strong and redundant edges.

    Article:
        Bobo Nick, Conrad Lee, Pádraig Cunningham, Ulrik Brandes. "Simmelian Backbones:
        Amplifying Hidden Homophily in Facebook Networks." Proceedings of the 2013 IEEE/ACM
        International Conference on Advances in Social Networks Analysis and Mining (ASONAM 2013),
        2013, pp. 525-532, doi: 10.1145/2492517.2492569.

    References:
        paper: https://kops.uni-konstanz.de/bitstream/handle/123456789/25994/Nick_259941.pdf;jsessionid=1BBC287934DAD4BDC586594A487E7CD8?sequence=1
        additional: https://hal.archives-ouvertes.fr/tel-02339047/

    Args:
        graph (nx.AnyGraph): target graph.
        edge_strength_ranking_threshold (int, optional): strength ranking threshold.
            Defaults to 1.
        edge_redundancy_threshold (int, optional): redundancy threshold.
            Defaults to 1.
        edge_weight_attr (str, optional): name of the edge attribute holding
            the edge's weight. Defaults to "triangular_strength".
        keep_connected (bool, optional): whether to keep the graph connected
            as it is using the UMST method. Defaults to False.
        in_or_out_edge (str, optional): whether to consider ingoing edges, or outgoing edges,
            or both. Defaults to both.
        reciprocity (bool, optional): wether reciprocity within top ranks is counted as overlap.
            Defaults to False.

    Returns:
        nx.AnyGraph: the sparse graph.
    """
    return SimmelianBackboneSparsifier(
        edge_strength_ranking_threshold=edge_strength_ranking_threshold,
        edge_redundancy_threshold=edge_redundancy_threshold,
        edge_weight_attr=edge_weight_attr,
        keep_connected=keep_connected,
        in_or_out_edge=in_or_out_edge,
        reciprocity=reciprocity,
    )(graph)
