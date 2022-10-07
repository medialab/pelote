# =============================================================================
# Pelote Union Find Classes
# =============================================================================
#
from array import array
from itertools import repeat

from pelote.classes import IncrementalIdRegister
from pelote.utils import uint_representation_for_capacity


class UnionFind(object):
    __slots__ = (
        "__count",
        "capacity",
        "representation",
        "parents",
        "ranks",
        "cardinalities",
    )

    def __init__(self, capacity: int) -> None:
        self.__count = capacity
        self.capacity = capacity
        self.allocate(capacity)

    def __repr__(self) -> str:
        return "<UnionFind representation={representation!r} capacity={capacity!r} count={count!r}>".format(
            representation=self.representation.code,
            capacity=self.capacity,
            count=self.__count,
        )

    def __len__(self) -> int:
        return self.__count

    def allocate(self, capacity: int) -> None:
        self.capacity = capacity
        self.representation = uint_representation_for_capacity(capacity)

        self.parents = array(self.representation.code, range(capacity))
        self.ranks = array(self.representation.code, repeat(0, capacity))
        self.cardinalities = array(self.representation.code, repeat(1, capacity))

    def clear(self) -> None:
        self.__count = self.capacity

        for i in range(self.capacity):
            self.parents[i] = i
            self.ranks[i] = 0
            self.cardinalities[i] = 1

    def find(self, x: int):
        y = x
        parents = self.parents

        while True:
            c = parents[y]

            if y == c:
                break

            y = c

        # Path compression trick
        while True:
            p = parents[x]

            if p == y:
                break

            x = p

        return y

    def cardinality(self, x: int) -> int:
        return self.cardinalities[self.find(x)]

    def union(self, x: int, y: int) -> bool:
        x_root = self.find(x)
        y_root = self.find(y)

        parents = self.parents
        ranks = self.ranks
        cardinalities = self.cardinalities

        # x & y are already in the same set
        if x_root == y_root:
            return False

        self.__count -= 1

        # x & y are not in the same set, we merge them
        x_rank = ranks[x]
        y_rank = ranks[y]

        if x_rank < y_rank:
            cardinalities[y_root] += cardinalities[x_root]
            parents[x_root] = y_root
        elif x_rank > y_rank:
            cardinalities[x_root] += cardinalities[y_root]
            parents[y_root] = x_root
        else:
            cardinalities[x_root] += cardinalities[y_root]
            parents[y_root] = x_root
            ranks[x_root] += 1

        return True

    def are_in_same_set(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


class DisjointSet(object):
    __slots__ = ("__union_find", "__register")

    def __init__(self, capacity: int):
        self.__union_find = UnionFind(capacity)
        self.__register = IncrementalIdRegister()

    def clear(self) -> None:
        self.__union_find.clear()
        self.__register.clear()

    @property
    def capacity(self) -> int:
        return self.__union_find.capacity

    def __len__(self) -> int:
        return len(self.__union_find)

    def find(self, x) -> int:
        x = self.__register[x]
        return self.__union_find.find(x)

    def union(self, x, y) -> bool:
        x = self.__register[x]
        y = self.__register[y]
        return self.__union_find.union(x, y)

    def cardinality(self, x) -> int:
        x = self.__register[x]
        return self.__union_find.cardinality(x)

    def are_in_same_set(self, x, y) -> bool:
        return self.find(x) == self.find(y)
