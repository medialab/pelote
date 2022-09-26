# =============================================================================
# Pelote Write Unit Tests
# =============================================================================
import networkx as nx
from pytest import raises

from pelote.read import read_graphology_json
from pelote.write import write_graphology_json
from pelote.graph import are_same_graphs


class TestWriteGraphologyJson(object):
    def test_write_basic(self):
        g = nx.DiGraph()
        g.add_nodes_from(
            [
                ("one", {"hello": "world", "hey": "how are you?"}),
                ("two", {"age": 34}),
            ]
        )
        g.add_edges_from(
            [
                ("one", "two", {"weight": 35}),
            ]
        )

        data = {
            "options": {"type": "directed", "multi": False, "allowSelfLoops": True},
            "nodes": [
                {"key": "one", "attributes": {"hello": "world", "hey": "how are you?"}},
                {"key": "two", "attributes": {"age": 34}},
            ],
            "edges": [{"source": "one", "target": "two", "attributes": {"weight": 35}}],
        }

        assert write_graphology_json(g) == data

    def test_write_multi(self):
        g = nx.MultiGraph()
        g.add_nodes_from(
            [
                ("one", {"hello": "world"}),
                ("two", {"age": 34}),
            ]
        )
        g.add_edges_from(
            [
                ("one", "two", {"weight": 35}),
                ("one", "two", {"weight": 12}),
            ]
        )

        data = {
            "options": {"type": "undirected", "multi": True, "allowSelfLoops": True},
            "nodes": [
                {"key": "one", "attributes": {"hello": "world"}},
                {"key": "two", "attributes": {"age": 34}},
            ],
            "edges": [
                {"source": "one", "target": "two", "attributes": {"weight": 35}},
                {
                    "source": "one",
                    "target": "two",
                    "attributes": {"weight": 12},
                },
            ],
        }

        assert write_graphology_json(g) == data

    def test_write_read_basic(self):

        data = {
            "options": {"type": "directed", "multi": False, "allowSelfLoops": True},
            "nodes": [
                {"key": "one", "attributes": {"hello": "world"}},
                {"key": "two", "attributes": {"age": 34}},
            ],
            "edges": [{"source": "one", "target": "two", "attributes": {"weight": 35}}],
        }

        assert write_graphology_json(read_graphology_json(data)) == data

    def test_write_read_multi(self):

        data = {
            "options": {"type": "undirected", "multi": True, "allowSelfLoops": True},
            "nodes": [
                {"key": "one", "attributes": {"hello": "world"}},
                {"key": "two", "attributes": {"age": 34}},
            ],
            "edges": [
                {"source": "one", "target": "two", "attributes": {"weight": 35}},
                {
                    "source": "one",
                    "target": "two",
                    "attributes": {"weight": 12},
                },
            ],
        }

        assert write_graphology_json(read_graphology_json(data)) == data

    def test_read_write_basic(self):

        g = nx.DiGraph()
        g.add_nodes_from(
            [
                ("one", {"hello": "world"}),
                ("two", {"age": 34}),
            ]
        )
        g.add_edges_from(
            [
                ("one", "two", {"weight": 35}),
            ]
        )

        assert are_same_graphs(read_graphology_json(write_graphology_json(g)), g)

    def test_read_write_multi(self):

        g = nx.MultiGraph()
        g.add_nodes_from(
            [
                ("one", {"hello": "world"}),
                ("two", {"age": 34}),
            ]
        )
        g.add_edges_from(
            [
                ("one", "two", {"weight": 35}),
                ("one", "two", {"weight": 12}),
            ]
        )

        assert are_same_graphs(read_graphology_json(write_graphology_json(g)), g)

    def test_unserializable_node_keys(self):
        g = nx.Graph()
        g.add_node((1, 2))

        with raises(TypeError, match="key"):
            write_graphology_json(g)

    def test_mixed_node_keys(self):
        g = nx.Graph()
        g.add_edge(1, "2")

        with raises(TypeError, match="mixed"):
            write_graphology_json(g)

        data = write_graphology_json(g, allow_mixed_keys=True)

        assert data["nodes"] == [{"key": "1"}, {"key": "2"}]

    def test_invalid_attribute_names(self):
        g = nx.Graph()

        g.add_node("test")
        g.nodes["test"][45] = "ok"

        with raises(TypeError, match="attr"):
            write_graphology_json(g)

        data = write_graphology_json(g, allow_invalid_attr_names=True)

        assert data["nodes"] == [{"key": "test", "attributes": {"45": "ok"}}]
