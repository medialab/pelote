# =============================================================================
# Pelote Tabular to Network Conversion Functions
# =============================================================================
#
# Functions able to convert tabular data to networkx graphs.
#
import networkx as nx
from collections.abc import Sequence, Mapping

from pelote.utils import iterator_from_dataframe
from pelote.classes import IncrementalIdRegister
from pelote.graph import check_node_exists


def collect_row_data(spec, row):
    if callable(spec):
        attr = spec(row)

        if not isinstance(attr, dict):
            raise TypeError(
                "row data collection should return a dict but returned %s instead"
                % type(attr).__name__
            )

        return attr

    if isinstance(spec, Mapping):
        attr = {}

        for col_name, attr_name in spec.items():
            v = row.get(col_name)

            if v is not None:
                attr[attr_name] = v

        return attr

    if isinstance(spec, Sequence):
        attr = {}

        for col_name in spec:
            v = row.get(col_name)

            if v is not None:
                attr[col_name] = v

        return attr

    raise TypeError(
        "could not collect part data. expecting a callable, a mapping or a sequence"
    )


def table_to_bipartite_graph(
    table,
    first_part_col,
    second_part_col,
    *,
    node_part_attr: str = "part",
    edge_weight_attr: str = "weight",
    first_part_data=None,
    second_part_data=None,
    first_part_name=None,
    second_part_name=None,
    disjoint_keys: bool = False,
):
    """
    Function creating a bipartite graph from the given tabular data.

    Args:
        table (Iterable[Indexable] or pd.DataFrame): input tabular data. It can
            be a large variety of things as long as it is 1. iterable and 2.
            yields indexable values such as dicts or lists. This can for instance
            be a list of dicts, a csv.DictReader stream etc. It also supports
            pandas DataFrame if the library is installed.
        first_part_col (Hashable): the name of the column containing the
            value representing a node in the resulting graph's first part.
            It could be the index if your rows are lists or a key if your rows
            are dicts instead.
        second_par_col (Hashable): the name of the column containing the
            value representing a node in the resulting graph's second part.
            It could be the index if your rows are lists or a key if your rows
            are dicts instead.
        node_part_attr (str, optional): name of the node attribute containing
            the part it belongs to. Defaults to "part".
        edge_weight_attr (str, optional): name of the edge attribute containing
            its weight, i.e. the number of times it was found in the table.
            Defaults to "weight".
        first_part_data (Sequence or Callable or Mapping, optional): sequence (i.e. list, tuple etc.)
            of column from rows to keep as node attributes for the graph's first part.
            Can also be a mapping (i.e. dict) from row column to node attribute
            name to create.
            Can also be a function returning a dict of those attributes.
            Note that the first row containing a given node will take precedence over
            subsequent ones regarding data to include.
            Defaults to None.
        second_part_data (Sequence or Callable or Mapping, optional): sequence (i.e. list, tuple etc.)
            of column from rows to keep as node attributes for the graph's second part.
            Can also be a mapping (i.e. dict) from row column to node attribute
            name to create.
            Can also be a function returning a dict of those attributes.
            Note that the first row containing a given node will take precedence over
            subsequent ones regarding data to include.
            Defaults to None.
        first_part_name (Hashable, optional): can be given to rename the first part.
            Defaults to None.
        second_part_name (Hashable, optional): can be given to rename the second part.
            to display as graph's second part's name.
            Defaults to None.
        disjoint_keys (bool, optional): set this to True as an optimization
            mechanism if you know your part keys are disjoint, i.e. if no
            value for `first_part_col` can also be found in `second_part_col`.
            If you enable this option wrongly, the result can be incorrect.
            Defaults to False.

    Returns:
        nx.AnyGraph: the bipartite graph.
    """

    if first_part_col == second_part_col:
        raise TypeError("first_part_col and second_part_col must be different")

    if first_part_name is None:
        first_part_name = first_part_col

    if second_part_name is None:
        second_part_name = second_part_col

    table = iterator_from_dataframe(table)

    graph = nx.Graph()
    node_id = IncrementalIdRegister()

    for i, row in enumerate(table):
        try:
            label1 = row[first_part_col]
            label2 = row[second_part_col]
        except (IndexError, KeyError):
            raise TypeError(
                'row %i lacks the "%s" or the "%s" value'
                % (i, first_part_col, second_part_col)
            )

        if disjoint_keys:
            n1 = label1
            n2 = label2
        else:
            # TODO: possibility to save lookups for sorted data
            n1 = node_id[first_part_col, label1]
            n2 = node_id[second_part_col, label2]

        if n1 not in graph:
            node_attr = {node_part_attr: first_part_name, "label": str(label1)}

            if first_part_data:
                node_attr.update(collect_row_data(first_part_data, row))

            graph.add_node(n1, **node_attr)

        if n2 not in graph:
            node_attr = {node_part_attr: second_part_name, "label": str(label2)}

            if second_part_data:
                node_attr.update(collect_row_data(second_part_data, row))

            graph.add_node(n2, **node_attr)

        if graph.has_edge(n1, n2):
            graph[n1][n2][edge_weight_attr] += 1
        else:
            edge_attr = {edge_weight_attr: 1}
            graph.add_edge(n1, n2, **edge_attr)

    return graph


