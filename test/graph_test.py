# =============================================================================
# Pelote Graph Unit Tests
# =============================================================================
import networkx as nx

from pelote.graph import (
    largest_connected_component,
    crop_to_largest_connected_components,
)


class TestGraph(object):
    def test_largest_connected_component(self):
        g = nx.MultiGraph()
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(0, 2)

        g.add_edge(3, 4)
        g.add_edge(4, 5)

        g.add_node(6)

        assert largest_connected_component(g) == {0, 1, 2}

        g.add_edge(7, 8)
        g.add_edge(8, 9)
        g.add_edge(9, 10)
        g.add_edge(10, 11)

        assert largest_connected_component(g) == {7, 8, 9, 10, 11}

        crop_to_largest_connected_components(g)

        assert set(g.nodes) == {7, 8, 9, 10, 11}
        assert g.size() == 4

        g = nx.DiGraph()
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(0, 2)

        g.add_edge(3, 4)
        g.add_edge(4, 5)

        g.add_node(6)

        assert largest_connected_component(g) == {0, 1, 2}

        crop_to_largest_connected_components(g)

        assert set(g.nodes) == {0, 1, 2}
        assert g.size() == 3
