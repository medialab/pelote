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
from typing import Union

from pelote.types import GraphologySerializedGraph, AnyGraph, FileHandle


def parse_graphology_json(data: GraphologySerializedGraph) -> AnyGraph:
    if "options" not in data:
        raise TypeError(
            "cannot parse a graphology json that does not record the graph options"
        )

    options = data["options"]
    graph_type = options["type"]

    if graph_type == "mixed":
        raise TypeError("cannot parse a mixed graph yet")

    is_multi = options["multi"]

    g: AnyGraph

    if graph_type == "directed":
        if is_multi:
            g = nx.MultiDiGraph()
        else:
            g = nx.DiGraph()
    else:
        if is_multi:
            g = nx.MultiGraph()
        else:
            g = nx.Graph()

    nodes = data.get("nodes")

    if nodes is not None:
        for serialized_node in nodes:
            attr = serialized_node.get("attributes", {})
            g.add_node(serialized_node["key"], **attr)

    edges = data.get("edges")

    if edges is not None:
        for serialized_edge in edges:
            key = serialized_edge.get("key")
            attr = serialized_edge.get("attributes", {})
            source = serialized_edge["source"]
            target = serialized_edge["target"]

            if key is not None and is_multi:
                g.add_edge(source, target, key=key, **attr)
            else:
                g.add_edge(source, target, **attr)

    return g


def read_graphology_json(
    target: Union[FileHandle, GraphologySerializedGraph]
) -> AnyGraph:
    """
    Function reading and parsing the given json file as a networkx graph.

    Args:
        target (str or Path or file or dict): target to read and parse. Can
            be a string path, a Path instance, a file buffer or already
            parsed JSON data as a dict.

    Returns:
        nx.AnyGraph: a networkx graph instance.
    """
    data: GraphologySerializedGraph

    if isinstance(target, (str, Path)):
        with open(target) as f:
            data = json.load(f)

    elif isinstance(target, IOBase):
        data = json.load(target)

    elif isinstance(target, dict):
        data = target

    else:
        raise TypeError("expecting a path or a file")

    return parse_graphology_json(data)
