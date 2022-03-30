# =============================================================================
# Pelote Tabular to Network Conversion Functions
# =============================================================================
#
# Functions able to convert tabular data to networkx graphs.
#
import networkx as nx
from typing import (
    Sequence,
    Union,
    Callable,
    Dict,
    Tuple,
    Any,
    Optional,
    Hashable,
    Iterable,
)

from pelote.utils import IncrementalIdRegister, check_node_exists
from pelote.shim import is_dataframe
from pelote.types import AnyGraph, Tabular, Indexable

RowDataSpec = Union[Sequence[Hashable], Callable[[Indexable], Dict[Any, Any]]]


def collect_row_data(spec: RowDataSpec, row: Indexable) -> Dict[Any, Any]:
    if callable(spec):
        attr = spec(row)

        if not isinstance(attr, dict):
            raise TypeError(
                "row data collection should return a dict but returned %s instead"
                % type(attr).__name__
            )

        return attr

    return {k: row[k] for k in spec}


def table_to_bipartite_graph(
    table: Tabular,
    first_part_col: Hashable,
    second_part_col: Hashable,
    *,
    node_part_attr: str = "part",
    edge_weight_attr: str = "weight",
    first_part_data: Optional[RowDataSpec] = None,
    second_part_data: Optional[RowDataSpec] = None,
    first_part_name: Optional[Hashable] = None,
    second_part_name: Optional[Hashable] = None,
    disjoint_keys: bool = False,
) -> AnyGraph:
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
        first_part_data (Sequence or Callable, optional): sequence (i.e. list, tuple etc.)
            of column from rows to keep as node attributes for the graph's first part.
            Can also be a function returning a dict of those attributes.
            Note that the first row containing a given node will take precedence over
            subsequent ones regarding data to include.
            Defaults to None.
        second_part_data (Sequence or Callable, optional): sequence (i.e. list, tuple etc.)
            of column from rows to keep as node attributes for the graph's second part.
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

    if is_dataframe(table):
        table = (row for _, row in table.iterrows())

    graph = nx.Graph()
    node_id = IncrementalIdRegister[Tuple[Hashable, Any]]()

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
    edge_table: Tabular,
    edge_source_col: Hashable,
    edge_target_col: Hashable,
    edge_weight_col: Optional[Hashable],
    graph: AnyGraph = nx.Graph(),
    nodes_exist: bool = False,
) -> AnyGraph:
    if edge_weight_col:
        if nodes_exist:
            graph.add_weighted_edges_from(
                (
                    check_node_exists(graph, row[edge_source_col]),
                    check_node_exists(graph, row[edge_target_col]),
                    row[edge_weight_col],
                )
                for row in edge_table
            )
        else:
            graph.add_weighted_edges_from(
                (row[edge_source_col], row[edge_target_col], row[edge_weight_col])
                for row in edge_table
            )
    else:
        if nodes_exist:
            graph.add_edges_from(
                (
                    check_node_exists(graph, row[edge_source_col]),
                    check_node_exists(graph, row[edge_target_col]),
                )
                for row in edge_table
            )
        else:
            graph.add_edges_from(
                (row[edge_source_col], row[edge_target_col]) for row in edge_table
            )
    return graph


def edges_table_to_graph(
    edge_table: Tabular,
    edge_source_col: Hashable = "source",
    edge_target_col: Hashable = "target",
    *,
    edge_weight_col: Optional[Hashable] = None,
) -> AnyGraph:
    """
    Function creating a bipartite graph from the given tabular data.

    Args:
        table (Iterable[Indexable] or pd.DataFrame): input tabular data. It can
            be a large variety of things as long as it is 1. iterable and 2.
            yields indexable values such as dicts or lists. This can for instance
            be a list of dicts, a csv.DictReader stream etc. It also supports
            pandas DataFrame if the library is installed.

    Returns:
        nx.AnyGraph: the resulting graph.
    """

    if is_dataframe(edge_table):
        edge_table = (row for _, row in edge_table.iterrows())

    return _edges_table_to_graph(
        edge_table, edge_source_col, edge_target_col, edge_weight_col
    )


def tables_to_graph(
    node_table: Tabular,
    edge_table: Tabular,
    node_col: Hashable = "key",
    edge_source_col: Hashable = "source",
    edge_target_col: Hashable = "target",
    *,
    edge_weight_col: Optional[Hashable] = None,
    node_data: Iterable[Hashable] = [],
    nodes_exist: bool = True,
) -> AnyGraph:
    """
    Function creating a bipartite graph from the given tabular data.

    Args:
        table (Iterable[Indexable] or pd.DataFrame): input tabular data. It can
            be a large variety of things as long as it is 1. iterable and 2.
            yields indexable values such as dicts or lists. This can for instance
            be a list of dicts, a csv.DictReader stream etc. It also supports
            pandas DataFrame if the library is installed.

    Returns:
        nx.AnyGraph: the resulting graph.
    """

    if is_dataframe(edge_table):
        edge_table = (row for _, row in edge_table.iterrows())

    if is_dataframe(node_table):
        node_table = (row for _, row in node_table.iterrows())

    graph = nx.Graph()

    graph.add_nodes_from(
        (
            row[node_col],
            {attr: row[attr] for attr in node_data},
        )
        for row in node_table
    )

    return _edges_table_to_graph(
        edge_table,
        edge_source_col,
        edge_target_col,
        edge_weight_col,
        graph=graph,
        nodes_exist=nodes_exist,
    )
