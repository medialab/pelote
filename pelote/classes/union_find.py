# =============================================================================
# Pelote Union Find Classes
# =============================================================================
#
from array import array
from itertools import repeat

from pelote.utils import uint_representation_for_capacity


class UnionFind(object):
    def __init__(self, capacity: int) -> None:
        self.__count = capacity
        self.capacity = capacity
        self.allocate(capacity)

    def __repr__(self):
        return "<UnionFind representation={representation!r} capacity={capacity!r} count={count!r}>".format(
            representation=self.representation.code,
            capacity=self.capacity,
            count=self.__count,
        )

    def __len__(self):
        return self.__count

    def allocate(self, capacity):
        self.capacity = capacity
        self.representation = uint_representation_for_capacity(capacity)

        self.parents = array(self.representation.code, range(capacity))
        self.ranks = array(self.representation.code, repeat(0, capacity))
        self.cardinalities = array(self.representation.code, repeat(1, capacity))

    def clear(self):
        self.__count = self.capacity

        for i in range(self.capacity):
            self.parents[i] = i
            self.ranks[i] = 0
            self.cardinalities[i] = 1

    def find(self, x):
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

    def cardinality(self, x):
        return self.cardinalities[self.find(x)]

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)

        parents = self.parents
        ranks = self.ranks
        cardinalities = self.cardinalities

        # x & y are already in the same set
        if x_root == y_root:
            return

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

    def are_in_same_set(self, x, y):
        return self.find(x) == self.find(y)
