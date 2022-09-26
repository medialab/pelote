# =============================================================================
# Pelote Writing Functions
# =============================================================================
#
# Functions used to write to various data formats.
#
VALID_KEY_TYPES = (int, str)


def write_graphology_json(graph, allow_mixed_keys: bool = False):
    """
    Function serializing the given networkx graph as JSON, using the
    [graphology](https://graphology.github.io/) format.

    Note that both node keys and attribute names will be cast to string so
    they can safely be represented in JSON.

    Args:
        graph (nx.AnyGraph): graph to serialize.
        allow_mixed_keys (bool, optional): whether to allow graph with mixed
            node key types to be serialized nonetheless. Keys will always be
            cast to string so keys might clash and produce an invalid
            serialization. Only use this if you know what you are doing.

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

    node_key_type = None

    for n, attr in graph.nodes.data():
        if not isinstance(n, VALID_KEY_TYPES):
            raise TypeError(
                "graph has node keys that cannot be represented in JSON, such as: %s"
                % type(n).__name__
            )

        if not allow_mixed_keys:
            if node_key_type is None:
                node_key_type = type(n)
            elif type(n) is not node_key_type:
                raise TypeError(
                    "graph has mixed node keys: %s and %s"
                    % (type(n).__name__, node_key_type.__name__)
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
