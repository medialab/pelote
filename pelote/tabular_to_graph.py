# =============================================================================
# Pelote Tabular to Network Conversion Functions
# =============================================================================
#
# Functions able to convert tabular data to networkx graphs.
#
import networkx as nx
from typing import Sequence, Union, Callable, Dict, Tuple, Any, Optional

from pelote.utils import IncrementalIdRegister
from pelote.shim import is_dataframe
from pelote.types import AnyGraph, Tabular, GenericKey, Indexable

RowDataSpec = Union[Sequence[GenericKey], Callable[[Indexable], Dict[Any, Any]]]


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
    first_part_col: GenericKey,
    second_part_col: GenericKey,
    *,
    node_part_attr: str = "part",
    edge_weight_attr: str = "weight",
    first_part_data: Optional[RowDataSpec] = None,
    second_part_data: Optional[RowDataSpec] = None,
    disjoint_keys: bool = False
) -> AnyGraph:
    """
    Function creating a bipartite graph from the given tabular data.

    Args:
        table (Iterable[Indexable] or pd.DataFrame): input tabular data. It can
            be a large variety of things as long as it is 1. iterable and 2.
            yields indexable values such as dicts or lists. This can for instance
            be a list of dicts, a csv.DictReader stream etc. It also supports
            pandas DataFrame if the library is installed.
        first_part_col (str or int): the name of the column containing the
            value representing a node in the resulting graph's first part.
            It could be the index if your rows are lists or a key if your rows
            are dicts instead.
        second_par_col (str or int): the name of the column containing the
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

    if is_dataframe(table):
        table = (row for _, row in table.iterrows())

    graph = nx.Graph()
    node_id = IncrementalIdRegister[Tuple[GenericKey, Any]]()

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
            node_attr = {node_part_attr: first_part_col, "label": str(label1)}

            if first_part_data:
                node_attr.update(collect_row_data(first_part_data, row))

            graph.add_node(n1, **node_attr)

        if n2 not in graph:
            node_attr = {node_part_attr: second_part_col, "label": str(label2)}

            if second_part_data:
                node_attr.update(collect_row_data(second_part_data, row))

            graph.add_node(n2, **node_attr)

        if graph.has_edge(n1, n2):
            graph[n1][n2][edge_weight_attr] += 1
        else:
            edge_attr = {edge_weight_attr: 1}
            graph.add_edge(n1, n2, **edge_attr)

    return graph
