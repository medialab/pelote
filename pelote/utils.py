# =============================================================================
# Pelote Utilities
# =============================================================================
#
# Miscellaneous utility functions used throughout the library.
#
from typing import Iterable, Any, Dict, TypeVar, Generic

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
    __slots__ = ("i", "index")

    def __init__(self):
        self.i = 0
        self.index: Dict[K, int] = {}

    def __getitem__(self, item: K) -> int:
        item_id = self.index.get(item)

        if item_id is None:
            item_id = self.i
            self.i += 1
            self.index[item] = item_id

        return item_id


def dict_without(d: Dict[K, V], k: str) -> Dict[K, V]:
    o = {}

    for n, v in d.items():
        if n == k:
            continue

        o[n] = v

    return o
