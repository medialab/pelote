# =============================================================================
# Pelote Utilities Unit Tests
# =============================================================================
import networkx as nx

from pelote.utils import has_mixed_types, uint_representation_for_capacity


class TestUtils(object):
    def test_has_mixed_types(self):
        g = nx.Graph()

        assert not has_mixed_types(g)

        g.add_node(1)

        assert not has_mixed_types(g)

        g.add_node("5")

        assert has_mixed_types(g)

    def test_uint_representation_for_capacity(self):
        assert uint_representation_for_capacity(34).code == "B"
        assert uint_representation_for_capacity(345).code == "H"
        assert uint_representation_for_capacity(486462).code == "L"
        assert uint_representation_for_capacity(847586358646854).code == "Q"
