# =============================================================================
# Pelote Network Projection Functions
# =============================================================================
#
# Functions used to compute various networkx projections such as bipartite
# to monopartite, for instance.
#
import math
import networkx as nx
from typing import Hashable, Optional, Counter, Any, Dict
from typing_extensions import Literal

from pelote.types import AnyGraph
from pelote.graph import check_graph
from pelote.utils import dict_without

MONOPARTITE_PROJECTION_METRICS = {
    "jaccard",
    "overlap",
    "cosine",
    "dice",
    "binary_cosine",
}
MonopartiteProjectionMetric = Literal[
    "jaccard", "overlap", "cosine", "dice", "binary_cosine"
]


def compute_metric(
    metric: Optional[MonopartiteProjectionMetric],
    norm1: float,
    norm2: float,
    i: float,
):
    if i == 0:
        return 0

    if metric == "cosine":
        return i / (norm1 * norm2)

    if metric == "jaccard":
        return i / (norm1 + norm2 - i)

    if metric == "dice":
        return (2 * i) / (norm1 + norm2)

    if metric == "overlap":
        return i / min(norm1, norm2)

    if metric == "binary_cosine":
        return i / math.sqrt(norm1 * norm2)

    return i


# TODO: bipartition check (is_bipartite_by, graph.py)
# TODO: partition is not empty
def monopartite_projection(
    bipartite_graph: AnyGraph,
    part_to_keep: Hashable,
    *,
    node_part_attr: str = "part",
    edge_weight_attr: str = "weight",
    metric: Optional[MonopartiteProjectionMetric] = None,
) -> AnyGraph:

    check_graph(bipartite_graph)

    if metric is not None and metric not in MONOPARTITE_PROJECTION_METRICS:
        raise TypeError(
            'unknown metric "%s", expecting one of %s'
            % (metric, ", ".join('"%s"' % m for m in MONOPARTITE_PROJECTION_METRICS))
        )

    monopartite_graph = nx.Graph()

    # Computing norms
    norms: Dict[Any, float] = {}

    for n1, a1 in bipartite_graph.nodes(data=True):
        p1 = a1[node_part_attr]

        if p1 != part_to_keep:
            continue

        norm: float = 0

        for token, ta in bipartite_graph[n1].items():
            weight = 1

            if metric == "cosine":
                weight = ta[edge_weight_attr]
                weight *= weight

            norm += weight

        if norm > 0:
            if metric == "cosine":
                norm = math.sqrt(norm)

            norms[n1] = norm

        monopartite_graph.add_node(n1, **dict_without(a1, node_part_attr))

    for n1, norm1 in norms.items():
        intersection: Counter[Any] = Counter()

        # Computing intersections
        for token, ta in bipartite_graph[n1].items():
            w1 = 1

            if metric == "cosine":
                w1 = ta[edge_weight_attr]

            for n2, a2 in bipartite_graph[token].items():

                # Don't compare to self
                if n2 == n1:
                    continue

                # NOTE: since we are dealing with undirected graphs we can
                # avoid doing the same computations twice.
                if n1 > n2:
                    continue

                w2 = 1

                if metric == "cosine":
                    w2 = a2[edge_weight_attr]

                intersection[n2] += w1 * w2

        # Finalizing metrics
        for n2, i in intersection.items():
            norm2 = norms[n2]
            weight = compute_metric(metric, norm1, norm2, i)

            # TODO: threshold can go there
            monopartite_graph.add_edge(n1, n2, weight=weight)

    return monopartite_graph
