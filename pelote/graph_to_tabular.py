# =============================================================================
# Pelote Network to Tabular Conversion Functions
# =============================================================================
#
# Functions able to convert networkx graphs to various tabular data formats.
#
from collections.abc import Mapping, Iterable

from pelote.shim import pd, check_pandas
from pelote.graph import check_graph


def graph_to_nodes_dataframe(graph, node_key_col: str = "key") -> "pd.DataFrame":
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
        from pelote import graph_to_nodes_dataframe

        df = graph_to_nodes_dataframe(graph)
    """

    check_pandas()
    check_graph(graph)

    if node_key_col is None:

        def raw_data():
            for _, a in graph.nodes(data=True):
                yield a

        return pd.DataFrame(data=raw_data(), index=graph.nodes)

    else:

        def data_with_key():
            for n, a in graph.nodes(data=True):
                r = {node_key_col: n}
                r.update(a)
                yield r

        return pd.DataFrame(data=data_with_key())


def graph_to_edges_dataframe(
    graph,
    *,
    edge_source_col: str = "source",
    edge_target_col: str = "target",
    source_node_data=None,
    target_node_data=None
):
    """
    Function converting the given networkx graph into a pandas DataFrame of
    its edges.

    Args:
        nx.AnyGraph: a networkx graph instance
        edge_source_col (str, optional): name of the DataFrame column containing
            the edge source. Defaults to "source".
        edge_target_col (str, optional): name of the DataFrame column containing
            the edge target. Defaults to "target".
        source_node_data (Iterable or Mapping, optional): iterable of attribute names
            or mapping from attribute names to column name to be used to add
            columns to the resulting dataframe based on source node data.
            Defaults to None.
        target_node_data (Iterable or Mapping, optional): iterable of attribute names
            or mapping from attribute names to column name to be used to add
            columns to the resulting dataframe based on target node data.
            Defaults to None.

    Returns:
        pd.DataFrame: A pandas DataFrame
    """

    check_pandas()
    check_graph(graph)

    if source_node_data is not None:
        if not isinstance(source_node_data, (Mapping, Iterable)):
            raise TypeError(
                "source_node_data should be an iterable of keys or a mapping of keys to extract from nodes"
            )

        if not isinstance(source_node_data, Mapping):
            source_node_data = {k: k for k in source_node_data}

    if target_node_data is not None:
        if not isinstance(target_node_data, (Mapping, Iterable)):
            raise TypeError(
                "target_node_data should be an iterable of keys or a mapping of keys to extract from nodes"
            )

        if not isinstance(target_node_data, Mapping):
            target_node_data = {k: k for k in target_node_data}

    def data():
        for source, target, a in graph.edges(data=True):
            r = {edge_source_col: source, edge_target_col: target}
            r.update(a)

            if source_node_data is not None:
                node_data = graph.nodes[source]

                for attr_name, col_name in source_node_data.items():
                    r[col_name] = node_data.get(attr_name)

            if target_node_data is not None:
                node_data = graph.nodes[target]

                for attr_name, col_name in target_node_data.items():
                    r[col_name] = node_data.get(attr_name)

            yield r

    return pd.DataFrame(data=data())


def graph_to_dataframes(
    graph,
    *,
    node_key_col: str = "key",
    edge_source_col: str = "source",
    edge_target_col: str = "target",
    source_node_data=None,
    target_node_data=None
):
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
        source_node_data (Iterable or Mapping, optional): iterable of attribute names
            or mapping from attribute names to column name to be used to add
            columns to the edge dataframe based on source node data.
            Defaults to None.
        target_node_data (Iterable or Mapping, optional): iterable of attribute names
            or mapping from attribute names to column name to be used to add
            columns to the edge dataframe based on target node data.
            Defaults to None.

    Returns:
        (pd.DataFrame, pd.DataFrame)
    """
    nodes = graph_to_nodes_dataframe(graph, node_key_col=node_key_col)
    edges = graph_to_edges_dataframe(
        graph,
        edge_source_col=edge_source_col,
        edge_target_col=edge_target_col,
        source_node_data=source_node_data,
        target_node_data=target_node_data,
    )

    return nodes, edges
