# =============================================================================
# Pelote Chiba-Nishizeki Routines
# =============================================================================
#
# Implementations of routines found in the Chiba-Nishizeki paper, related
# to triangle and quadrangle enumeration.
#
# http://www.ecei.tohoku.ac.jp/alg/nishizeki/sub/j/DVD/PDF_J/J053.pdf
#
from collections import OrderedDict
from llist import dllist


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
    if graph.is_directed():
        graph = graph.to_undirected(as_view=True)

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
