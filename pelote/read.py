# =============================================================================
# Pelote Reading Functions
# =============================================================================
#
# Functions used to read from various data formats.
#
import networkx as nx

from pelote.types import GraphologySerializedGraph, AnyGraph


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
