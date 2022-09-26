# =============================================================================
# Pelote Reading Functions
# =============================================================================
#
# Functions used to read from various data formats.
#
import json
import networkx as nx
from pathlib import Path
from io import IOBase


def parse_graphology_json(data):
    if "options" not in data:
        raise TypeError(
            "cannot parse a graphology json that does not record the graph options"
        )

    options = data["options"]
    graph_type = options["type"]

    graph_attributes = data.get("attributes", {})
    nodes = data.get("nodes")
    edges = data.get("edges")
    must_check_mixed = graph_type == "mixed"

    if must_check_mixed:
        if edges and edges[0].get("undirected", False):
            graph_type = "undirected"
        else:
            graph_type = "directed"

    is_multi = options["multi"]

    if graph_type == "directed":
        if is_multi:
            graph = nx.MultiDiGraph(**graph_attributes)
        else:
            graph = nx.DiGraph(**graph_attributes)
    else:
        if is_multi:
            graph = nx.MultiGraph(**graph_attributes)
        else:
            graph = nx.Graph(**graph_attributes)

    if nodes is not None:
        for serialized_node in nodes:
            attr = serialized_node.get("attributes", {})
            graph.add_node(serialized_node["key"], **attr)

    if edges is not None:
        for serialized_edge in edges:
            key = serialized_edge.get("key")
            attr = serialized_edge.get("attributes", {})
            source = serialized_edge["source"]
            target = serialized_edge["target"]

            if must_check_mixed:
                is_valid = serialized_edge.get("undirected", False) == (
                    graph_type == "undirected"
                )

                if not is_valid:
                    raise TypeError("cannot parse true mixed graphs")

            if key is not None and is_multi:
                graph.add_edge(source, target, key=key, **attr)
            else:
                graph.add_edge(source, target, **attr)

    return graph


def read_graphology_json(target):
    """
    Function reading and parsing the given json file representing a serialized
    [graphology](https://graphology.github.io/) graph as a networkx graph.

    Note that this function cannot parse a true mixed graph since this is not
    supported by networkx.

    Args:
        target (str or Path or file or dict): target to read and parse. Can
            be a string path, a Path instance, a file buffer or already
            parsed JSON data as a dict.

    Returns:
        nx.AnyGraph: a networkx graph instance.
    """
    if isinstance(target, (str, Path)):
        with open(target) as f:
            data = json.load(f)

    elif isinstance(target, IOBase):
        data = json.load(target)

    elif isinstance(target, dict):
        data = target

    else:
        raise TypeError("expected a path or a file")

    return parse_graphology_json(data)