def _edges_table_to_graph(
    graph,
    edge_table,
    edge_source_col,
    edge_target_col,
    edge_data,
    count_rows_as_weight: bool,
    edge_weight_attr: str,
    add_missing_nodes: bool = True,
):

    for row in edge_table:

        n1, n2 = row[edge_source_col], row[edge_target_col]

        if not add_missing_nodes:
            n1 = check_node_exists(graph, row[edge_source_col])
            n2 = check_node_exists(graph, row[edge_target_col])

        data = {str(attr): row[attr] for attr in edge_data}

        if count_rows_as_weight:
            if graph.has_edge(n1, n2):
                graph[n1][n2][edge_weight_attr] += 1
                continue
            else:
                data[edge_weight_attr] = 1
        graph.add_edge(n1, n2, **data)

    return graph


def edges_table_to_graph(
    edge_table,
    edge_source_col="source",
    edge_target_col="target",
    *,
    edge_data=[],
    count_rows_as_weight: bool = False,
    edge_weight_attr: str = "weight",
    directed: bool = False,
):
    """
    Function creating a graph from a table of edges.

    Args:
        edges_table (Iterable[Indexable] or pd.DataFrame): input edges in tabular
            format. It can be a large variety of things as long as it is 1. iterable
            and 2. yields indexable values such as dicts or lists. This can for
            instance be a list of dicts, a csv.DictReader stream etc. It also supports
            pandas DataFrame if the library is installed.
        edge_source_col (Hashable, optional): the name of the column containing the edges' source
            nodes in the edges_table.
            Defaults to "source".
        edge_target_col (Hashable, optional): the name of the column containing the edges' target
            nodes in the edges_table.
            Defaults to "target".
        edge_data (Sequence, optional): sequence (i.e. list, tuple etc.) of columns' names
            from the edges_table to keep as edge attributes in the resulting graph, e.g. ["weight"].
            Defaults to [].
        count_rows_as_weight (bool, optional): set this to True to compute a weight
            attribute for each edge, corresponding to the number of times it was
            found in the table. The name of this attribute is defined by the
            `edge_weight_attr` parameter. If set to False, only the last occurrence of
            each edge will be kept in the graph.
            Defaults to False.
        edge_weight_attr (str, optional): name of the edge attribute containing
            its weight, i.e. the number of times it was found in the table, if
            `count_rows_as_weight` is set to True.
            Defaults to "weight".
        directed (bool, optional): whether the resulting graph must be directed.
            Defaults to False.

    Returns:
        nx.AnyGraph: the resulting graph.
    """

    edge_table = iterator_from_dataframe(
        edge_table, [edge_source_col, edge_target_col] + list(edge_data)
    )

    if directed:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    return _edges_table_to_graph(
        graph,
        edge_table,
        edge_source_col,
        edge_target_col,
        edge_data,
        count_rows_as_weight,
        edge_weight_attr,
    )


