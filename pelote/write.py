# =============================================================================
# Pelote Writing Functions
# =============================================================================
#
# Functions used to write to various data formats.
#

import networkx as nx

VALID_KEY_TYPES = (int, str)


def write_graphology_json(graph):
    """
    Function serializing the given networkx graph as JSON, using the
    [graphology](https://graphology.github.io/) format.

    Args:
        graph (nx.AnyGraph): graph to serialize.

    Returns:
        dict: JSON data

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
        if not isinstance(n, VALID_KEY_TYPES):
            raise TypeError(
                "graph has node keys that cannot be represented in JSON, such as: %s"
                % type(n).__name__
            )

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
        result["attributes"] = attributes

    return result
