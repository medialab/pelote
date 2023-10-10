# =============================================================================
# Pelote Edge Disparity Unit Tests
# =============================================================================
import networkx as nx
from pytest import raises
from ebbe import with_prev

from pelote.metrics import edge_redundancy


class TestEdgeRedundancy(object):
    def test_errors(self):
        with raises(TypeError, match="multi"):
            edge_redundancy(nx.MultiGraph())

    def test_identical_values(self):
        g = nx.Graph()
        g.add_edges_from([(0, 1), (0, 2), (1, 2)])
        redundancies = edge_redundancy(g, edge_strength_ranking_threshold=1)

        for previous, current in with_prev(redundancies.values()):
            if previous is None:
                continue

            assert previous == current

    def test_redundancy_takes_all(self):
        g = nx.Graph()
        g.add_edges_from([(0, 1)])

        redundancies = edge_redundancy(g, edge_strength_ranking_threshold=1)

        correct_result = {
            (0, 1): 0,
        }

        assert redundancies == correct_result

    def test_result_nothing(self):
        g = nx.Graph()
        g.add_edges_from([(0, 1), (0, 2), (1, 2)])

        redundancies = edge_redundancy(g)

        correct_result = {
            (0, 1): 0,
            (0, 2): 0,
            (1, 2): 0,
        }

        assert redundancies == correct_result

        g = nx.Graph()

        redundancies = edge_redundancy(g)

        correct_result = {}

        assert redundancies == correct_result

    def test_correct_redundancies(self):
        g = nx.Graph()

        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)
        g.add_edge(4, 2)
        g.add_edge(4, 3)

        redundancies = edge_redundancy(g, edge_strength_ranking_threshold=1)

        correct_result = {
            (0, 1): 0,
            (1, 2): 1,
            (1, 3): 1,
            (2, 3): 0,
            (2, 4): 1,
            (3, 4): 1,
        }

        assert redundancies == correct_result

        g = nx.Graph()

        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)
        g.add_edge(4, 2)
        g.add_edge(4, 3)

        redundancies = edge_redundancy(
            g, edge_strength_ranking_threshold=1, reciprocity=True
        )

        correct_result = {
            (0, 1): 0,
            (1, 2): 1,
            (1, 3): 1,
            (2, 3): 1,
            (2, 4): 1,
            (3, 4): 1,
        }

        assert redundancies == correct_result

        g = nx.Graph()

        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)
        g.add_edge(4, 2)
        g.add_edge(4, 3)

        redundancies = edge_redundancy(g, edge_strength_ranking_threshold=2)

        correct_result = {
            (0, 1): 0,
            (1, 2): 1,
            (1, 3): 1,
            (2, 3): 2,
            (2, 4): 1,
            (3, 4): 1,
        }

        assert redundancies == correct_result

        g = nx.complete_graph(5)

        g.add_node(10)

        g.remove_edge(0, 4)
        g.remove_edge(1, 2)
        g.remove_edge(2, 3)
        g.remove_edge(3, 4)

        for e in g.edges:
            if e[0] == 0:
                g[e[0]][e[1]]["weight"] = 25
            else:
                g[e[0]][e[1]]["weight"] = 1

        redundancies = edge_redundancy(
            g, edge_strength_ranking_threshold=1, edge_weight_attr="weight"
        )

        correct_result = {
            (0, 1): 0,
            (0, 2): 0,
            (0, 3): 0,
            (1, 3): 1,
            (1, 4): 0,
            (2, 4): 0,
        }

        assert redundancies == correct_result

        g = nx.DiGraph()

        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)
        g.add_edge(4, 2)
        g.add_edge(4, 3)

        redundancies = edge_redundancy(g, edge_strength_ranking_threshold=1)

        correct_result = {
            (0, 1): 0,
            (1, 2): 1,
            (3, 1): 1,
            (2, 3): 0,
            (4, 2): 1,
            (4, 3): 1,
        }

        assert redundancies == correct_result

        g = nx.DiGraph()

        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)
        g.add_edge(4, 2)
        g.add_edge(4, 3)

        redundancies = edge_redundancy(
            g, edge_strength_ranking_threshold=1, in_or_out_edge="out"
        )

        correct_result = {
            (0, 1): 0,
            (1, 2): 0,
            (3, 1): 0,
            (2, 3): 0,
            (4, 2): 1,
            (4, 3): 0,
        }

        assert redundancies == correct_result

        g = nx.DiGraph()

        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)
        g.add_edge(4, 2)
        g.add_edge(4, 3)

        redundancies = edge_redundancy(
            g, edge_strength_ranking_threshold=1, in_or_out_edge="in"
        )

        correct_result = {
            (0, 1): 0,
            (1, 2): 0,
            (3, 1): 0,
            (2, 3): 0,
            (4, 2): 0,
            (4, 3): 0,
        }

        assert redundancies == correct_result
