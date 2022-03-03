# =============================================================================
# Pelote Tabular to Network Conversion Functions
# =============================================================================
#
# Functions able to convert tabular data to networkx graphs.
#
import networkx as nx

from pelote.utils import IncrementalId
from pelote.shim import is_dataframe
from pelote.types import AnyGraph, Tabular


def to_bipartite_graph(
    table: Tabular,
    first_part_col: str,
    second_part_col: str,
    *,
    part_attr: str = "part",
    weight_attr: str = "weight",
    disjoint_keys: bool = False
) -> AnyGraph:
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
            node_attr = {part_attr: first_part_col, "label": str(label1)}
            graph.add_node(n1, **node_attr)

        if n2 not in graph:
            node_attr = {part_attr: second_part_col, "label": str(label2)}
            graph.add_node(n2, **node_attr)

        if graph.has_edge(n1, n2):
            graph[n1][n2][weight_attr] += 1
        else:
            edge_attr = {weight_attr: 1}
            graph.add_edge(n1, n2, **edge_attr)

    return graph
