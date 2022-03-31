# =============================================================================
# Pelote Utilities
# =============================================================================
#
# Miscellaneous utility functions used throughout the library.
#
from collections import Counter, defaultdict, OrderedDict
from typing import Iterable, Any, Dict, TypeVar

from pelote.types import AnyGraph

K = TypeVar("K")
V = TypeVar("V")
NodeKey = TypeVar("NodeKey")


def has_mixed_types(iterable: Iterable[Any]) -> bool:
    iterator = iter(iterable)

    main_type = None

    for item in iterator:
        main_type = type(item)
        break

    for item in iterator:
        if type(item) is not main_type:
            return True

    return False


def check_node_exists(g: AnyGraph, n: NodeKey) -> NodeKey:
    if n not in g:
        raise KeyError("Node {} does not exist. {}".format(n, g.nodes))

    return n


def dict_without(d: Dict[K, V], k: str) -> Dict[K, V]:
    o = {}

    for n, v in d.items():
        if n == k:
            continue

        o[n] = v

    return o


CONSTANT_TIME_LOOKUP = (set, frozenset, dict, Counter, defaultdict, OrderedDict)


def has_constant_time_lookup(v: Any) -> bool:
    return isinstance(v, CONSTANT_TIME_LOOKUP)
