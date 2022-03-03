# =============================================================================
# Pelote Utilities Unit Tests
# =============================================================================
import networkx as nx

from pelote.utils import has_mixed_types


class TestUtils(object):
    def test_has_mixed_types(self):
        g: nx.Graph = nx.Graph()

        assert not has_mixed_types(g)

        g.add_node(1)

        assert not has_mixed_types(g)

        g.add_node("5")

        assert has_mixed_types(g)
