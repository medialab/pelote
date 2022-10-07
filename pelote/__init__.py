# =============================================================================
# Pelote Library Endpoint
# =============================================================================
#
from pelote.graph import (
    union_of_maximum_spanning_trees,
    largest_connected_component,
    crop_to_largest_connected_component,
    largest_connected_component_subgraph,
    remove_edges,
    filter_edges,
    remove_nodes,
    filter_nodes,
    remove_leaves,
    filter_leaves,
)
from pelote.graph_to_tabular import (
    graph_to_nodes_dataframe,
    graph_to_edges_dataframe,
    graph_to_dataframes,
)
from pelote.learn import floatsam_threshold_learner
from pelote.metrics import edge_disparity, triangular_strength
from pelote.projection import monopartite_projection
from pelote.read import read_graphology_json
from pelote.write import write_graphology_json
from pelote.sparsification import (
    global_threshold_sparsification,
    GlobalThresholdSparsifier,
    multiscale_backbone,
    MultiscaleBackboneSparsifier,
)
from pelote.tabular_to_graph import (
    table_to_bipartite_graph,
    tables_to_graph,
    edges_table_to_graph,
)

__all__ = [
    "union_of_maximum_spanning_trees",
    "largest_connected_component",
    "crop_to_largest_connected_component",
    "largest_connected_component_subgraph",
    "remove_edges",
    "filter_edges",
    "remove_nodes",
    "filter_nodes",
    "remove_leaves",
    "filter_leaves",
    "graph_to_nodes_dataframe",
    "graph_to_edges_dataframe",
    "graph_to_dataframes",
    "floatsam_threshold_learner",
    "edge_disparity",
    "triangular_strength",
    "monopartite_projection",
    "read_graphology_json",
    "global_threshold_sparsification",
    "GlobalThresholdSparsifier",
    "multiscale_backbone",
    "MultiscaleBackboneSparsifier",
    "table_to_bipartite_graph",
    "tables_to_graph",
    "edges_table_to_graph",
]

__toc__ = [
    {
        "title": "Tabular data to graphs",
        "fns": [
            table_to_bipartite_graph,
            tables_to_graph,
            edges_table_to_graph,
        ],
    },
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
    {
        "title": "Miscellaneous graph-related metrics",
        "fns": [edge_disparity, triangular_strength],
    },
    {
        "title": "Graph utilities",
        "fns": [
            union_of_maximum_spanning_trees,
            largest_connected_component,
            crop_to_largest_connected_component,
            largest_connected_component_subgraph,
            remove_edges,
            filter_edges,
            remove_nodes,
            filter_nodes,
            remove_leaves,
            filter_leaves,
        ],
    },
    {"title": "Learning", "fns": [floatsam_threshold_learner]},
    {
        "title": "Reading & Writing",
        "fns": [read_graphology_json, write_graphology_json],
    },
]
