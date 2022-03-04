# =============================================================================
# Pelote Tabular to Network Unit Tests
# =============================================================================
import networkx as nx
from pytest import raises

from pelote.graph import are_same_graphs
from pelote import to_bipartite_graph


class TestToBipartiteGraph(object):
    def test_errors(self):
        with raises(TypeError):
            to_bipartite_graph([], "one", "one")

    def test_basic(self):
        table = [
            ("john", "apple"),
            ("jack", "apple"),
            ("lisa", "pear"),
        ]

        g = to_bipartite_graph(table, 0, 1, disjoint_keys=True)

        expected = nx.Graph()
        expected.add_node("john", part=0, label="john")
        expected.add_node("jack", part=0, label="jack")
        expected.add_node("lisa", part=0, label="lisa")
        expected.add_node("apple", part=1, label="apple")
        expected.add_node("pear", part=1, label="pear")
        expected.add_edge("john", "apple", weight=1)
        expected.add_edge("jack", "apple", weight=1)
        expected.add_edge("lisa", "pear", weight=1)

        assert are_same_graphs(g, expected, check_attributes=True)
