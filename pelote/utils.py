# =============================================================================
# Pelote Utilities
# =============================================================================
#
# Miscellaneous utility functions used throughout the library.
#
from typing import Iterable, Any


def has_mixed_types(iterable: Iterable[Any]) -> bool:
    nodes = iter(iterable)

    main_type = None

    for node in nodes:
        main_type = type(node)
        break

    for node in nodes:
        if type(node) is not main_type:
            return True

    return False
