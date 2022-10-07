# =============================================================================
# Pelote Union Find Unit Tests
# =============================================================================
from pelote.classes import UnionFind


class TestUnionFind(object):
    def test_basics(self):
        u = UnionFind(5)

        assert u.capacity == 5

        assert len(u) == 5

        for i in range(len(u)):
            assert u.cardinality(i) == 1

        u.union(0, 1)

        assert u.are_in_same_set(0, 1)
        assert not u.are_in_same_set(1, 2)
        assert len(u) == 4
        assert u.cardinality(0) == 2
        assert u.cardinality(1) == 2
        assert u.cardinality(3) == 1

        # noop
        u.union(1, 0)

        assert u.are_in_same_set(0, 1)
        assert not u.are_in_same_set(1, 2)
        assert len(u) == 4

        u.union(1, 2)
        u.union(4, 3)
        u.union(3, 2)

        assert len(u) == 1
        assert u.are_in_same_set(2, 1)
        assert u.are_in_same_set(4, 1)

        for i in range(len(u)):
            assert u.cardinality(i) == 5

        u.clear()

        assert len(u) == 5
        assert not u.are_in_same_set(0, 1)
