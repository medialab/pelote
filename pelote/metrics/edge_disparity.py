# =============================================================================
# Pelote Edge Disparity Metric
# =============================================================================
#
from pelote.graph import check_graph


def edge_disparity(graph, edge_weight_attr: str = "weight", reverse: bool = False):
    """
    Function computing the disparity score of each edge in the given graph. This
    score is typically used to extract the multiscale backbone of a weighted
    graph.

    The formula from the paper (relying on integral calculus) can be simplified
    to become:

    ```
    disparity(u, v) = min(
        (1 - normalizedWeight(u, v)) ^ (degree(u) - 1)),
        (1 - normalizedWeight(v, u)) ^ (degree(v) - 1))
    )
    ```

    where

    ```
    normalizedWeight(u, v) = weight(u, v) / weightedDegree(u)
    weightedDegree(u) = sum(weight(u, v) for v in neighbors(u))
    ```

    This score can sometimes be found reversed likewise:

    ```
    disparity(u, v) = max(
        1 - (1 - normalizedWeight(u, v)) ^ (degree(u) - 1)),
        1 - (1 - normalizedWeight(v, u)) ^ (degree(v) - 1))
    )
    ```

    so that higher score means better edges. We chose to keep the metric close
    to the paper to keep the statistical test angle. This means that, in this
    implementation at least, a low score for an edge means a high relevance and
    increases its chances to be kept in the backbone.

    Note that this algorithm has no proper definition for directed graphs and
    is only useful if edges have varying weights. This said, it could be
    possible to compute the disparity score only based on edge direction, if
    we drop the min part.

    Article:
        Serrano, M. Ángeles, Marián Boguná, and Alessandro Vespignani. "Extracting
        the multiscale backbone of complex weighted networks." Proceedings of the
        national academy of sciences 106.16 (2009): 6483-6488.

    References:
        paper: https://www.pnas.org/content/pnas/106/16/6483.full.pdf
        wikipedia: https://en.wikipedia.org/wiki/Disparity_filter_algorithm_of_weighted_network

    Args:
        graph(nx.AnyGraph): target graph.
        edge_weight_attr (str, optional): name of the edge attribute containing
            its weight.
            Defaults to "weight".
        reverse (bool, optional): whether to reverse the metric, i.e. higher weight
            means more relevant edges. Defaults to False.

    Returns:
        dict: Dictionnary with edges - (source, target) tuples - as keys and the disparity scores as values
    """
    check_graph(graph)

    if graph.is_directed() or graph.is_multigraph():
        raise TypeError("edge_disparity cannot work on a directed or multi graph")

    disparities = {}

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

            if reverse:
                source_score = 1.0 - source_score
                target_score = 1.0 - target_score

            # NOTE: for now we don't deal with directed graphs, so we have
            # the guarantee we have an undirected edge at this point
            disparities[(source, target)] = (
                min(source_score, target_score)
                if not reverse
                else max(source_score, target_score)
            )

    return disparities
