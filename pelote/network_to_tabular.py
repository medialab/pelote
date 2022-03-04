# =============================================================================
# Pelote Network to Tabular Conversion Functions
# =============================================================================
#
# Functions able to convert networkx graphs to various tabular data formats.
#
from typing import Optional, Tuple

from pelote.types import AnyGraph
from pelote.shim import pd, check_pandas
from pelote.graph import check_graph


def to_nodes_dataframe(
    graph: AnyGraph, node_key_col: Optional[str] = "key"
) -> "pd.DataFrame":
    """
    Function converting the given networkx graph into a pandas DataFrame of
    its nodes.

    Args:
        nx.AnyGraph: a networkx graph instance
        node_key_col (str, optional): name of the DataFrame column containing
            the node keys. If None, the node keys will be used as the DataFrame
            index. Defaults to "key".

    Returns:
        pd.DataFrame: A pandas DataFrame

    Example:
        from pelote import to_nodes_dataframe

        df = to_nodes_dataframe(graph)
    """

    check_pandas()
    check_graph(graph)

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


def to_edges_dataframe(
    graph: AnyGraph,
    *,
    edge_source_col: Optional[str] = "source",
    edge_target_col: Optional[str] = "target"
) -> "pd.DataFrame":
    """
    Function converting the given networkx graph into a pandas DataFrame of
    its edges.

    Args:
        nx.AnyGraph: a networkx graph instance
        edge_source_col (str, optional): name of the DataFrame column containing
            the edge source. Defaults to "source".
        edge_target_col (str, optional): name of the DataFrame column containing
            the edge target. Defaults to "target".

    Returns:
        pd.DataFrame: A pandas DataFrame
    """

    check_pandas()
    check_graph(graph)

    def data():
        for source, target, a in graph.edges(data=True):
            r = {edge_source_col: source, edge_target_col: target}
            r.update(a)
            yield r

    return pd.DataFrame(data=data())


def to_dataframes(
    graph: AnyGraph,
    *,
    node_key_col: Optional[str] = "key",
    edge_source_col: Optional[str] = "source",
    edge_target_col: Optional[str] = "target"
) -> Tuple["pd.DataFrame", "pd.DataFrame"]:
    """
    Function converting the given networkx graph into two pandas DataFrames:
    one for its nodes, one for its edges.

    Args:
        nx.AnyGraph: a networkx graph instance
        node_key_col (str, optional): name of the node DataFrame column containing
            the node keys. If None, the node keys will be used as the DataFrame
            index. Defaults to "key".
        edge_source_col (str, optional): name of the edge DataFrame column containing
            the edge source. Defaults to "source".
        edge_target_col (str, optional): name of the edge DataFrame column containing
            the edge target. Defaults to "target".

    Returns:
        (pd.DataFrame, pd.DataFrame)
    """
    nodes = to_nodes_dataframe(graph, node_key_col=node_key_col)
    edges = to_edges_dataframe(
        graph, edge_source_col=edge_source_col, edge_target_col=edge_target_col
    )

    return nodes, edges
