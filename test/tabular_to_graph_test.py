# =============================================================================
# Pelote Tabular to Network Unit Tests
# =============================================================================
import networkx as nx
from pytest import raises

from pelote.graph import are_same_graphs
from pelote import table_to_bipartite_graph, tables_to_graph


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

        # Basics
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

        # Using a lambda
        g = table_to_bipartite_graph(
            table,
            "person",
            "color",
            first_part_data=lambda row: {"age": row["age"] * 2},
            disjoint_keys=True,
        )

        expected = nx.Graph()
        expected.add_node("john", part="person", label="john", age=90)
        expected.add_node("red", part="color", label="red")
        expected.add_edge("john", "red", weight=1)

        assert are_same_graphs(g, expected, check_attributes=True)

        # Using a mapping
        g = table_to_bipartite_graph(
            table,
            "person",
            "color",
            first_part_data={"age": "label"},
            second_part_data={"light": "dark"},
            disjoint_keys=True,
        )

        expected = nx.Graph()
        expected.add_node("john", part="person", label=45)
        expected.add_node("red", part="color", label="red", dark="high")
        expected.add_edge("john", "red", weight=1)

        assert are_same_graphs(g, expected, check_attributes=True)

    def test_renaming_parts(self):
        table = [{"person": "john", "color": "red", "light": "high", "age": 45}]

        g = table_to_bipartite_graph(
            table,
            "person",
            "color",
            first_part_data=("age",),
            second_part_data=("light",),
            disjoint_keys=True,
            first_part_name="vegetable",
            second_part_name="fruit",
        )

        expected = nx.Graph()
        expected.add_node(
            "john",
            part="vegetable",
            age=45,
            label="john",
        )
        expected.add_node("red", part="fruit", light="high", label="red")
        expected.add_edge("john", "red", weight=1)

        assert are_same_graphs(g, expected, check_attributes=True)


class TestTablesToGraph(object):
    def test_errors(self):
        tables_to_graph(
            [{"key": "john"}],
            [{"source": "john", "target": "lisa"}],
            add_missing_nodes=True,
        )

        with raises(KeyError):
            tables_to_graph([{"key": "john"}], [{"source": "john", "target": "lisa"}])

    def test_basic(self):
        table_nodes = [
            {"key": "john"},
            {"key": "jack"},
            {"key": "lisa"},
        ]
        table_edges = [
            {"source": "john", "target": "jack"},
            {"source": "jack", "target": "lisa"},
        ]

        g = tables_to_graph(table_nodes, table_edges)

        expected = nx.Graph()
        expected.add_node("john")
        expected.add_node("jack")
        expected.add_node("lisa")
        expected.add_edge("john", "jack")
        expected.add_edge("jack", "lisa")

        assert are_same_graphs(g, expected, check_attributes=True)

    def test_weight(self):
        table_nodes = [
            {"key": "john"},
            {"key": "jack"},
            {"key": "lisa"},
        ]

        table_edges = [
            {"source": "john", "target": "jack", "weight": 0.5},
            {"source": "jack", "target": "lisa", "weight": 0.5},
        ]

        g = tables_to_graph(table_nodes, table_edges, edge_data=["weight"])

        expected = nx.Graph()
        expected.add_node("john")
        expected.add_node("jack")
        expected.add_node("lisa")
        expected.add_edge("john", "jack", weight=0.5)
        expected.add_edge("jack", "lisa", weight=0.5)

        assert are_same_graphs(g, expected, check_attributes=True)

    def test_directed(self):
        table_nodes = [
            {"key": "john"},
            {"key": "jack"},
            {"key": "lisa"},
        ]

        table_edges = [
            {"source": "john", "target": "jack", "weight": 0.5},
            {"source": "jack", "target": "lisa", "weight": 0.5},
            {"source": "lisa", "target": "jack", "weight": 0.5},
        ]

        g = tables_to_graph(
            table_nodes, table_edges, edge_data=["weight"], directed=True
        )

        expected = nx.DiGraph()
        expected.add_node("john")
        expected.add_node("jack")
        expected.add_node("lisa")
        expected.add_edge("john", "jack", weight=0.5)
        expected.add_edge("jack", "lisa", weight=0.5)
        expected.add_edge("lisa", "jack", weight=0.5)

        assert are_same_graphs(g, expected, check_attributes=True)

    def test_custom_attributes(self):
        table_nodes = [
            {"key": "john", "color": "blue"},
            {"key": "jack", "color": "green"},
            {"key": "lisa", "color": "green"},
        ]

        table_edges = [
            {"source": "john", "target": "jack", "weight": 0.5},
            {"source": "jack", "target": "lisa", "weight": 0.5},
        ]

        g = tables_to_graph(
            table_nodes, table_edges, edge_data=["weight"], node_data=["color"]
        )

        expected = nx.Graph()
        expected.add_node("john", color="blue")
        expected.add_node("jack", color="green")
        expected.add_node("lisa", color="green")
        expected.add_edge("john", "jack", weight=0.5)
        expected.add_edge("jack", "lisa", weight=0.5)

        assert are_same_graphs(g, expected, check_attributes=True)

    def test_count_rows_as_weight(self):
        table_nodes = [
            {"key": "john", "color": "blue"},
            {"key": "jack", "color": "green"},
            {"key": "lisa", "color": "green"},
        ]

        table_edges = [
            {"source": "john", "target": "jack"},
            {"source": "jack", "target": "lisa"},
            {"source": "jack", "target": "lisa"},
        ]

        g = tables_to_graph(
            table_nodes, table_edges, node_data=["color"], count_rows_as_weight=True
        )

        expected = nx.Graph()
        expected.add_node("john", color="blue")
        expected.add_node("jack", color="green")
        expected.add_node("lisa", color="green")
        expected.add_edge("john", "jack", weight=1)
        expected.add_edge("jack", "lisa", weight=2)

        assert are_same_graphs(g, expected, check_attributes=True)

    # TODO: test callable spec also
    # def test_renamed_part_data(self):
    #     table = [{"person": "john", "color": "red", "light": "high", "age": 45}]

    #     g = table_to_bipartite_graph(
    #         table,
    #         "person",
    #         "color",
    #         first_part_data={"age": "Age"},
    #         second_part_data={"light": "Light"},
    #         disjoint_keys=True,
    #     )

    #     expected = nx.Graph()
    #     expected.add_node("john", part="person", label="john", Age=45)
    #     expected.add_node("red", part="color", label="red", Light="high")
    #     expected.add_edge("john", "red", weight=1)

    #     assert are_same_graphs(g, expected, check_attributes=True)
