# =============================================================================
# Pelote Network to Tabular Conversion Functions
# =============================================================================
#
# Functions able to convert networkx to various tabular data formats.
#
from pelote.types import AnyGraph
from pelote.compat import requires_pandas, pd


@requires_pandas()
def to_nodes_dataframe(graph: AnyGraph) -> pd.DataFrame:
    test = "ok"
