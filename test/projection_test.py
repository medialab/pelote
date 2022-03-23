# =============================================================================
# Pelote Projection Unit Tests
# =============================================================================
import networkx as nx
from pytest import raises

from pelote import monopartite_projection
from pelote.graph import are_same_graphs

NODES = [
    ("John", "people"),
    ("Mary", "people"),
    ("Lucy", "people"),
    ("Gabriel", "people"),
    ("Meredith", "people"),
    ("red", "color"),
    ("blue", "color"),
    ("yellow", "color"),
    ("purple", "color"),
    ("orange", "color"),
]

PEOPLE_PART = set([n[0] for n in NODES if n[1] == "people"])

EDGES = [
    ("John", "red", 1.0),
    ("John", "purple", 3.0),
    ("Gabriel", "yellow", 2.0),
    ("Gabriel", "orange", 4.0),
    ("Mary", "red", 2.0),
    ("Mary", "yellow", 1.0),
    ("Lucy", "red", 7.0),
    ("Lucy", "purple", 1.0),
]

BIPARTITE = nx.Graph()

for key, part in NODES:
    BIPARTITE.add_node(key, part=part)

BIPARTITE.add_weighted_edges_from(EDGES)

PEOPLE_MONOPARTITE_NODES = set(n[0] for n in NODES if n[1] == "people")

PEOPLE_MONOPARTITE_EDGES = {
    ("John", "Mary", 1),
    ("John", "Lucy", 2),
    ("Mary", "Lucy", 1),
    ("Mary", "Gabriel", 1),
}

PEOPLE_MONOPARTITE = nx.Graph()
PEOPLE_MONOPARTITE.add_nodes_from(PEOPLE_MONOPARTITE_NODES)
PEOPLE_MONOPARTITE.add_weighted_edges_from(PEOPLE_MONOPARTITE_EDGES)


class TestMonopartiteProjection(object):
    def test_errors(self):

        # Bad graph
        with raises(TypeError, match="graph"):
            monopartite_projection(None, "person")

        # Bad metric
        with raises(TypeError, match="metric"):
            monopartite_projection(nx.Graph(), "person", metric="test")

        # Empty partition
        with raises(TypeError, match="exist"):
            g = nx.Graph()
            g.add_edge(0, 1)
            monopartite_projection(g, "person")

    def test_basic(self):
        monopartite = monopartite_projection(BIPARTITE, "people")

        assert are_same_graphs(monopartite, PEOPLE_MONOPARTITE)

    def test_only_one_part_tagged(self):
        untagged_color_bipartite = BIPARTITE.copy()

        for _, attr in untagged_color_bipartite.nodes.data():
            if attr["part"] == "color":
                del attr["part"]

        monopartite = monopartite_projection(untagged_color_bipartite, "people")

        assert are_same_graphs(monopartite, PEOPLE_MONOPARTITE)
