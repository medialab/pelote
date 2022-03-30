# =============================================================================
# Pelote Sparsification Utilities
# =============================================================================
#
from pelote.types import AnyGraph
from pelote.graph import check_graph, filter_edges


class Sparsifier(object):
    def _get_edge_predicate(self):
        raise NotImplementedError

    def filter(self, graph: AnyGraph) -> AnyGraph:
        check_graph(graph)

        edge_predicate = self._get_edge_predicate()
        return filter_edges(graph, edge_predicate)

    def __call__(self, graph: AnyGraph) -> AnyGraph:
        return self.filter(graph)
