# =============================================================================
# Pelote Simmelian Backbone Sparsification Unit Tests
# =============================================================================
from cmath import exp
import networkx as nx

from pelote.graph import are_same_graphs
from pelote.sparsification.simmelian_backbone import (
    simmelian_backbone,
    SimmelianBackboneSparsifier,
)


class TestSimmelianBackboneSparsifier(object):
    def test_basics(self):
        graph = nx.Graph()

        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 1)
        graph.add_edge(4, 2)
        graph.add_edge(4, 3)

        sparse = simmelian_backbone(
            graph, edge_strength_ranking_threshold=1, edge_redundancy_threshold=1
        )

        expected = nx.Graph()
        expected.add_node(0)
        expected.add_edge(1, 2)
        expected.add_edge(3, 1)
        expected.add_edge(2, 4)
        expected.add_edge(3, 4)

        assert are_same_graphs(sparse, expected, check_attributes=True)

    def test_digraph(self):
        graph = nx.DiGraph()

        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 1)
        graph.add_edge(4, 2)
        graph.add_edge(4, 3)

        sparse = simmelian_backbone(
            graph, edge_strength_ranking_threshold=1, edge_redundancy_threshold=1
        )

        expected = nx.DiGraph()
        expected.add_node(0)
        expected.add_edge(1, 2)
        expected.add_edge(3, 1)
        expected.add_edge(4, 2)
        expected.add_edge(4, 3)

        assert are_same_graphs(sparse, expected, check_attributes=True)

    def test_weight(self):
        graph = nx.Graph()

        graph.add_edge(0, 1, weight=3)
        graph.add_edge(1, 2, weight=2)
        graph.add_edge(2, 3, weight=1)
        graph.add_edge(3, 1, weight=2)
        graph.add_edge(4, 2, weight=3)
        graph.add_edge(4, 3, weight=3)

        sparse = simmelian_backbone(
            graph,
            edge_strength_ranking_threshold=1,
            edge_redundancy_threshold=1,
            edge_weight_attr="weight",
        )

        expected = nx.Graph()
        expected.add_nodes_from(range(5))
        expected.add_edge(3, 2, weight=1)

        assert are_same_graphs(sparse, expected, check_attributes=True)

    def test_weight_directed(self):
        graph = nx.DiGraph()

        graph.add_edge(0, 1, weight=3)
        graph.add_edge(1, 2, weight=2)
        graph.add_edge(2, 3, weight=1)
        graph.add_edge(3, 1, weight=2)
        graph.add_edge(4, 2, weight=3)
        graph.add_edge(4, 3, weight=3)

        sparse = simmelian_backbone(
            graph,
            edge_strength_ranking_threshold=1,
            edge_redundancy_threshold=1,
            edge_weight_attr="weight",
        )

        expected = nx.DiGraph()
        expected.add_nodes_from(range(5))
        expected.add_edge(2, 3, weight=1)

        assert are_same_graphs(sparse, expected, check_attributes=True)

    def test_filter(self):
        graph = nx.Graph()
        graph.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5), (1, 3, 5)])

        sparsifier = SimmelianBackboneSparsifier(1, 1, edge_weight_attr="weight")

        sparse = sparsifier(graph)

        expected = nx.Graph()
        expected.add_nodes_from(range(4))
        expected.add_weighted_edges_from([(2, 3, 5)])

        assert are_same_graphs(sparse, expected, check_attributes=True)
        assert are_same_graphs(
            sparsifier.filter(graph), expected, check_attributes=True
        )

    def test_remove(self):
        graph = nx.Graph()
        graph.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5), (1, 3, 5)])

        sparsifier = SimmelianBackboneSparsifier(1, 1, edge_weight_attr="weight")

        sparsifier.remove(graph)

        expected = nx.Graph()
        expected.add_nodes_from(range(4))
        expected.add_weighted_edges_from([(2, 3, 5)])

        assert are_same_graphs(graph, expected, check_attributes=True)

    def test_relevant_edges(self):
        graph = nx.Graph()
        graph.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5), (1, 3, 5)])

        sparsifier = SimmelianBackboneSparsifier(1, 1, edge_weight_attr="weight")

        assert list(sparsifier.relevant_edges(graph)) == [(2, 3, {"weight": 5})]

    def test_redundant_edges(self):
        graph = nx.Graph()
        graph.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5), (1, 3, 5)])

        sparsifier = SimmelianBackboneSparsifier(1, 1, edge_weight_attr="weight")

        assert list(sparsifier.redundant_edges(graph)) == [
            (0, 1, {"weight": 10}),
            (1, 2, {"weight": 5}),
            (1, 3, {"weight": 5}),
        ]

    def test_flag_relevant_edges(self):
        graph = nx.Graph()
        graph.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5), (1, 3, 5)])

        sparsifier = SimmelianBackboneSparsifier(1, 1, edge_weight_attr="weight")

        sparsifier.flag_relevant_edges(graph)

        assert list(graph.edges.data()) == [
            (0, 1, {"weight": 10}),
            (1, 2, {"weight": 5}),
            (1, 3, {"weight": 5}),
            (2, 3, {"weight": 5, "relevant": True}),
        ]

        sparsifier.flag_relevant_edges(graph, full=True)

        assert list(graph.edges.data()) == [
            (0, 1, {"weight": 10, "relevant": False}),
            (1, 2, {"weight": 5, "relevant": False}),
            (1, 3, {"weight": 5, "relevant": False}),
            (2, 3, {"weight": 5, "relevant": True}),
        ]

    def test_flag_redundant_edges(self):
        graph = nx.Graph()
        graph.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5), (1, 3, 5)])

        sparsifier = SimmelianBackboneSparsifier(1, 1, edge_weight_attr="weight")

        sparsifier.flag_redundant_edges(graph)

        assert list(graph.edges.data()) == [
            (0, 1, {"weight": 10, "redundant": True}),
            (1, 2, {"weight": 5, "redundant": True}),
            (1, 3, {"weight": 5, "redundant": True}),
            (2, 3, {"weight": 5}),
        ]

        sparsifier.flag_redundant_edges(graph, full=True)

        assert list(graph.edges.data()) == [
            (0, 1, {"weight": 10, "redundant": True}),
            (1, 2, {"weight": 5, "redundant": True}),
            (1, 3, {"weight": 5, "redundant": True}),
            (2, 3, {"weight": 5, "redundant": False}),
        ]

    def test_keep_connected(self):
        graph = nx.Graph()
        graph.add_edge(0, 1, weight=5)

        sparsifier = SimmelianBackboneSparsifier(
            0, 1, edge_weight_attr="weight", keep_connected=True
        )

        sparse = sparsifier(graph)

        assert list(sparse.edges) == [(0, 1)]
        assert list(sparsifier.relevant_edges(graph)) == [(0, 1, {"weight": 5})]
        assert list(sparsifier.redundant_edges(graph)) == []
