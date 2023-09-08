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

try:
    from llist import dllist
except ImportError:
    from pyllist import dllist

from pelote.utils import fast_intersection_size
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

        # NOTE: theoretically, using a linear time such as counting sort count speed
        # up the sorting step, but as it turns out, I cannot design a faster function
        # in python than the builtin `sorted` for this use case. Numpy does not
        # speed this up either.
        # NOTE: sorting is not necessary to produce a correct result but
        # minimizes the number of operations to perform by ensuring we
        # traverse the graph less. But it is quite tricky to assess whether
        # the induced O(n log n) or linear sort is worth it in most cases.
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

        # NOTE: last two nodes are not important because we already
        # iterated over every possible triangle when we reach them
        for i in range(0, len(sorted_nodes) - 2):
            node = sorted_nodes[i]

            for neighbor in adjacencies[node]:
                marked_nodes[neighbor] = True

            while len(marked_nodes) != 0:
                neighbor, _ = marked_nodes.popitem()
                neighbor_adjacency = adjacencies[neighbor]

                self_dllist_node = None

                for dllist_node in neighbor_adjacency.iternodes():
                    neighbor_of_neighbor = dllist_node.value

                    if neighbor_of_neighbor == node:
                        self_dllist_node = dllist_node
                        continue

                    if neighbor_of_neighbor in marked_nodes:
                        yield (node, neighbor, neighbor_of_neighbor)

                # NOTE: Handling deletion of current node in the graph. We only
                # need to delete it from the neighbor's side, because we will
                # never iterate over current node later on.
                # NOTE: we remove the dllist_node here because removing it
                # from the loop can cause the iteration to skip some items,
                # at least in this implementation of dllist.
                neighbor_adjacency.remove(self_dllist_node)

    return generator()


def naive_triangular_strength(graph, full=False):
    """
    Naive algorithm to compute edge triangular strength. We keep it mostly to
    benchmark against the Chiba-Nishizeki method.

    Arguments:
        graph (nx.AnyGraph): target graph.
        full (bool, optional): whether to return strength for every edge,
            including those with strength = 0. Defaults to False.

    Returns:
        dict: mapping of edges to their triangular strength.
    """
    check_graph(graph)

    if graph.is_directed():
        graph = graph.to_undirected(as_view=True)

    neighborhoods = {}

    for node in graph:
        neighborhood = set()

        for neighbor in graph.neighbors(node):
            if node == neighbor:
                continue

            neighborhood.add(neighbor)

        if len(neighborhood) > 1:
            neighborhoods[node] = neighborhood

    strengths = {}

    for u, v in graph.edges():
        if u > v:
            u, v = v, u

        n1 = neighborhoods.get(u)
        n2 = neighborhoods.get(v)

        if n1 is None or n2 is None:
            if full:
                strengths[u, v] = 0

            continue

        strengths[u, v] = fast_intersection_size(n1, n2)

    return strengths


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
        if u < v:
            strengths[u, v] += 1
        else:
            strengths[v, u] += 1

        if u < w:
            strengths[u, w] += 1
        else:
            strengths[w, u] += 1

        if v < w:
            strengths[v, w] += 1
        else:
            strengths[w, v] += 1

    return strengths
