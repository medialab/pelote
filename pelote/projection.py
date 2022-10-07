# =============================================================================
# Pelote Network Projection Functions
# =============================================================================
#
# Functions used to compute various networkx projections such as bipartite
# to monopartite, for instance.
#
import networkx as nx
from collections import defaultdict
from collections.abc import Hashable
from ebbe import omit

from pelote.classes import BFSQueue
from pelote.classes.online_metrics import instantiate_online_metric
from pelote.graph import check_graph
from pelote.utils import has_constant_time_lookup


def monopartite_projection(
    bipartite_graph,
    part_to_keep,
    *,
    node_part_attr: str = "part",
    edge_weight_attr: str = "weight",
    metric=None,
    bipartition_check: bool = True,
    weight_threshold=None
):
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
        metric (str, optional): one of "jaccard", "overlap", "cosine", "dice",
            "binary_cosine", "pmi" or "dot_product". If not given, resulting weight
            will be set to the size of neighbor intersection. Defaults to None.
        bipartition_check (bool, optional): whether to check if given graph
            is truly bipartite. You can disable this as an optimization
            strategy if you know what you are doing. Defaults to True.
        weight_threshold (float, optional): if an edge weight should be less
            than this threshold we would not add it to the projected
            monopartite graph. Defaults to None.

    Returns:
        nx.Graph: the projected monopartite graph.
    """
    # TODO: raise if multigraph
    check_graph(bipartite_graph)

    online_metric = instantiate_online_metric(metric)

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
            part_to_keep = set(part_to_keep)

    # Computing norms
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
        online_metric.reset_norm()

        for token, ta in bipartite_graph[n1].items():
            if bipartition_check:
                if (part_to_keep_as_set and token in part_to_keep) or ta.get(  # type: ignore
                    node_part_attr
                ) == part_to_keep:
                    raise TypeError(
                        'given graph is not truly bipartite because of an edge between two nodes of the same part: "%s" and "%s"'
                        % (n1, token)
                    )

            weight = ta.get(edge_weight_attr, 1)
            online_metric.accumulate_norm(weight)

        online_metric.add_norm(n1)
        monopartite_graph.add_node(n1, **omit(a1, [node_part_attr]))

    if part_is_empty:
        raise TypeError(
            '"%s" part does not exist in given graph. Are you sure your nodes have a "%s" attribute?'
            % (part_to_keep, node_part_attr)
        )

    online_metric.finalize()

    for n1 in online_metric.nodes():
        online_metric.start_intersection(n1)

        # Computing intersections
        for token, ta in bipartite_graph[n1].items():
            w1 = ta.get(edge_weight_attr, 1)

            for n2, a2 in bipartite_graph[token].items():

                # Don't compare to self
                if n2 == n1:
                    continue

                # NOTE: since we are producing an undirected graphs we can
                # avoid doing the same computations twice.
                # NOTE: we could also drop n1 from the graph after we processed
                # it as this would have the same effect. But this is often less
                # performant because the graph must be copied to avoid
                # mutation and dropping a node is at least O(E), E being the
                # number of its incident edges.
                elif n1 > n2:
                    continue

                w2 = a2.get(edge_weight_attr, 1)
                online_metric.intersect(n2, w1, w2)

        # Finalizing metrics
        for n2, similarity in online_metric.neighbors():

            if weight_threshold is not None and similarity < weight_threshold:
                continue

            monopartite_graph.add_edge(n1, n2, weight=similarity)

    return monopartite_graph


def bfs_from_node(graph, source, reverse=False, limit=1):
    queue = BFSQueue(graph)
    queue.append(source, (source, 0))

    while len(queue) != 0:
        node, depth = queue.popleft()

        if depth > 0:
            yield node, depth

        if depth >= limit:
            continue

        for neighbor in (graph.predecessors if reverse else graph.successors)(node):
            queue.append(neighbor, (neighbor, depth + 1))


def self_similarity_projection(graph, depth=1):
    # TODO: raise if multigraph
    check_graph(graph)

    # NOTE: only Jaccard & only directed version currently implemented

    if not graph.is_directed():
        raise NotImplementedError

    # Null graph early exit
    if graph.order() == 0:
        return nx.Graph()

    projected_graph = nx.Graph()

    norms = {}
    inverted_index = defaultdict(list)

    for node, attr in graph.nodes.data():
        projected_graph.add_node(node, **attr)

        norm = 0
        candidates = defaultdict(int)

        # TODO: plug BFS strategy here
        # TODO: directed BFS can only follow one kind of links, supposedly?
        for out_neighbor, depth in bfs_from_node(graph, node, limit=depth):
            norm += 1
            k = (True, depth, out_neighbor)
            container = inverted_index[k]

            for candidate in container:
                candidates[candidate] += 1

            container.append(node)

        for in_neighbor, depth in bfs_from_node(graph, node, reverse=True, limit=depth):
            norm += 1
            k = (False, depth, in_neighbor)
            container = inverted_index[k]

            for candidate in container:
                candidates[candidate] += 1

            container.append(node)

        norms[node] = norm

        for candidate, intersection in candidates.items():
            candidate_norm = norms[candidate]

            # NOTE: We don't consider the edges between node & candidate in
            # the similarity score.
            # TODO: Verify that the bipartite projection conceptual parallelism
            # still holds.
            # NOTE: Decrementing the candidate's norm twice is equivalent
            # to decrementing both the candidate norm and node's one (only
            # for Jaccard, will not work for Dice and overlap).
            if graph.has_edge(node, candidate):
                candidate_norm -= 2

            if graph.has_edge(candidate, node):
                candidate_norm -= 2

            similarity = intersection / (norm + candidate_norm - intersection)

            projected_graph.add_edge(node, candidate, weight=similarity)

    return projected_graph
