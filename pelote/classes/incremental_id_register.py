# =============================================================================
# Pelote Incremental Id Register Class
# =============================================================================
#


class IncrementalIdRegister:
    """
    Helper class mapping incremental ids to arbitrary hashable keys.
    """

    __slots__ = ("__counter", "__index")

    def __init__(self):
        self.__counter = 0
        self.__index = {}

    def __getitem__(self, item) -> int:
        item_id = self.__index.get(item)

        if item_id is None:
            item_id = self.__counter
            self.__counter += 1
            self.__index[item] = item_id

        return item_id

    def clear(self) -> None:
        self.__counter = 0
        self.__index.clear()
