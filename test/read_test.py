# =============================================================================
# Pelote Read Unit Tests
# =============================================================================
from typing import cast
from pytest import raises

from pelote.types import GraphologySerializedGraph
from pelote.read import parse_graphology_json


class TestReadGraphologyJson(object):
    def test_parsing_errors(self):
        data = cast(GraphologySerializedGraph, {})

        with raises(TypeError):
            parse_graphology_json(data)

    def test_parsing(self):
        data: GraphologySerializedGraph = {
            "options": {"type": "directed", "multi": False, "allowSelfLoops": True},
            "nodes": [{"key": "one", "attributes": {"hello": "world"}}],
        }

        g = parse_graphology_json(data)

        assert list(g.nodes(data=True)) == [("one", {"hello": "world"})]
