# =============================================================================
# Pelote Tabular to Network Unit Tests
# =============================================================================
from pytest import raises

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

        g = to_bipartite_graph(table, 0, 1)

        assert g.order() == 5
        assert g.size() == len(table)
