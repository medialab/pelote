# =============================================================================
# Pelote Union Find Unit Tests
# =============================================================================
from pelote.classes import UnionFind, DisjointSet


class TestUnionFind(object):
    def test_basics(self):
        u = UnionFind(5)

        assert u.capacity == 5

        assert len(u) == 5

        for i in range(len(u)):
            assert u.cardinality(i) == 1

        assert u.union(0, 1)

        assert u.are_in_same_set(0, 1)
        assert not u.are_in_same_set(1, 2)
        assert len(u) == 4
        assert u.cardinality(0) == 2
        assert u.cardinality(1) == 2
        assert u.cardinality(3) == 1

        # noop
        assert not u.union(1, 0)

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


class TestDisjointSet(object):
    def test_basics(self):
        ds = DisjointSet(5)

        numbers = ["zero", "one", "two", "three", "four"]

        assert ds.capacity == 5

        assert len(ds) == 5

        for i in range(len(ds)):
            assert ds.cardinality(numbers[i]) == 1

        assert ds.union("zero", "one")

        assert ds.are_in_same_set("zero", "one")
        assert not ds.are_in_same_set("one", "two")
        assert len(ds) == 4
        assert ds.cardinality("zero") == 2
        assert ds.cardinality("one") == 2
        assert ds.cardinality("three") == 1

        # noop
        assert not ds.union("one", "zero")

        assert ds.are_in_same_set("zero", "one")
        assert not ds.are_in_same_set("one", "two")
        assert len(ds) == 4

        ds.union("one", "two")
        ds.union("four", "three")
        ds.union("three", "two")

        assert len(ds) == 1
        assert ds.are_in_same_set("two", "one")
        assert ds.are_in_same_set("four", "one")

        for i in range(len(ds)):
            assert ds.cardinality(numbers[i]) == 5

        ds.clear()

        assert len(ds) == 5
        assert not ds.are_in_same_set("zero", "one")
