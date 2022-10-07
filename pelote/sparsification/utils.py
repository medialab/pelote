# =============================================================================
# Pelote Sparsification Utilities
# =============================================================================
#
import networkx as nx

from pelote.graph import check_graph, union_of_maximum_spanning_trees


def decorate_predicate_factory_with_umst(predicate_factory):
    def decorated_factory(graph):
        predicate = predicate_factory(graph)
        umst = set((u, v) for u, v, _ in union_of_maximum_spanning_trees(graph))

        def decorated_predicate(u, v, a):
            return predicate(u, v, a) or (u, v) in umst

        return decorated_predicate

    return decorated_factory


class Sparsifier(object):
    def __init__(
        self,
        edge_predicate_factory=None,
        relevant_edges_generator=None,
        redundant_edges_generator=None,
        keep_connected=False,
    ):

        if (
            edge_predicate_factory is None
            and relevant_edges_generator is None
            and redundant_edges_generator is None
        ):
            raise TypeError(
                "Sparsifier implementation cannot work without at least a edge_predicate_factory, relevant_edges_generator or a redundant_edges_generator"
            )

        if relevant_edges_generator is None:

            if not edge_predicate_factory:

                def edge_predicate_factory(graph):
                    redundant_edges = set()

                    for u, v, _ in redundant_edges_generator(graph):
                        if not graph.is_directed() and u > v:
                            u, v = v, u

                        redundant_edges.add((u, v))

                    def predicate(u, v, _):
                        if not graph.is_directed() and u > v:
                            u, v = v, u

                        return (u, v) not in redundant_edges

                    return predicate

            def relevant_edges_generator(graph):
                edge_predicate = edge_predicate_factory(graph)

                for u, v, a in graph.edges.data():
                    if edge_predicate(u, v, a):
                        yield u, v, a

        if redundant_edges_generator is None:

            if not edge_predicate_factory:

                def edge_predicate_factory(graph):
                    relevant_edges = set()

                    for u, v, _ in relevant_edges_generator(graph):
                        if not graph.is_directed() and u > v:
                            u, v = v, u

                        relevant_edges.add((u, v))

                    def predicate(u, v, _):
                        if not graph.is_directed() and u > v:
                            u, v = v, u

                        return (u, v) in relevant_edges

                    return predicate

            def redundant_edges_generator(graph):
                edge_predicate = edge_predicate_factory(graph)

                for u, v, a in graph.edges.data():
                    if not edge_predicate(u, v, a):
                        yield u, v, a

        if keep_connected:
            edge_predicate_factory = decorate_predicate_factory_with_umst(
                edge_predicate_factory
            )

        self.edge_predicate_factory = edge_predicate_factory
        self.relevant_edges_generator = relevant_edges_generator
        self.redundant_edges_generator = redundant_edges_generator

    def filter(self, graph):
        check_graph(graph)

        filtered = nx.create_empty_copy(graph)

        for u, v, a in self.relevant_edges_generator(graph):
            filtered.add_edge(u, v, **a)

        return filtered

    def remove(self, graph):
        check_graph(graph)

        graph.remove_edges_from(list(self.redundant_edges(graph)))

    def __call__(self, graph):
        return self.filter(graph)

    def relevant_edges(self, graph):
        check_graph(graph)

        return self.relevant_edges_generator(graph)

    def redundant_edges(self, graph):
        check_graph(graph)

        return self.redundant_edges_generator(graph)

    def flag_relevant_edges(self, graph, attr="relevant", full=False):
        if not full:
            for _u, _v, a in self.relevant_edges(graph):
                a[attr] = True
        else:
            edge_predicate = self.edge_predicate_factory(graph)

            for u, v, a in graph.edges.data():
                a[attr] = edge_predicate(u, v, a)

    def flag_redundant_edges(self, graph, attr="redundant", full=False):
        if not full:
            for _u, _v, a in self.redundant_edges(graph):
                a[attr] = True
        else:
            edge_predicate = self.edge_predicate_factory(graph)

            for u, v, a in graph.edges.data():
                a[attr] = not edge_predicate(u, v, a)
