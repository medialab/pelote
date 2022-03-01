# =============================================================================
# Pelote Network to Tabular Unit Tests
# =============================================================================
import networkx as nx
from pytest import raises

from pelote.exceptions import MissingPandasException
from pelote.shim import missing_pandas
from pelote.network_to_tabular import to_nodes_dataframe


class TestNetworkToTabular(object):
    def test_to_nodes_dataframe(self):
        with raises(MissingPandasException), missing_pandas():
            to_nodes_dataframe(nx.Graph())
