# =============================================================================
# Pelote Projection Unit Tests
# =============================================================================
import networkx as nx
from pytest import raises

from pelote import monopartite_projection

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


class TestMonopartiteProjection(object):
    def test_errors(self):
        with raises(TypeError):
            monopartite_projection(None, "person")

        with raises(TypeError):
            monopartite_projection(nx.Graph(), "person", metric="test")

    def test_basic(self):
        monopartite = monopartite_projection(BIPARTITE, "people")
