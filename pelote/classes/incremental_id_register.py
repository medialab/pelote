# =============================================================================
# Pelote Incremental Id Register Class
# =============================================================================
#
from typing import Generic, TypeVar, Dict

K = TypeVar("K")


class IncrementalIdRegister(Generic[K]):
    """
    Helper class mapping incremental ids to arbitrary hashable keys.
    """

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
