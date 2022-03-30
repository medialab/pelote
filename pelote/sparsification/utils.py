# =============================================================================
# Pelote Sparsification Utilities
# =============================================================================
#
from typing import Generator, Tuple, Any

from pelote.types import AnyGraph, Attributes
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

    def relevant_edges(
        self, graph: AnyGraph
    ) -> Generator[Tuple[Any, Any, Attributes], None, None]:
        edge_predicate = self._get_edge_predicate()

        for u, v, a in graph.edges.data():
            if edge_predicate(u, v, a):
                yield u, v, a

    def redundant_edges(
        self, graph: AnyGraph
    ) -> Generator[Tuple[Any, Any, Attributes], None, None]:
        edge_predicate = self._get_edge_predicate()

        for u, v, a in graph.edges.data():
            if not edge_predicate(u, v, a):
                yield u, v, a
