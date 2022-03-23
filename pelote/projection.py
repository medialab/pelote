# =============================================================================
# Pelote Network Projection Functions
# =============================================================================
#
# Functions used to compute various networkx projections such as bipartite
# to monopartite, for instance.
#
import math
import networkx as nx
from typing import (
    cast,
    Hashable,
    Optional,
    Counter,
    Any,
    Dict,
    Collection,
    Union,
    Iterable,
)
from typing_extensions import Literal

from pelote.types import AnyGraph
from pelote.graph import check_graph
from pelote.utils import dict_without, has_constant_time_lookup

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


Part = Union[Hashable, Collection[Any]]


def monopartite_projection(
    bipartite_graph: AnyGraph,
    part_to_keep: Part,
    *,
    node_part_attr: str = "part",
    edge_weight_attr: str = "weight",
    metric: Optional[MonopartiteProjectionMetric] = None,
    bipartition_check: bool = True,
    weight_threshold: Optional[float] = None
) -> AnyGraph:
    """
    Function returning the monopartite projection of a given bipartite graph
    wrt one of both partitions of the graph.

    That is to say the resulting graph will keep a single type of nodes sharing
    weighted edges based on the neighbors they shared in the bipartite graph.

    Example:
        import networkx as nx
        from pelote import monopartite_projection

        bipartite = nx.Graph()
        bipartite.add_nodes_from([1, 2, 3], part='account')
        bipartite.add_nodes_from([4, 5, 6], part='color')
        bipartite.add_edges_from([
            (1, 4),
            (1, 5),
            (2, 6),
            (3, 4),
            (3, 6)
        ])

        # Resulting graph will only contain nodes [1, 2, 3]
        # with edges: (1, 3) and (2, 3)
        monopartite = monopartite_projection(bipartite, 'account')

    Args:
        bipartite_graph (nx.AnyGraph): target graph. The function will raise
            if given graph is not truly bipartite.
        part_to_keep (Hashable or Collection): partition to keep in the projected
            graph. It can either be the value of the part node attribute in the
            given graph (a string, most commonly), or a collection (a set, list etc.)
            holding the nodes composing the part to keep.
        node_part_attr (str, optional): name of the node attribute containing
            the part the node belongs to. Defaults to "part".
        edge_weight_attr (str, optional): name of the edge attribute containing
            the edge's weight. Defaults to "weight".
        metric (str, optional): one of "jaccard", "overlap", "cosine", "dice"
            or "binary_cosine". If not given, resulting weight will be seyto the
            size of neighbor intersection. Defaults to None.
        bipartition_check (bool, optional): whether to check if given graph
            is truly bipartite. You can disable this as an optimization
            strategy if you know what you are doing. Defaults to True.
        weight_threshold (float, optional): if an edge weight should be less
            than this threshold we would not add it to the projected
            monopartite graph. Defaults to None.

    Returns:
        nx.Graph: the projected monopartite graph.
    """
    check_graph(bipartite_graph)

    if metric is not None and metric not in MONOPARTITE_PROJECTION_METRICS:
        raise TypeError(
            'unknown metric "%s", expecting one of %s'
            % (metric, ", ".join('"%s"' % m for m in MONOPARTITE_PROJECTION_METRICS))
        )

    if weight_threshold is not None and (
        not isinstance(weight_threshold, (int, float)) or weight_threshold <= 0
    ):
        raise TypeError("weight_threshold should be a number >= 0")

    # Null graph early exit
    if bipartite_graph.order() == 0:
        return nx.Graph()

    monopartite_graph = nx.Graph()

    part_to_keep_as_set = not isinstance(part_to_keep, Hashable)

    if part_to_keep_as_set:
        if not has_constant_time_lookup(part_to_keep):
            part_to_keep = set(cast(Iterable[Any], part_to_keep))

    # Computing norms
    norms: Dict[Any, float] = {}
    part_is_empty = True

    for n1, a1 in bipartite_graph.nodes(data=True):
        if part_to_keep_as_set:
            if n1 not in part_to_keep:  # type: ignore
                continue
        else:
            p1 = a1.get(node_part_attr)

            if p1 != part_to_keep:
                continue

        part_is_empty = False
        norm: float = 0

        for token, ta in bipartite_graph[n1].items():
            if bipartition_check:
                if (part_to_keep_as_set and token in part_to_keep) or ta.get(  # type: ignore
                    node_part_attr
                ) == part_to_keep:
                    raise TypeError(
                        'given graph is not truly bipartite because of an edge between two nodes of the same part: "%s" and "%s"'
                        % (n1, token)
                    )

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

    if part_is_empty:
        raise TypeError(
            '"%s" part does not exist in given graph. Are you sure your nodes have a "%s" attribute?'
            % (part_to_keep, node_part_attr)
        )

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

            if weight_threshold is not None and weight < weight_threshold:
                continue

            monopartite_graph.add_edge(n1, n2, weight=weight)

    return monopartite_graph
