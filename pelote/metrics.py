# =============================================================================
# Pelote Metrics Functions
# =============================================================================
#
import math
from typing import Dict, Any

from pelote.types import AnyGraph, Indexable


def edge_disparity(
    graph: AnyGraph, edge_weight_attr: str = "weight"
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

    Returns:
        dict: Dictionnary with edges - (source, target) tuples - as keys and the disparity scores as values

    """
    # todo: raise if multigraph

    disparities = {}
    first_edge = True
    previous: Any
    weighted_degrees = graph.degree(weight=edge_weight_attr)

    for source, target, weight in graph.edges.data(data=edge_weight_attr):

        if first_edge or previous != source:
            previous = source
            previous_degree = graph.degree(source)
            previous_weighted_degree = weighted_degrees[source]
            first_edge = False

        target_degree = graph.degree(target)
        target_weighted_degree = weighted_degrees[target]

        normalized_weight_source = weight / previous_weighted_degree
        normalized_weight_target = weight / target_weighted_degree

        source_score = math.pow(1 - normalized_weight_source, previous_degree - 1)
        target_score = math.pow(1 - normalized_weight_target, target_degree - 1)

        disparities[(source, target)] = min(source_score, target_score)

    return disparities
