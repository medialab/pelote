# =============================================================================
# Pelote Network to Tabular Unit Tests
# =============================================================================
import networkx as nx
import pandas as pd
from pytest import raises

from pelote.exceptions import MissingPandasException
from pelote.shim import missing_pandas
from pelote.network_to_tabular import (
    to_nodes_dataframe,
    to_edges_dataframe,
    to_dataframes,
)


def get_basic_range_graph(n: int = 3) -> nx.Graph:
    g = nx.Graph()
    g.add_nodes_from(range(n))

    for i, node in enumerate(g):
        g.nodes[node]["value"] = i

    return g


class TestToNodesDataframe(object):
    def test_errors(self):
        with raises(MissingPandasException), missing_pandas():
            to_nodes_dataframe(nx.Graph())

        with raises(TypeError):
            to_nodes_dataframe(None)

    def test_default_behavior(self):
        g = get_basic_range_graph()

        df = to_nodes_dataframe(g)
        expected = pd.DataFrame(data={"key": list(range(3)), "value": list(range(3))})

        assert df.equals(expected)

    def test_node_key_col(self):
        g = get_basic_range_graph()

        df = to_nodes_dataframe(g, node_key_col="node")
        expected = pd.DataFrame(data={"node": list(range(3)), "value": list(range(3))})

        assert df.equals(expected)

    def test_node_key_as_index(self):
        g = get_basic_range_graph()

        df = to_nodes_dataframe(g, node_key_col=None)
        expected = pd.DataFrame(index=list(range(3)), data={"value": list(range(3))})

        assert df.equals(expected)


class TestToEdgesDataframe(object):
    def test_errors(self):
        with raises(MissingPandasException), missing_pandas():
            to_edges_dataframe(nx.Graph())

        with raises(TypeError):
            to_edges_dataframe(None)

    def test_default_behavior(self):
        g = nx.Graph()
        g.add_edge(0, 1, weight=2.0)

        df = to_edges_dataframe(g)
        expected = pd.DataFrame(data={"source": [0], "target": [1], "weight": [2.0]})

        assert df.equals(expected)

    def test_key_cols(self):
        g = nx.Graph()
        g.add_edge(0, 1, weight=2.0)

        df = to_edges_dataframe(g, edge_source_col="Source", edge_target_col="Target")
        expected = pd.DataFrame(data={"Source": [0], "Target": [1], "weight": [2.0]})

        assert df.equals(expected)


class TestToDataframes(object):
    def test_errors(self):
        with raises(MissingPandasException), missing_pandas():
            to_dataframes(nx.Graph())

        with raises(TypeError):
            to_dataframes(None)

    def test_default_behavior(self):
        g = nx.Graph()
        g.add_edge(0, 1, weight=2.0)

        nodes, edges = to_dataframes(g)
        expected_nodes = pd.DataFrame(data={"key": [0, 1]})
        expected_edges = pd.DataFrame(
            data={"source": [0], "target": [1], "weight": [2.0]}
        )

        assert nodes.equals(expected_nodes)
        assert edges.equals(expected_edges)

    def test_key_cols(self):
        g = nx.Graph()
        g.add_edge(0, 1, weight=2.0)

        nodes, edges = to_dataframes(
            g, node_key_col="Node", edge_source_col="Source", edge_target_col="Target"
        )
        expected_nodes = pd.DataFrame(data={"Node": [0, 1]})
        expected_edges = pd.DataFrame(
            data={"Source": [0], "Target": [1], "weight": [2.0]}
        )

        assert nodes.equals(expected_nodes)
        assert edges.equals(expected_edges)
