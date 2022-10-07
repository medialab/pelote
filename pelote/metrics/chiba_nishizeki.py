# =============================================================================
# Pelote Chiba-Nishizeki Routines
# =============================================================================
#
# Implementations of routines found in the Chiba-Nishizeki paper, related
# to triangle and quadrangle enumeration.
#
# http://www.ecei.tohoku.ac.jp/alg/nishizeki/sub/j/DVD/PDF_J/J053.pdf
#
from collections import OrderedDict, Counter
from llist import dllist

from pelote.graph import check_graph


def triangles(graph):
    """
    Function using "procedure K3" from the Chiba-Nishizeki paper to iterate
    over all of a graph's triangles.

    Article:
        Chiba, Norishige, and Takao Nishizeki. “Arboricity and Subgraph Listing
        Algorithms.” SIAM Journal on Computing, vol. 14, no. 1, Feb. 1985,
        pp. 210-23. DOI.org (Crossref), https://doi.org/10.1137/0214017.

    References:
        paper: http://www.ecei.tohoku.ac.jp/alg/nishizeki/sub/j/DVD/PDF_J/J053.pdf

    Arguments:
        graph (nx.AnyGraph): target graph.

    Yields:
        3-tuple: a triangle as a 3 nodes tuple.
    """
    check_graph(graph)

    if graph.is_directed():
        graph = graph.to_undirected(as_view=True)

    def generator():
        marked_nodes = OrderedDict()

        # NOTE: a node connected to a single other one cannot be part of a triangle
        valid_nodes = (n for n in graph if graph.degree[n] > 1)

        # NOTE: this sort can be done in linear time using e.g. bucket sort if required
        sorted_nodes = sorted(valid_nodes, key=graph.degree, reverse=True)

        adjacencies = {}

        for node in sorted_nodes:
            adjacency = dllist()

            for neighbor in graph.neighbors(node):

                # NOTE: avoiding self loops
                if neighbor == node:
                    continue

                # NOTE: avoiding leaf nodes
                if graph.degree[neighbor] < 2:
                    continue

                adjacency.append(neighbor)

            adjacencies[node] = adjacency

        for node in sorted_nodes:
            for neighbor in adjacencies[node]:
                marked_nodes[neighbor] = True

            while len(marked_nodes) != 0:
                neighbor, _ = marked_nodes.popitem()
                neighbor_adjacency = adjacencies[neighbor]

                for dllist_node in neighbor_adjacency.iternodes():
                    neighbor_of_neighbor = dllist_node.value

                    # NOTE: Handling deletion of current node in the graph
                    if neighbor_of_neighbor == node:
                        neighbor_adjacency.remove(dllist_node)
                        continue

                    if neighbor_of_neighbor in marked_nodes:
                        yield (node, neighbor, neighbor_of_neighbor)

    return generator()


def triangular_strength(graph, full: bool = False):
    """
    Function returning a graph edges triangular strength, sometimes also called
    Simmelian strength, i.e. the number of triangles each edge is a part of.

    Arguments:
        graph (nx.AnyGraph): target graph.
        full (bool, optional): whether to return strength for every edge,
            including those with strength = 0. Defaults to False.

    Returns:
        dict: mapping of edges to their triangular strength.
    """
    strengths = Counter()

    if full:
        for u, v in graph.edges():
            if u > v:
                u, v = v, u

            strengths[u, v] = 0

    for u, v, w in triangles(graph):

        # First edge
        if u < v:
            strengths[u, v] += 1
        else:
            strengths[v, u] += 1

        # Second edge
        if v < w:
            strengths[v, w] += 1
        else:
            strengths[w, v] += 1

        # Third edge
        if w < u:
            strengths[w, u] += 1
        else:
            strengths[u, w] += 1

    return strengths
