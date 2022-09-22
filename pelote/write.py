# =============================================================================
# Pelote Writing Functions
# =============================================================================
#
# Functions used to write to various data formats.
#

import networkx as nx


def write_graphology_json(graph):
    """
    Function reading and parsing the given a networkx graph as a json file representing a serialized
    [graphology](https://graphology.github.io/) graph.

    Args:
        graph (nx.AnyGraph): graph to read and parse.

    Returns:
        dict: dict with the graph represented in the structure of a json file representing a serialized
    [graphology] graph.
    """
    edges = []
    nodes = []
    attributes = graph.graph
    if nx.is_directed(graph):
        type_options = "directed"
    else:
        type_options = "undirected"
    if graph.is_multigraph():
        multi = True
    else:
        multi = False
    options = {"allowSelfLoops": True, "multi": multi, "type": type_options}
    for n, attr in graph.nodes.data():
        if attr:
            for i, g in attr.items():
                nodes.append({"key": str(n), "attributes": {str(i): g}})
        else:
            nodes.append({"key": str(n)})
    for source, target, attr in graph.edges.data():
        if attr:
            for i, g in attr.items():
                edges.append(
                    {
                        "source": str(source),
                        "target": str(target),
                        "attributes": {str(i): g},
                    }
                )
        else:
            edges.append({"source": str(source), "target": str(target)})
    if attributes:
        return {
            "attributes": attributes,
            "options": options,
            "nodes": nodes,
            "edges": edges,
        }
    return {"options": options, "nodes": nodes, "edges": edges}
