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


def check_node_exists(g, n):
    if n not in g:
        raise KeyError("Node {} does not exist. {}".format(n, g.nodes))

    return n


def dict_without(d, k: str):
    o = {}

    for n, v in d.items():
        if n == k:
            continue

        o[n] = v

    return o


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
