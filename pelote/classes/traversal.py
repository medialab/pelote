# =============================================================================
# Pelote DFS Stack Class
# =============================================================================
#
from collections import deque


class DFSStack:
    """
    Specialized stack structure tailored to perform memory-efficient DFS
    traversal in graphs.
    """

    def __init__(self, graph):
        self.__graph = graph
        self.__stack = []
        self.__seen = set()

    def __len__(self) -> int:
        return len(self.__stack)

    def __contains__(self, node) -> bool:
        return node in self.__seen

    def has_already_seen_everything(self) -> bool:
        return len(self.__seen) == len(self.__graph)

    def nodes_yet_unseen(self):
        for node in self.__graph:
            if len(self.__seen) == len(self.__graph):
                break

            if node in self.__seen:
                continue

            yield node

    def append(self, node, item=None) -> bool:
        size_before = len(self.__seen)

        self.__seen.add(node)

        if size_before == len(self.__seen):
            return False

        self.__stack.append(node if item is None else item)

        return True

    def pop(self):
        return self.__stack.pop()


class BFSQueue:
    """
    Specialized queue structure tailored to perform memory-efficient BFS
    traversal in graphs.
    """

    def __init__(self, graph):
        self.__graph = graph
        self.__queue = deque()
        self.__seen = set()

    def __len__(self) -> int:
        return len(self.__queue)

    def __contains__(self, node) -> bool:
        return node in self.__seen

    def has_already_seen_everything(self) -> bool:
        return len(self.__seen) == len(self.__graph)

    def nodes_yet_unseen(self):
        for node in self.__graph:
            if len(self.__seen) == len(self.__graph):
                break

            if node in self.__seen:
                continue

            yield node

    def append(self, node, item=None) -> bool:
        size_before = len(self.__seen)

        self.__seen.add(node)

        if size_before == len(self.__seen):
            return False

        self.__queue.append(node if item is None else item)

        return True

    def popleft(self):
        return self.__queue.popleft()
