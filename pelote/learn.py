# =============================================================================
# Pelote Learning Routines
# =============================================================================
#
# Collection of learning function related to graph sparsification mostly.
#
import math
from collections import namedtuple

from pelote.graph import (
    largest_connected_component_order,
    second_largest_connected_component_order,
    check_graph,
)

FloatsamEpoch = namedtuple(
    "FloatsamEpoch", ["nth", "max_drifter_order", "drifter_order", "threshold"]
)


def floatsam_threshold_learner(
    graph,
    starting_threshold: float = 0.0,
    learning_rate: float = 0.01,
    max_drifter_order=None,
    edge_weight_attr: str = "weight",
    on_epoch=None,
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

    When working on metrics where lower is better (i.e. edge disparity), you
    can reverse the logic of the algorithm by tweaking `starting_threshold`
    and giving a negative `learning_rate`.

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
        on_epoch (callable, optional): Function called on each epoch of the
            algorithm with some metadata about iteration state.

    Returns:
        float: The found threshold
    """
    check_graph(graph)

    if on_epoch is not None and not callable(on_epoch):
        raise TypeError("on_epoch should be callable")

    if graph.size() == 0:
        return starting_threshold

    threshold = starting_threshold
    best_threshold = None

    def edge_filter(u, v, attr):
        return attr[edge_weight_attr] >= threshold

    if max_drifter_order is None:
        max_drifter_order = int(math.log(largest_connected_component_order(graph) or 1))

    n = 0

    while True:
        n += 1

        best_threshold = threshold
        threshold += learning_rate

        c = second_largest_connected_component_order(graph, edge_filter)

        if on_epoch is not None:
            epoch = FloatsamEpoch(n, max_drifter_order, c, threshold)
            on_epoch(epoch)

        if c is not None and c >= max_drifter_order:
            break

    return best_threshold
