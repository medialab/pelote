# =============================================================================
# Pelote Learning Routines
# =============================================================================
#
# Collection of learning function related to graph sparsification mostly.
#
import math
from typing import Optional

from pelote.types import AnyGraph
from pelote.graph import (
    largest_connected_component_order,
    second_largest_connected_component_order,
    check_graph,
)


def floatsam_threshold_learner(
    graph: AnyGraph,
    starting_threshold: float = 0.0,
    learning_rate: float = 0.01,
    max_drifter_order: Optional[int] = None,
    edge_weight_attr: str = "weight",
):
    """
    Function using an iterative algorithm to try and find the best weight
    threshold to apply to trim the given graph's edges while keeping the
    underlying community structure.

    It works by iteratively increasing the threshold and stopping as soon as
    a significant connected component starts to drift away from the principal
    one.

    This is basically an optimization algorithm applied to a complex nonlinear
    function using a very naive cost heuristic, but it works decently for typical
    cases as it emulates the method used by hand by some researchers when they
    perform this kind of task on Gephi, for instance.

    Args:
        graph (nx.Graph): Graph to sparsify.
        starting_threshold (float, optional): Starting similarity threshold.
            Defaults to `0.0`.
        learning_rate (float, optional): How much to increase the threshold
            at each step of the algorithm. Defaults to `0.05`.
        max_drifter_order (int, optional): Max order of component to detach itself
            from the principal one before stopping the algorithm. If not
            provided it will default to the logarithm of the graph's largest
            connected component's order.
        edge_weight_attr (str, optional): Name of the weight attribute.
            Defaults to "weight".

    Returns:
        float: The found threshold
    """
    check_graph(graph)

    if graph.size() == 0:
        return starting_threshold

    threshold = starting_threshold
    best_threshold = None

    def edge_filter(u, v, attr):
        return attr[edge_weight_attr] >= threshold

    if max_drifter_order is None:
        max_drifter_order = int(math.log(largest_connected_component_order(graph) or 1))

    while True:
        best_threshold = threshold
        threshold += learning_rate

        c = second_largest_connected_component_order(graph, edge_filter)

        if c is not None and c >= max_drifter_order:
            break

    return best_threshold
