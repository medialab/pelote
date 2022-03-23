# =============================================================================
# Pelote Metrics Functions
# =============================================================================
#
from typing import Dict, Tuple, Any

from pelote.graph import check_graph
from pelote.types import AnyGraph


def edge_disparity(
    graph: AnyGraph, edge_weight_attr: str = "weight", reverse: bool = False
) -> Dict[Any, float]:
    """
    Function computing the disparity score of each edge in the given graph. This
    score is typically used to extract the multiscale backbone of a weighted
    graph.

    Args:
        graph(nx.AnyGraph): target graph.
        edge_weight_attr (str, optional): name of the edge attribute containing
            its weight.
            Defaults to "weight".
        reverse (bool, optional): whether to reverse the metric, i.e. return
            `1 - score`. Defaults to False.

    Returns:
        dict: Dictionnary with edges - (source, target) tuples - as keys and the disparity scores as values

    """
    check_graph(graph)

    # todo: raise if multigraph, raise if directed or at least change code to optimize

    if graph.is_directed():
        raise NotImplementedError

    disparities: Dict[Tuple[Any, Any], float] = {}

    # NOTE: we need to recast as dict to avoid the linear complexity trap
    # of networkx DegreeView...
    weighted_degrees = dict(graph.degree(weight=edge_weight_attr))

    for source in graph.nodes:
        source_degree = graph.degree(source)
        source_weighted_degree = weighted_degrees[source]

        for _, target, weight in graph.edges(source, data=edge_weight_attr):
            if source > target:
                continue

            target_degree = graph.degree(target)
            target_weighted_degree = weighted_degrees[target]

            normalized_weight_source = weight / source_weighted_degree
            normalized_weight_target = weight / target_weighted_degree

            source_score = (1 - normalized_weight_source) ** (source_degree - 1)
            target_score = (1 - normalized_weight_target) ** (target_degree - 1)

            d = min(source_score, target_score)

            if reverse:
                d = 1.0 - d

            disparities[(source, target)] = d

    return disparities
