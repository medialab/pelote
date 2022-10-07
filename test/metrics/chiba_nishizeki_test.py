# =============================================================================
# Pelote Chiba Nishizeki Unit Tests
# =============================================================================
import networkx as nx

from pelote.metrics.chiba_nishizeki import triangles, triangular_strength


class TestChibaNishizeki(object):
    def test_triangles(self):
        graph = nx.Graph()

        graph.add_edge("A", "B")
        graph.add_edge("A", "F")
        graph.add_edge("B", "F")
        graph.add_edge("E", "F")
        graph.add_edge("B", "E")
        graph.add_edge("B", "C")
        graph.add_edge("C", "D")

        T = set(triangles(graph))

        assert T == {("B", "E", "F"), ("B", "F", "A")}

        graph.add_edge("B", "D")

        T = set(triangles(graph))

        assert T == {("B", "D", "C"), ("B", "F", "A"), ("B", "E", "F")}

        graph.add_edge("G", "H")
        graph.add_edge("H", "I")
        graph.add_edge("I", "G")

        graph.add_edge("G", "G")

        T = set(triangles(graph))

        assert T == {("B", "D", "C"), ("B", "F", "A"), ("B", "E", "F"), ("G", "I", "H")}

    def test_triangular_strength(self):
        graph = nx.Graph()

        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 1)

        strengths = triangular_strength(graph)

        assert strengths == {(1, 2): 1, (2, 3): 1, (1, 3): 1}

        strengths = triangular_strength(graph, full=True)

        assert strengths == {(1, 2): 1, (2, 3): 1, (1, 3): 1, (0, 1): 0}
