# =============================================================================
# Pelote Utilities
# =============================================================================
#
# Miscellaneous utility functions used throughout the library.
#
from collections import Counter, defaultdict, OrderedDict

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


UINT_REPRESENTATIONS = [
    (2**8 - 1, "B"),
    (2**16 - 1, "H"),
    (2**32 - 1, "L"),
    (2**64 - 1, "Q"),
]


def uint_representation_for_capacity(capacity):
    max_int = capacity - 1

    for max_representable, representation in UINT_REPRESENTATIONS:
        if max_int <= max_representable:
            return representation

    raise TypeError("capacity is over 64 bits")
