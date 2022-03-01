# =============================================================================
# Pelote Network to Tabular Conversion Functions
# =============================================================================
#
# Functions able to convert networkx to various tabular data formats.
#
from pelote.types import AnyGraph
from pelote.shim import pd, check_pandas


def to_nodes_dataframe(graph: AnyGraph) -> pd.DataFrame:
    check_pandas()

    return pd.DataFrame()
