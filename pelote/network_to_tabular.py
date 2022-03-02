# =============================================================================
# Pelote Network to Tabular Conversion Functions
# =============================================================================
#
# Functions able to convert networkx to various tabular data formats.
#
from typing import Any

from pelote.types import AnyGraph
from pelote.shim import pd, check_pandas


def to_nodes_dataframe(graph: "AnyGraph[Any]") -> pd.DataFrame:
    check_pandas()

    iterator = (a for _, a in graph.nodes(data=True))

    df = pd.DataFrame(data=iterator, index=list(graph.nodes))

    return df
