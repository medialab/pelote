# =============================================================================
# Pelote Metrics Unit Tests
# =============================================================================
import networkx as nx

from pelote.metrics import edge_disparity


class TestEdgeDisparity(object):
    def test_identical_values(self):
        g = nx.Graph()
        g.add_weighted_edges_from(
            [(0, 1, 1), (0, 2, 1), (0, 3, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]
        )
        disparities = edge_disparity(g)
        for i, disparity in enumerate(disparities.values()):
            if i == 0:
                previous_disparity = disparity
            assert previous_disparity == disparity
            previous_disparity = disparity

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

        assert correct_result == disparities
