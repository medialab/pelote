# =============================================================================
# Pelote Utilities
# =============================================================================
#
# Miscellaneous utility functions used throughout the library.
#
from collections import Counter, defaultdict, OrderedDict
from typing import Iterable, Any, Dict, TypeVar, Generic, List, Set, Optional

from pelote.types import AnyGraph

K = TypeVar("K")
V = TypeVar("V")


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


class IncrementalIdRegister(Generic[K]):
    def __init__(self):
        self.__counter = 0
        self.__index: Dict[K, int] = {}

    def __getitem__(self, item: K) -> int:
        item_id = self.__index.get(item)

        if item_id is None:
            item_id = self.__counter
            self.__counter += 1
            self.__index[item] = item_id

        return item_id


class DFSStack(Generic[V]):
    def __init__(self, graph: AnyGraph):
        self.__order = graph.order()
        self.__stack: List[V] = []
        self.__seen: Set[V] = set()

    def __len__(self) -> int:
        return len(self.__stack)

    def __contains__(self, node: V) -> bool:
        return node in self.__seen

    def has_seen_everything(self) -> bool:
        return len(self.__seen) == self.__order

    def append(self, node: V) -> bool:
        size_before = len(self.__seen)

        self.__seen.add(node)

        if size_before == len(self.__seen):
            return False

        self.__stack.append(node)

        return True

    def pop(self) -> Optional[V]:
        if len(self.__stack) == 0:
            return None

        return self.__stack.pop()


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
