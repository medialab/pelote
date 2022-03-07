from pelote.network_to_tabular import (
    to_nodes_dataframe,
    to_edges_dataframe,
    to_dataframes,
)
from pelote.graph import (
    largest_connected_component,
    crop_to_largest_connected_components,
    remove_edges,
)
from pelote.projection import monopartite_projection
from pelote.read import read_graphology_json
from pelote.tabular_to_network import to_bipartite_graph

from pelote.metrics import edge_disparity

DOCS = [
    {"title": "Tabular to network", "fns": [to_bipartite_graph]},
    {
        "title": "Network to tabular",
        "fns": [to_nodes_dataframe, to_edges_dataframe, to_dataframes],
    },
    {"title": "Graph projection", "fns": [monopartite_projection]},
    {
        "title": "Graph utilities",
        "fns": [
            largest_connected_component,
            crop_to_largest_connected_components,
            remove_edges,
        ],
    },
    {"title": "Reading & Writing", "fns": [read_graphology_json]},
    {"title": "Metrics", "fns": [edge_disparity]},
]

__all__ = ["DOCS"]
