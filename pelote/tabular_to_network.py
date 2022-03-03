# =============================================================================
# Pelote Tabular to Network Conversion Functions
# =============================================================================
#
# Functions able to convert tabular data to networkx graphs.
#
import networkx as nx

from pelote.utils import IncrementalId
from pelote.shim import is_dataframe
from pelote.types import AnyGraph, Tabular, GenericKey


def to_bipartite_graph(
    table: Tabular,
    first_part_col: GenericKey,
    second_part_col: GenericKey,
    *,
    node_part_attr: str = "part",
    edge_weight_attr: str = "weight",
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
        disjoint_keys (bool, optional): set this to True as an optimization
            mechanism if you know your part keys are disjoint, i.e. if no
            value for `first_part_col` can also be found in `second_part_col`.
            If you enable this option wrongly, the result can be incorrect.
            Defaults to False.
    """

    if first_part_col == second_part_col:
        raise TypeError("first_part_col and second_part_col must be different")

    if is_dataframe(table):
        table = (row for _, row in table.iterrows())

    graph = nx.Graph()
    node_id = IncrementalId()

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
            graph.add_node(n1, **node_attr)

        if n2 not in graph:
            node_attr = {node_part_attr: second_part_col, "label": str(label2)}
            graph.add_node(n2, **node_attr)

        if graph.has_edge(n1, n2):
            graph[n1][n2][edge_weight_attr] += 1
        else:
            edge_attr = {edge_weight_attr: 1}
            graph.add_edge(n1, n2, **edge_attr)

    return graph
