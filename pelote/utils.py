# =============================================================================
# Pelote Utilities
# =============================================================================
#
# Miscellaneous utility functions used throughout the library.
#
from array import array
from itertools import repeat
from collections.abc import Iterable
from collections import Counter, defaultdict, OrderedDict, namedtuple

from pelote.shim import is_dataframe


def has_mixed_types(iterable) -> bool:
    iterator = iter(iterable)

    main_type = None

    for item in iterator:
        main_type = type(item)
        break

    for item in iterator:
        if type(item) is not main_type:
            return True

    return False


CONSTANT_TIME_LOOKUP = (set, frozenset, dict, Counter, defaultdict, OrderedDict)


def has_constant_time_lookup(v) -> bool:
    return isinstance(v, CONSTANT_TIME_LOOKUP)


def iterator_from_dataframe(table, columns=None):
    if is_dataframe(table):
        if columns is None:
            columns = table.columns
        return (
            dict(zip(columns, row))
            for row in zip(*(table[col].values for col in columns))
        )
    else:
        return table


Representation = namedtuple("Representation", ("max", "code"))

UINT_REPRESENTATIONS = [
    Representation(2**8 - 1, "B"),
    Representation(2**16 - 1, "H"),
    Representation(2**32 - 1, "L"),
    Representation(2**64 - 1, "Q"),
]


def uint_representation_for_max(upper_bound):
    for r in UINT_REPRESENTATIONS:
        if upper_bound <= r.max:
            return r

    raise TypeError("capacity is over 64 bits")


def uint_representation_for_capacity(capacity):
    return uint_representation_for_max(capacity - 1)


def counting_sort(items, *, key=None, reverse=False):
    # TODO: optimize some cases, precompute keys if needed and add possibility to give bounds
    if not isinstance(items, Iterable):
        raise TypeError("items should be an iterable")

    # 1. Computing bounds
    keys = []

    lower_bound = None
    upper_bound = None

    l = len(items)

    for item in items:
        k = item if key is None else key(item)
        keys.append(k)

        # if not isinstance(item, int) or k < 0:
        #     raise TypeError("sorted items should be int >= 0")

        if lower_bound is None or k < lower_bound:
            lower_bound = k

        if upper_bound is None or k > upper_bound:
            upper_bound = k

    span = upper_bound - lower_bound

    # 2. Counting
    counts = array(uint_representation_for_max(l).code, repeat(0, span + 1))

    for k in keys:
        j = k - lower_bound
        counts[j] += 1

    # 3. Cumulating
    for i in range(1, span + 1):
        counts[i] += counts[i - 1]

    # 4. Sorting
    output = [None] * l

    for k, item in zip(keys, items):
        j = k - lower_bound
        i = counts[j] - 1
        counts[j] = i

        if reverse:
            i = l - i - 1

        output[i] = item

    return output


def fast_intersection_size(A, B) -> int:
    if len(A) > len(B):
        A, B = B, A

    if not A:
        return 0

    if A is B:
        return len(A)

    I = 0

    for item in A:
        if item in B:
            I += 1

    return I
