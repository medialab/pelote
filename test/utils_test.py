# =============================================================================
# Pelote Utilities Unit Tests
# =============================================================================
import networkx as nx
from typing import Union

from pelote.utils import has_mixed_type_node_keys


class TestUtils(object):
    def test_has_mixed_type_node_keys(self):
        g: nx.Graph[Union[int, str]] = nx.Graph()

        assert not has_mixed_type_node_keys(g)

        g.add_node(1)

        assert not has_mixed_type_node_keys(g)

        g.add_node("5")

        assert has_mixed_type_node_keys(g)
