# =============================================================================
# Pelote Metrics Functions
# =============================================================================
#
import math
from typing import Dict, Any

from pelote.types import AnyGraph


def edge_disparity(graph: AnyGraph) -> Dict[Any, float]:
    """
    Function computing the disparity score of each edge in the given graph. This
    score is typically used to extract the multiscale backbone of a weighted
    graph.

    Args:
        graph(nx.AnyGraph): target graph.

    Returns:
        dict: Dictionnary with edges - (source, target) tuples - as keys and the disparity scores as values

    """
    # todo: raise if multigraph

    weighted_degrees = dict.fromkeys(graph, 0.0)

    for source, target, data in graph.edges(data=True):
        weighted_degrees[source] += data["weight"]
        weighted_degrees[target] += data["weight"]

    disparities = {}
    first_edge = True

    for source, target, data in graph.edges(data=True):

        if first_edge:
            previous = source
            previous_degree = graph.degree(source)
            previous_weighted_degree = weighted_degrees[source]
            first_edge = False

        if previous != source:
            previous = source
            previous_degree = graph.degree(source)
            previous_weighted_degree = weighted_degrees[source]

        target_degree = graph.degree(target)
        target_weighted_degree = weighted_degrees[target]

        weight = data["weight"]

        normalized_weight_source = weight / previous_weighted_degree
        normalized_weight_target = weight / target_weighted_degree

        source_score = math.pow(1 - normalized_weight_source, previous_degree - 1)
        target_score = math.pow(1 - normalized_weight_target, target_degree - 1)

        disparities[(source, target)] = min(source_score, target_score)

    return disparities
