# =============================================================================
# Pelote Utilities Unit Tests
# =============================================================================
import networkx as nx

from pelote.utils import (
    has_mixed_types,
    uint_representation_for_capacity,
    counting_sort,
)


class TestUtils(object):
    def test_has_mixed_types(self):
        g = nx.Graph()

        assert not has_mixed_types(g)

        g.add_node(1)

        assert not has_mixed_types(g)

        g.add_node("5")

        assert has_mixed_types(g)

    def test_uint_representation_for_capacity(self):
        assert uint_representation_for_capacity(34).code == "B"
        assert uint_representation_for_capacity(345).code == "H"
        assert uint_representation_for_capacity(486462).code == "L"
        assert uint_representation_for_capacity(847586358646854).code == "Q"

    def test_counting_sort(self):
        numbers = [0, 4, 3, 1, 0, 2, 4, 5, 9]
        expected = [0, 0, 1, 2, 3, 4, 4, 5, 9]

        assert counting_sort(numbers) == expected
        assert counting_sort(numbers, reverse=True) == list(reversed(expected))
        assert counting_sort(numbers, key=lambda x: 10 - x) == list(reversed(expected))

        numbers = [4, 5, 6, 7]

        assert counting_sort(numbers) == numbers

        numbers = [18, 54, 5, 16]

        assert counting_sort(numbers) == [5, 16, 18, 54]
