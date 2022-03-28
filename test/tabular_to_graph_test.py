# =============================================================================
# Pelote Tabular to Network Unit Tests
# =============================================================================
import networkx as nx
from pytest import raises

from pelote.graph import are_same_graphs
from pelote import table_to_bipartite_graph


class TestToBipartiteGraph(object):
    def test_errors(self):
        with raises(TypeError):
            table_to_bipartite_graph([], "one", "one")

    def test_basic(self):
        table = [
            ("john", "apple"),
            ("jack", "apple"),
            ("lisa", "pear"),
        ]

        g = table_to_bipartite_graph(table, 0, 1, disjoint_keys=True)

        expected = nx.Graph()
        expected.add_node("john", part=0, label="john")
        expected.add_node("jack", part=0, label="jack")
        expected.add_node("lisa", part=0, label="lisa")
        expected.add_node("apple", part=1, label="apple")
        expected.add_node("pear", part=1, label="pear")
        expected.add_edge("john", "apple", weight=1)
        expected.add_edge("jack", "apple", weight=1)
        expected.add_edge("lisa", "pear", weight=1)

        assert are_same_graphs(g, expected, check_attributes=True)

    def test_key_generation(self):
        table = [
            ("john", "apple"),
            ("jack", "apple"),
            ("lisa", "pear"),
        ]

        g = table_to_bipartite_graph(table, 0, 1)

        expected = nx.Graph()
        expected.add_node(0, part=0, label="john")
        expected.add_node(2, part=0, label="jack")
        expected.add_node(3, part=0, label="lisa")
        expected.add_node(1, part=1, label="apple")
        expected.add_node(4, part=1, label="pear")
        expected.add_edge(0, 1, weight=1)
        expected.add_edge(2, 1, weight=1)
        expected.add_edge(3, 4, weight=1)

        assert are_same_graphs(g, expected, check_attributes=True)

    def test_weight(self):
        table = [("john", "apple"), ("john", "apple"), ("john", "pear")]

        g = table_to_bipartite_graph(table, 0, 1, disjoint_keys=True)

        expected = nx.Graph()
        expected.add_node("john", part=0, label="john")
        expected.add_node("apple", part=1, label="apple")
        expected.add_node("pear", part=1, label="pear")
        expected.add_edge("john", "apple", weight=2)
        expected.add_edge("john", "pear", weight=1)

        assert are_same_graphs(g, expected, check_attributes=True)

    def test_custom_attributes(self):
        table = [("john", "apple"), ("john", "apple"), ("john", "pear")]

        g = table_to_bipartite_graph(
            table,
            0,
            1,
            disjoint_keys=True,
            node_part_attr="category",
            edge_weight_attr="count",
        )

        expected = nx.Graph()
        expected.add_node("john", category=0, label="john")
        expected.add_node("apple", category=1, label="apple")
        expected.add_node("pear", category=1, label="pear")
        expected.add_edge("john", "apple", count=2)
        expected.add_edge("john", "pear", count=1)

        assert are_same_graphs(g, expected, check_attributes=True)

    def test_part_data(self):
        table = [{"person": "john", "color": "red", "light": "high", "age": 45}]

        g = table_to_bipartite_graph(
            table,
            "person",
            "color",
            first_part_data=("age",),
            second_part_data=("light",),
            disjoint_keys=True,
        )

        expected = nx.Graph()
        expected.add_node("john", part="person", label="john", age=45)
        expected.add_node("red", part="color", label="red", light="high")
        expected.add_edge("john", "red", weight=1)

        assert are_same_graphs(g, expected, check_attributes=True)

    def test_names(self):
        table = [{"person": "john", "color": "red", "light": "high", "age": 45, "vegetable": "asparagus", "fruit": "coconut"}]

        g = table_to_bipartite_graph(
            table,
            "person",
            "color",
            first_part_data=("age",),
            second_part_data=("light",),
            disjoint_keys=True,
            first_part_name="vegetable",
            second_part_name="fruit"
        )

        expected = nx.Graph()
        expected.add_node("john", part="vegetable", age=45, label="john",)
        expected.add_node("red", part="fruit", light="high", label="red")
        expected.add_edge("john", "red", weight=1)

        assert are_same_graphs(g, expected, check_attributes=True)
