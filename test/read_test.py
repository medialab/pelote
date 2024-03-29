# =============================================================================
# Pelote Read Unit Tests
# =============================================================================
import json
import networkx as nx
from pytest import raises
from pathlib import Path

from test.utils import get_resource_path

from pelote.read import parse_graphology_json, read_graphology_json


class TestReadGraphologyJson(object):
    def test_parsing_errors(self):
        with raises(TypeError):
            parse_graphology_json({})

        with raises(TypeError, match="mixed"):
            data = {
                "options": {"type": "mixed", "multi": False, "allowSelfLoops": True},
                "nodes": [{"key": "one"}, {"key": "two"}, {"key": "three"}],
                "edges": [
                    {"source": "one", "target": "two", "undirected": True},
                    {"source": "two", "target": "three", "undirected": False},
                ],
            }

            parse_graphology_json(data)

    def test_parsing_basic(self):
        data = {
            "options": {"type": "directed", "multi": False, "allowSelfLoops": True},
            "nodes": [
                {"key": "one", "attributes": {"hello": "world"}},
                {"key": "two", "attributes": {"age": 34}},
            ],
            "edges": [{"source": "one", "target": "two", "attributes": {"weight": 35}}],
        }

        g = parse_graphology_json(data)

        assert list(g.nodes(data=True)) == [
            ("one", {"hello": "world"}),
            ("two", {"age": 34}),
        ]

        assert list(g.edges(data=True)) == [("one", "two", {"weight": 35})]

        assert isinstance(g, nx.DiGraph)

    def test_parsing_graph_attributes(self):
        data = {
            "options": {"type": "mixed", "multi": False, "allowSelfLoops": True},
            "attributes": {"name": "Test Graph", "year": 2022},
            "nodes": [{"key": "one"}, {"key": "two"}],
            "edges": [{"source": "one", "target": "two"}],
        }

        g = parse_graphology_json(data)

        assert g.graph == {"name": "Test Graph", "year": 2022}

    def test_parsing_multi(self):
        data = {
            "options": {"type": "undirected", "multi": True, "allowSelfLoops": True},
            "nodes": [
                {"key": "one", "attributes": {"hello": "world"}},
                {"key": "two", "attributes": {"age": 34}},
            ],
            "edges": [
                {"source": "one", "target": "two", "attributes": {"weight": 35}},
                {
                    "key": "one--two",
                    "source": "one",
                    "target": "two",
                    "attributes": {"weight": 12},
                },
            ],
        }

        g = parse_graphology_json(data)

        assert list(g.nodes(data=True)) == [
            ("one", {"hello": "world"}),
            ("two", {"age": 34}),
        ]

        def key(x) -> str:
            return str(x[2])

        assert sorted(list(g.edges(data=True, keys=True)), key=key) == [
            ("one", "two", 0, {"weight": 35}),
            ("one", "two", "one--two", {"weight": 12}),
        ]

        assert isinstance(g, nx.MultiGraph)

    def test_read(self):
        with raises(TypeError):
            read_graphology_json(None)

        les_miserables_path = get_resource_path("les_miserables.json")

        def check_graph(g) -> None:
            assert g.order() == 77
            assert g.size() == 254
            assert isinstance(g, nx.DiGraph)

        check_graph(read_graphology_json(les_miserables_path))
        check_graph(read_graphology_json(Path(les_miserables_path)))

        with open(les_miserables_path) as f:
            check_graph(read_graphology_json(f))

        with open(les_miserables_path) as f:
            data = json.load(f)
            check_graph(read_graphology_json(data))

    def test_falsely_mixed(self):
        data = {
            "options": {"type": "mixed", "multi": False, "allowSelfLoops": True},
            "nodes": [{"key": "one"}, {"key": "two"}, {"key": "three"}],
            "edges": [
                {"source": "one", "target": "two", "undirected": True},
            ],
        }

        g = parse_graphology_json(data)

        assert isinstance(g, nx.Graph)

        data = {
            "options": {"type": "mixed", "multi": False, "allowSelfLoops": True},
            "nodes": [{"key": "one"}, {"key": "two"}, {"key": "three"}],
            "edges": [
                {"source": "one", "target": "two"},
            ],
        }

        g = parse_graphology_json(data)

        assert isinstance(g, nx.DiGraph)
