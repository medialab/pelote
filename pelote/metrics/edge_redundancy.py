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
):
    """
    Function computing the redundancy of each edge in the given graph. This
    score is typically used to extract the simmelian backbone of a graph.

    Args:
        graph(nx.AnyGraph): target graph.
        edge_weight_attr (str, optional): name of the edge attribute containing
            the measure to use to calculate redundancy.
            Defaults to "triangular_strength".

    Returns:
        dict: Dictionnary with edges - (source, target) tuples - as keys and the redundancy as values
    """
    check_graph(graph)

    if graph.is_multigraph():
        raise TypeError("edge_redundancy cannot work on a multi graph")

    redundancies = {}

    undirected_graph = graph
    if graph.is_directed():
        undirected_graph = graph.to_undirected(as_view=True)

    if edge_weight_attr == "triangular_strength":
        graph_edge_weight = triangular_strength(undirected_graph, full=True)
    else:
        graph_edge_weight = {}
        for u, v, w in graph.edges.data(edge_weight_attr):
            if u > v:
                u, v = v, u
            graph_edge_weight[(u, v)] = w
    neighbors_strong_edges_nodes = {}

    for node in graph.nodes:

        def get_neighbors_with_strong_edge(node):

            if edge_strength_ranking_threshold == 0:
                return set()

            if undirected_graph.degree[node] <= edge_strength_ranking_threshold:
                return set(nx.neighbors(undirected_graph, node))

            edges = []

            for u, v in nx.edges(undirected_graph, nbunch=node):
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

        neighbors_strong_edges_nodes[node] = get_neighbors_with_strong_edge(node)

    for u, v in graph.edges:
        redundancies[u, v] = fast_intersection_size(
            neighbors_strong_edges_nodes[u], neighbors_strong_edges_nodes[v]
        )

    return redundancies
