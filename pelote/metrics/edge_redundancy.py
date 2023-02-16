# =============================================================================
# Pelote Edge Redundancy Metric
# =============================================================================
#
import networkx as nx

from pelote.graph import check_graph
from pelote.metrics.chiba_nishizeki import triangular_strength
from pelote.utils import fast_intersection_size


def edge_redundancy(
    graph,
    edge_strength_ranking_threshold: int = 0,
    edge_weight_attr: str = "triangular_strength",
    in_or_out_edge_ranking: str = "both",
    in_or_out_edge_redundancy : str = "both",
    reciprocity: bool = False,
):
    """
    Function computing the redundancy of each edge in the given graph. This
    score is typically used to extract the simmelian backbone of a graph.

    Args:
        graph(nx.AnyGraph): target graph.
        edge_strength_ranking_threshold (int, optional): strength ranking threshold.
            Defaults to 1.
        edge_weight_attr (str, optional): name of the edge attribute holding
            the edge's weight. Defaults to "triangular_strength".
        in_or_out_edge_ranking (str, optional): whether to consider ingoing edges, or outgoing edges,
            or both. Defaults to both.
        in_or_out_edge_redundancy (str, optional): wether to consider ingoing edges, outgoing edges,
            both, or in_out, or out_in, in_out_and_out_in when checking redundancy. Will only be considered if
            in_or_out_edge_ranking is both. Defaults to both.
        reciprocity (bool, optional): wether reciprocity within top ranks is counted as overlap.
            Defaults to False.

    Returns:
        dict: Dictionnary with edges - (source, target) tuples - as keys and the redundancy as values
    """
    check_graph(graph)

    if graph.is_multigraph():
        raise TypeError("edge_redundancy cannot work on a multi graph")

    redundancies = {}

    undirected_graph = graph
    is_directed = graph.is_directed()
    if is_directed:
        undirected_graph = graph.to_undirected(as_view=True)

    if edge_weight_attr == "triangular_strength":
        graph_edge_weight = triangular_strength(undirected_graph, full=True)
    else:
        graph_edge_weight = {}
        for u, v, w in graph.edges.data(edge_weight_attr):
            if u > v:
                u, v = v, u
            graph_edge_weight[(u, v)] = w

    if in_or_out_edge_ranking!="both":
        in_or_out_edge_redundancy=in_or_out_edge_ranking

    if in_or_out_edge_redundancy=="in_out" or in_or_out_edge_redundancy=="out_in" or in_or_out_edge_redundancy=="in_out_and_out_in":
        neighbors_strong_edges_nodes_in = {}
        neighbors_strong_edges_nodes_out = {}

    else:
        neighbors_strong_edges_nodes = {}

    for node in graph.nodes:

        def get_neighbors_with_strong_edge(node, dict_in_or_out):

            if edge_strength_ranking_threshold == 0:
                return set()

            if (
                not is_directed or dict_in_or_out == "both"
            ) and undirected_graph.degree[node] <= edge_strength_ranking_threshold:
                return set(undirected_graph.neighbors(node))

            if is_directed:
                if (
                    dict_in_or_out == "out"
                    and graph.out_degree[node] <= edge_strength_ranking_threshold
                ):
                    return set(graph.successors(node))
                elif (
                    dict_in_or_out == "in"
                    and graph.in_degree[node] <= edge_strength_ranking_threshold
                ):
                    return set(graph.predecessors(node))

            edges = []

            if not is_directed or dict_in_or_out == "both":
                for u, v in nx.edges(undirected_graph, nbunch=node):
                    if u > v:
                        u, v = v, u
                    edges.append((u, v))
            elif is_directed:
                if dict_in_or_out == "out":
                    for u, v in graph.out_edges(node):
                        if u > v:
                            u, v = v, u
                        edges.append((u, v))
                elif dict_in_or_out == "in":
                    for u, v in graph.in_edges(node):
                        if u > v:
                            u, v = v, u
                        edges.append((u, v))

            edges_sorted_by_decreasing_weight = sorted(
                edges,
                key=lambda edge: graph_edge_weight[edge],
                reverse=True,
            )

            neighbors_strong_edge = set()
            l = edge_strength_ranking_threshold
            while (
                l < len(edges_sorted_by_decreasing_weight)
                and graph_edge_weight[edges_sorted_by_decreasing_weight[l - 1]]
                == graph_edge_weight[edges_sorted_by_decreasing_weight[l]]
            ):
                l += 1

            for edge in edges_sorted_by_decreasing_weight[:l]:
                neighbor = edge[0]
                if neighbor == node:
                    neighbor = edge[1]

                neighbors_strong_edge.add(neighbor)

            return neighbors_strong_edge

        if in_or_out_edge_redundancy=="in_out" or in_or_out_edge_redundancy== "out_in" or in_or_out_edge_redundancy=="in_out_and_out_in":
            neighbors_strong_edges_nodes_in[node] = get_neighbors_with_strong_edge(node, "in")
            neighbors_strong_edges_nodes_out[node] = get_neighbors_with_strong_edge(node, "out")
        else:
            neighbors_strong_edges_nodes[node] = get_neighbors_with_strong_edge(node, in_or_out_edge_redundancy)

    for u, v in graph.edges:
        if in_or_out_edge_redundancy!="in_out" and in_or_out_edge_redundancy!="out_in" and in_or_out_edge_redundancy!="in_out_and_out_in":
            redundancies[u, v] = fast_intersection_size(
                neighbors_strong_edges_nodes[u], neighbors_strong_edges_nodes[v]
            )
            if (
                reciprocity
                and u in neighbors_strong_edges_nodes[v]
                and v in neighbors_strong_edges_nodes[u]
            ):
                redundancies[u, v] += 1
        else:
            if in_or_out_edge_redundancy=="in_out":
                redundancies[u, v] = fast_intersection_size(
                    neighbors_strong_edges_nodes_in[u], neighbors_strong_edges_nodes_out[v]
                )
            elif in_or_out_edge_redundancy=="out_in":
                redundancies[u, v] = fast_intersection_size(
                    neighbors_strong_edges_nodes_out[u], neighbors_strong_edges_nodes_in[v]
                )
            else:
                redundancies[u, v] = fast_intersection_size(
                    neighbors_strong_edges_nodes_in[u], neighbors_strong_edges_nodes_out[v]
                )
                redundancies[u, v] += fast_intersection_size(
                    neighbors_strong_edges_nodes_out[u], neighbors_strong_edges_nodes_in[v]
                )
    print(redundancies)

    return redundancies
