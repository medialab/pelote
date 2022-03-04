# =============================================================================
# Pelote Network to Tabular Unit Tests
# =============================================================================
import networkx as nx
import pandas as pd
from pytest import raises

from pelote.exceptions import MissingPandasException
from pelote.shim import missing_pandas
from pelote.network_to_tabular import to_nodes_dataframe


def get_basic_range_graph(n: int = 3) -> nx.Graph:
    g = nx.Graph()
    g.add_nodes_from(range(n))

    for i, node in enumerate(g):
        g.nodes[node]["value"] = i

    return g


class TestToNodesDataframe(object):
    def test_missing_pandas(self):
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
