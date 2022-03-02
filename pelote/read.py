# =============================================================================
# Pelote Reading Functions
# =============================================================================
#
# Functions used to read from various data formats.
#
import networkx as nx

from pelote.types import GraphologySerializedGraph, AnyGraph


def parse_graphology_json(data: GraphologySerializedGraph) -> "AnyGraph[str]":
    if "options" not in data:
        raise TypeError(
            "cannot parse a graphology json that does not record the graph options"
        )

    options = data["options"]
    assert options is not None  # Casting the value

    graph_type = options["type"]

    if graph_type == "mixed":
        raise TypeError("cannot parse a mixed graph yet")

    is_multi = options["multi"]

    g: AnyGraph[str]

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

    return g
