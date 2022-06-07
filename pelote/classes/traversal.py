# =============================================================================
# Pelote DFS Stack Class
# =============================================================================
#
from typing import Generic, List, Set, TypeVar, Generator, Deque, cast

from pelote.types import AnyGraph

K = TypeVar("K")
V = TypeVar("V")


class DFSStack(Generic[K, V]):
    """
    Specialized stack structure tailored to perform memory-efficient DFS
    traversal in graphs.
    """

    def __init__(self, graph: AnyGraph):
        self.__graph = graph
        self.__stack: List[V] = []
        self.__seen: Set[K] = set()

    def __len__(self) -> int:
        return len(self.__stack)

    def __contains__(self, node: K) -> bool:
        return node in self.__seen

    def has_already_seen_everything(self) -> bool:
        return len(self.__seen) == len(self.__graph)

    def nodes_yet_unseen(self) -> Generator[K, None, None]:
        for node in self.__graph:
            if len(self.__seen) == len(self.__graph):
                break

            if node in self.__seen:
                continue

            yield node

    def append(self, node: K) -> bool:
        size_before = len(self.__seen)

        self.__seen.add(node)

        if size_before == len(self.__seen):
            return False

        self.__stack.append(cast(V, node))

        return True

    def pop(self) -> V:
        return self.__stack.pop()


class BFSQueue(Generic[K, V]):
    """
    Specialized queue structure tailored to perform memory-efficient BFS
    traversal in graphs.
    """

    def __init__(self, graph: AnyGraph):
        self.__graph = graph
        self.__queue: Deque[V] = Deque()
        self.__seen: Set[K] = set()

    def __len__(self) -> int:
        return len(self.__queue)

    def __contains__(self, node: K) -> bool:
        return node in self.__seen

    def has_already_seen_everything(self) -> bool:
        return len(self.__seen) == len(self.__graph)

    def nodes_yet_unseen(self) -> Generator[K, None, None]:
        for node in self.__graph:
            if len(self.__seen) == len(self.__graph):
                break

            if node in self.__seen:
                continue

            yield node

    def append(self, node: K) -> bool:
        size_before = len(self.__seen)

        self.__seen.add(node)

        if size_before == len(self.__seen):
            return False

        self.__queue.append(cast(V, node))

        return True

    def append_with(self, node: K, item: V) -> bool:
        size_before = len(self.__seen)

        self.__seen.add(node)

        if size_before == len(self.__seen):
            return False

        self.__queue.append(item)

        return True

    def popleft(self) -> V:
        return self.__queue.popleft()
