# =============================================================================
# Pelote Graph Unit Tests
# =============================================================================
import networkx as nx
from pytest import raises
from collections import Counter

from pelote.graph import (
    are_same_graphs,
    largest_connected_component,
    crop_to_largest_connected_component,
    connected_component_orders,
    filter_edges,
)


class TestLargestConnectedComponent(object):
    def test_basics(self):
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

        crop_to_largest_connected_component(g)

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

        crop_to_largest_connected_component(g)

        assert set(g.nodes) == {0, 1, 2}
        assert g.size() == 3


class TestConnectedComponentSizes(object):
    def test_errors(self):
        with raises(TypeError):
            connected_component_orders("test")

        with raises(TypeError):
            connected_component_orders(nx.Graph(), edge_filter="test")

    def test_basics(self):
        g = nx.Graph()
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(0, 2)

        assert list(connected_component_orders(g)) == [3]

        g.add_edge(3, 4)

        g.add_node(5)

        assert set(connected_component_orders(g)) == {1, 2, 3}

        g.add_edge(6, 7, skip=True)

        assert Counter(connected_component_orders(g)) == Counter([3, 2, 1, 2])
        assert Counter(
            connected_component_orders(g, lambda s, t, e: not e.get("skip", False))
        ) == Counter([3, 2, 1, 1, 1])


class TestFilterEdges(object):
    def test_basics(self):
        g = nx.Graph()
        g.add_weighted_edges_from([(0, 1, 10), (1, 2, 5), (2, 3, 5)])

        h = filter_edges(g, lambda u, v, a: a["weight"] >= 10)

        expected = nx.Graph()
        expected.add_nodes_from(range(4))
        expected.add_edge(0, 1, weight=10)

        assert are_same_graphs(h, expected, check_attributes=True)
