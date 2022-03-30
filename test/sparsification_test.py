# =============================================================================
# Pelote Sparsification Unit Tests
# =============================================================================
import networkx as nx

from pelote.graph import are_same_graphs
from pelote.sparsification.global_threshold import GlobalThresholdSparsifier


class TestGlobalThresholdSparsifier(object):
    def test_basics(self):
        dense = nx.Graph()
        dense.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5)])

        sparsifier = GlobalThresholdSparsifier(10)

        sparse = sparsifier(dense)

        expected = nx.Graph()
        expected.add_nodes_from(range(4))
        expected.add_edge(0, 1, weight=10)

        assert are_same_graphs(sparse, expected, check_attributes=True)
        assert are_same_graphs(sparse, sparsifier.filter(dense), check_attributes=True)
