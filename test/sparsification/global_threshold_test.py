# =============================================================================
# Pelote Global Threshold Sparsification Unit Tests
# =============================================================================
import networkx as nx

from pelote.graph import are_same_graphs
from pelote.sparsification.global_threshold import (
    GlobalThresholdSparsifier,
    global_threshold_sparsification,
)


class TestGlobalThresholdSparsifier(object):
    def test_basics(self):
        dense = nx.Graph()
        dense.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5)])

        sparse = global_threshold_sparsification(dense, 10)

        expected = nx.Graph()
        expected.add_nodes_from(range(4))
        expected.add_edge(0, 1, weight=10)

        assert are_same_graphs(sparse, expected, check_attributes=True)

    def test_reverse(self):
        dense = nx.Graph()
        dense.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5)])

        sparse = global_threshold_sparsification(dense, 9, reverse=True)

        expected = nx.Graph()
        expected.add_nodes_from(range(4))
        expected.add_edge(1, 2, weight=5)
        expected.add_edge(2, 3, weight=5)

        assert are_same_graphs(sparse, expected, check_attributes=True)

    def test_filter(self):
        dense = nx.Graph()
        dense.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5)])

        sparsifier = GlobalThresholdSparsifier(10)

        sparse = sparsifier(dense)

        expected = nx.Graph()
        expected.add_nodes_from(range(4))
        expected.add_edge(0, 1, weight=10)

        assert are_same_graphs(sparse, expected, check_attributes=True)
        assert are_same_graphs(
            sparsifier.filter(dense), expected, check_attributes=True
        )

    def test_remove(self):
        dense = nx.Graph()
        dense.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5)])

        sparsifier = GlobalThresholdSparsifier(10)

        sparsifier.remove(dense)

        expected = nx.Graph()
        expected.add_nodes_from(range(4))
        expected.add_edge(0, 1, weight=10)

        assert are_same_graphs(dense, expected, check_attributes=True)

    def test_relevant_edges(self):
        dense = nx.Graph()
        dense.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5)])

        sparsifier = GlobalThresholdSparsifier(10)

        assert list(sparsifier.relevant_edges(dense)) == [(0, 1, {"weight": 10})]

    def test_redundant_edges(self):
        dense = nx.Graph()
        dense.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5)])

        sparsifier = GlobalThresholdSparsifier(10)

        assert list(sparsifier.redundant_edges(dense)) == [
            (1, 2, {"weight": 5}),
            (2, 3, {"weight": 5}),
        ]

    def test_flag_relevant_edges(self):
        dense = nx.Graph()
        dense.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5)])

        sparsifier = GlobalThresholdSparsifier(10)

        sparsifier.flag_relevant_edges(dense)

        assert list(dense.edges.data()) == [
            (0, 1, {"weight": 10, "relevant": True}),
            (1, 2, {"weight": 5}),
            (2, 3, {"weight": 5}),
        ]

        sparsifier.flag_relevant_edges(dense, full=True)

        assert list(dense.edges.data()) == [
            (0, 1, {"weight": 10, "relevant": True}),
            (1, 2, {"weight": 5, "relevant": False}),
            (2, 3, {"weight": 5, "relevant": False}),
        ]

    def test_flag_redundant_edges(self):
        dense = nx.Graph()
        dense.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5)])

        sparsifier = GlobalThresholdSparsifier(10)

        sparsifier.flag_redundant_edges(dense)

        assert list(dense.edges.data()) == [
            (0, 1, {"weight": 10}),
            (1, 2, {"weight": 5, "redundant": True}),
            (2, 3, {"weight": 5, "redundant": True}),
        ]

        sparsifier.flag_redundant_edges(dense, full=True)

        assert list(dense.edges.data()) == [
            (0, 1, {"weight": 10, "redundant": False}),
            (1, 2, {"weight": 5, "redundant": True}),
            (2, 3, {"weight": 5, "redundant": True}),
        ]

    def test_keep_connected(self):
        dense = nx.Graph()
        dense.add_edge(0, 1, weight=5)

        sparsifier = GlobalThresholdSparsifier(10, keep_connected=True)

        sparse = sparsifier(dense)

        assert list(sparse.edges) == [(0, 1)]
        assert list(sparsifier.relevant_edges(dense)) == [(0, 1, {"weight": 5})]
        assert list(sparsifier.redundant_edges(dense)) == []
