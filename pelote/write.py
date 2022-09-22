# =============================================================================
# Pelote Writing Functions
# =============================================================================
#
# Functions used to write to various data formats.
#

import networkx as nx


def write_graphology_json(graph):

    attr_nodes = {}
    attr_edges = {}
    edges = []
    nodes = []
    total = {}
    if nx.number_of_selfloops(graph):
        allowSelfLoops = False
    else:
        allowSelfLoops = True
    attributes = graph.graph
    if type(graph) == nx.classes.graph.Graph:  # graphe non dirigé, simple
        multi = False
        type_options = "undirected"
    elif type(graph) == nx.classes.digraph.DiGraph:  # graphe dirigé, simple
        multi = False
        type_options = "directed"
    elif type(graph) == nx.classes.multigraph.MultiGraph:  # non dirigé multi
        multi = True
        type_options = "undirected"
    else:  # nx.classes.multidigraph.MultiDiGraph, dirigé, multi
        multi = True
        type_options = "directed"
    options = {"allowSelfLoops": allowSelfLoops, "multi": multi, "type": type_options}
    for n, attr in graph.nodes.data():
        if attr:
            for i, g in attr.items():
                attr_nodes[n] = {str(i): g}
        else:
            attr_nodes[n] = attr
    for e, attr in graph.edges.items():
        if attr:
            for i, g in attr.items():
                attr_edges[e] = {str(i): g}
        else:
            attr_edges[e] = attr
    for key, edge in attr_edges.items():
        if edge:
            edges.append(
                {
                    "source": str(list(key)[0]),
                    "target": str(list(key)[1]),
                    "attributes": edge,
                }
            )
        else:
            edges.append({"source": str(list(key)[0]), "target": str(list(key)[1])})
    for key, node in attr_nodes.items():
        if node:
            nodes.append({"key": str(key), "attributes": node})
        else:
            nodes.append({"key": str(key)})
    if attributes:
        total["attributes"] = attributes
    total["options"] = options
    total["nodes"] = nodes
    total["edges"] = edges
    return total
