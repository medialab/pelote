# =============================================================================
# Pelote Writing Functions
# =============================================================================
#
# Functions used to write to various data formats.
#

import networkx as nx


def write_graphology_json(graph):
    """
    Function writing a json file representing a serialized
    [graphology](https://graphology.github.io/) graph corresponding to the given networkx graph.

    Args:
        graph (nx.AnyGraph): graph to be represented as serialized
    [graphology](https://graphology.github.io/) graph in json file.

    Returns:
        dict: parsed JSON data.
    """
    edges = []
    nodes = []
    attributes = graph.graph.copy()
    options = {
        "allowSelfLoops": True,
        "multi": graph.is_multigraph(),
        "type": "directed" if graph.is_directed() else "undirected",
    }
    for n, attr in graph.nodes.data():
        node_data = {"key": str(n)}

        if attr:
            node_data["attributes"] = {str(k): v for k, v in attr.items()}

        nodes.append(node_data)

    for source, target, attr in graph.edges.data():
        edge_data = {"source": str(source), "target": str(target)}

        if attr:
            edge_data["attributes"] = {str(k): v for k, v in attr.items()}

        edges.append(edge_data)
    result = {"options": options, "nodes": nodes, "edges": edges}
    if attributes:
        return result.update({"attributes": attributes})
    return result
