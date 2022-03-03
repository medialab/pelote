# =============================================================================
# Pelote Network to Tabular Conversion Functions
# =============================================================================
#
# Functions able to convert networkx to various tabular data formats.
#
from typing import Optional

from pelote.types import AnyGraph
from pelote.shim import pd, check_pandas


def to_nodes_dataframe(
    graph: AnyGraph, node_key_col: Optional[str] = "key"
) -> pd.DataFrame:
    check_pandas()

    if node_key_col is None:

        def raw_data():
            for _, a in graph.nodes(data=True):
                yield a

        return pd.DataFrame(data=raw_data(), index=list(graph.nodes))

    else:

        def data_with_key():
            for n, a in graph.nodes(data=True):
                r = {node_key_col: n}
                r.update(a)
                yield r

        return pd.DataFrame(data=data_with_key())
