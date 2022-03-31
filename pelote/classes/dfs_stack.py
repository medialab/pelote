# =============================================================================
# Pelote DFS Stack Class
# =============================================================================
#
from typing import Generic, List, Set, TypeVar, Optional

from pelote.types import AnyGraph

V = TypeVar("V")


class DFSStack(Generic[V]):
    """
    Specialized stack structure tailored to perform memory-efficient DFS
    traversal in graphs.
    """

    def __init__(self, graph: AnyGraph):
        self.__order = graph.order()
        self.__stack: List[V] = []
        self.__seen: Set[V] = set()

    def __len__(self) -> int:
        return len(self.__stack)

    def __contains__(self, node: V) -> bool:
        return node in self.__seen

    def has_seen_everything(self) -> bool:
        return len(self.__seen) == self.__order

    def append(self, node: V) -> bool:
        size_before = len(self.__seen)

        self.__seen.add(node)

        if size_before == len(self.__seen):
            return False

        self.__stack.append(node)

        return True

    def pop(self) -> Optional[V]:
        if len(self.__stack) == 0:
            return None

        return self.__stack.pop()
