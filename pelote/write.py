# =============================================================================
# Pelote Writing Functions
# =============================================================================
#
# Functions used to write to various data formats.
#
VALID_KEY_TYPES = (int, str)


def coerce_attributes(attr, allow_invalid_names=False):
    copy = {}

    for k, v in attr.items():
        if not isinstance(k, str):
            if allow_invalid_names:
                k = str(k)
            else:
                raise TypeError(
                    "some attributes contain non-string name: %s" % type(k).__name__
                )

        copy[k] = v

    return copy


def write_graphology_json(
    graph, allow_mixed_keys: bool = False, allow_invalid_attr_names: bool = False
):
    """
    Function serializing the given networkx graph as JSON, using the
    [graphology](https://graphology.github.io/) format.

    Note that both node keys and attribute names will be cast to string so
    they can safely be represented in JSON. As such in some cases (where
    your node keys and/or attribute names are not strings), this function
    will not be bijective when used with `read_graphology_json`.

    Args:
        graph (nx.AnyGraph): graph to serialize.
        allow_mixed_keys (bool, optional): whether to allow graph with mixed
            node key types to be serialized nonetheless. Keys will always be
            cast to string so keys might clash and produce an invalid
            serialization. Only use this if you know what you are doing.
            Defaults to False.
        allow_invalid_attr_names (bool, optional): whether to allow non-string
            attribute names. Note that if you chose to allow them, some might
            clash and produce an invalid serialization. Only use this if you
            know what you are doing.
            Defaults to False.

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
                "graph has node keys that cannot be represented in JSON, such as: %s. Use allow_mixed_keys=True if you know what you are doing."
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
            node_data["attributes"] = coerce_attributes(
                attr, allow_invalid_names=allow_invalid_attr_names
            )

        nodes.append(node_data)

    for source, target, attr in graph.edges.data():
        edge_data = {"source": str(source), "target": str(target)}

        if attr:
            edge_data["attributes"] = coerce_attributes(
                attr, allow_invalid_names=allow_invalid_attr_names
            )

        edges.append(edge_data)

    result = {"options": options, "nodes": nodes, "edges": edges}

    if attributes:
        result["attributes"] = attributes

    return result
