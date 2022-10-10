# =============================================================================
# Pelote Chiba Nishizeki Unit Tests
# =============================================================================
import networkx as nx

from pelote.metrics.chiba_nishizeki import (
    triangles,
    triangular_strength,
    naive_triangular_strength,
)


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
        assert strengths == naive_triangular_strength(graph)

        strengths = triangular_strength(graph, full=True)

        assert strengths == {(1, 2): 1, (2, 3): 1, (1, 3): 1, (0, 1): 0}
        assert strengths == naive_triangular_strength(graph, full=True)

        graph.add_edge(4, 2)
        graph.add_edge(4, 3)

        strengths = triangular_strength(graph, full=True)

        assert strengths == {
            (1, 2): 1,
            (2, 3): 2,
            (1, 3): 1,
            (0, 1): 0,
            (2, 4): 1,
            (3, 4): 1,
        }
        assert strengths == naive_triangular_strength(graph, full=True)

        # Complete graphs
        for n in range(3, 10):
            k = nx.complete_graph(n)

            assert len(list(triangles(k))) == (n * (n - 1) * (n - 2)) / 6

            strengths = triangular_strength(k)

            assert len(strengths) == n * (n - 1) // 2
            assert all(x == n - 2 for x in strengths.values())

            assert strengths == naive_triangular_strength(k)
