from pelote.graph_to_tabular import (
    graph_to_nodes_dataframe,
    graph_to_edges_dataframe,
    graph_to_dataframes,
)
from pelote.graph import (
    largest_connected_component,
    crop_to_largest_connected_component,
    remove_edges,
    filter_edges,
)
from pelote.learn import floatsam_threshold_learner
from pelote.metrics import edge_disparity
from pelote.projection import monopartite_projection
from pelote.read import read_graphology_json
from pelote.sparsification import global_threshold_sparsification, multiscale_backbone
from pelote.tabular_to_graph import table_to_bipartite_graph

DOCS = [
    {"title": "Tabular data to graphs", "fns": [table_to_bipartite_graph]},
    {
        "title": "Graphs to tabular data",
        "fns": [
            graph_to_nodes_dataframe,
            graph_to_edges_dataframe,
            graph_to_dataframes,
        ],
    },
    {"title": "Graph projection", "fns": [monopartite_projection]},
    {
        "title": "Graph sparsification",
        "fns": [global_threshold_sparsification, multiscale_backbone],
    },
    {"title": "Miscellaneous graph-related metrics", "fns": [edge_disparity]},
    {
        "title": "Graph utilities",
        "fns": [
            largest_connected_component,
            crop_to_largest_connected_component,
            remove_edges,
            filter_edges,
        ],
    },
    {"title": "Learning", "fns": [floatsam_threshold_learner]},
    {"title": "Reading & Writing", "fns": [read_graphology_json]},
]

__all__ = ["DOCS"]
