from pelote.graph_to_tabular import (
    to_nodes_dataframe,
    to_edges_dataframe,
    to_dataframes,
)
from pelote.graph import (
    largest_connected_component,
    crop_to_largest_connected_components,
    remove_edges,
    filter_edges,
    connected_component_sizes,
)
from pelote.projection import monopartite_projection
from pelote.read import read_graphology_json
from pelote.tabular_to_graph import to_bipartite_graph

from pelote.metrics import edge_disparity

DOCS = [
    {"title": "Tabular data to graphs", "fns": [to_bipartite_graph]},
    {
        "title": "Graphs to tabular data",
        "fns": [to_nodes_dataframe, to_edges_dataframe, to_dataframes],
    },
    {"title": "Graph projection", "fns": [monopartite_projection]},
    {"title": "Metrics", "fns": [edge_disparity]},
    {
        "title": "Graph utilities",
        "fns": [
            largest_connected_component,
            crop_to_largest_connected_components,
            remove_edges,
            filter_edges,
            connected_component_sizes,
        ],
    },
    {"title": "Reading & Writing", "fns": [read_graphology_json]},
]

__all__ = ["DOCS"]
