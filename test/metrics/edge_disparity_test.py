# =============================================================================
# Pelote Edge Disparity Unit Tests
# =============================================================================
import networkx as nx
from pytest import raises
from ebbe import with_prev

from pelote.metrics import edge_disparity


class TestEdgeDisparity(object):
    def test_errors(self):
        with raises(TypeError, match="directed"):
            edge_disparity(nx.DiGraph())

    def test_identical_values(self):
        g = nx.Graph()
        g.add_weighted_edges_from(
            [(0, 1, 1), (0, 2, 1), (0, 3, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]
        )
        disparities = edge_disparity(g)

        for previous, current in with_prev(disparities.values()):
            if previous is None:
                continue

            assert previous == current

    def test_correct_disparities(self):
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

        disparities = edge_disparity(g)

        correct_result = {
            (0, 1): 0.0054869684499314125,
            (0, 2): 0.038461538461538436,
            (0, 3): 0.038461538461538436,
            (1, 3): 0.9272976680384089,
            (1, 4): 0.5,
            (2, 4): 0.5,
        }

        assert disparities == correct_result

        reversed_disparities = edge_disparity(g, reverse=True)

        correct_result = {
            (0, 1): 0.9945130315500685,
            (0, 2): 0.9615384615384616,
            (0, 3): 0.9615384615384616,
            (1, 3): 0.07270233196159115,
            (1, 4): 0.5,
            (2, 4): 0.5,
        }

        assert reversed_disparities == correct_result