def tables_to_graph(
    nodes_table,
    edges_table,
    node_col="key",
    edge_source_col="source",
    edge_target_col="target",
    *,
    node_data=[],
    edge_data=[],
    count_rows_as_weight: bool = False,
    edge_weight_attr: str = "weight",
    add_missing_nodes: bool = False,
    directed: bool = False,
):
    """
    Function creating a graph from two tables: a table of nodes and a table of edges.

    Args:
        nodes_table (Iterable[Indexable] or pd.DataFrame): input nodes in tabular
            format. It can be a large variety of things as long as it is 1. iterable
            and 2. yields indexable values such as dicts or lists. This can for
            instance be a list of dicts, a csv.DictReader stream etc. It also supports
            pandas DataFrame if the library is installed.
        edges_table (Iterable[Indexable] or pd.DataFrame): input edges in tabular
            format.
        node_col (Hashable, optional): the name of the column containing the nodes in the nodes_table.
            It could be the index if your rows are lists or a key if your rows
            are dicts instead.
            Defaults to "key".
        edge_source_col (Hashable, optional): the name of the column containing the edges' source
            nodes in the edges_table.
            Defaults to "source".
        edge_target_col (Hashable, optional): the name of the column containing the edges' target
            nodes in the edges_table.
            Defaults to "target".
        node_data (Sequence, optional): sequence (i.e. list, tuple etc.)
            of columns' names from the nodes_table to keep as node attributes in the resulting graph.
            Defaults to [].
        edge_data (Sequence, optional): sequence (i.e. list, tuple etc.) of columns' names
            from the edges_table to keep as edge attributes in the resulting graph, e.g. ["weight"].
            Defaults to [].
        count_rows_as_weight (bool, optional): set this to True to compute a weight
            attribute for each edge, corresponding to the number of times it was
            found in the table. The name of this attribute is defined by the
            `edge_weight_attr` parameter. If set to False, only the last occurrence of
            each edge will be kept in the graph.
            Defaults to False.
        edge_weight_attr (str, optional): name of the edge attribute containing
            its weight, i.e. the number of times it was found in the table, if
            `count_rows_as_weight` is set to True.
            Defaults to "weight".
        add_missing_nodes (bool, optional): set this to True to check that the edges' sources and targets
            in the edges_table are all defined in the nodes_table.
            Defaults to True.
        directed (bool, optional): whether the resulting graph must be directed.
            Defaults to False.

    Returns:
        nx.AnyGraph: the resulting graph.

    Example:
        from pelote import tables_to_graph

        table_nodes = [
            {"name": "alice", "age": 50},
            {"name": "bob", "age": 12}
        ]

        table_edges = [
            {"source": "alice", "target": "bob", "weight": 0.8},
            {"source": "bob", "target": "alice", "weight": 0.2}
        ]

        g = tables_to_graph(
            table_nodes, table_edges, node_col="name", node_data=["age"], edge_data=["weight"], directed=True
        )
    """

    nodes_table = iterator_from_dataframe(nodes_table, [node_col] + list(node_data))

    edges_table = iterator_from_dataframe(
        edges_table, [edge_source_col, edge_target_col] + list(edge_data)
    )

    if directed:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    for row in nodes_table:
        graph.add_node(row[node_col], **{str(attr): row[attr] for attr in node_data})

    return _edges_table_to_graph(
        graph,
        edges_table,
        edge_source_col,
        edge_target_col,
        edge_data,
        count_rows_as_weight,
        edge_weight_attr,
        add_missing_nodes=add_missing_nodes,
    )
