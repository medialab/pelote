# =============================================================================
# Pelote Network to Tabular Unit Tests
# =============================================================================
import networkx as nx
import pandas as pd
from pytest import raises

from pelote.exceptions import MissingPandasException
from pelote.shim import missing_pandas
from pelote.network_to_tabular import to_nodes_dataframe


class TestNetworkToTabular(object):
    def test_to_nodes_dataframe(self):
        with raises(MissingPandasException), missing_pandas():
            to_nodes_dataframe(nx.Graph())

        g: nx.Graph[int] = nx.Graph()
        g.add_nodes_from(range(3))

        for i, node in enumerate(g):
            g.nodes[node]["value"] = i

        df = to_nodes_dataframe(g)
        expected = pd.DataFrame(index=list(range(3)), data={"value": list(range(3))})

        assert df.equals(expected)
