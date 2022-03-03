# =============================================================================
# Pelote Utilities
# =============================================================================
#
# Miscellaneous utility functions used throughout the library.
#
from pelote.types import AnyGraph


def has_mixed_type_node_keys(graph: AnyGraph) -> bool:
    if not graph:
        return False

    nodes = iter(graph.nodes)

    main_type = None

    for node in nodes:
        main_type = type(node)
        break

    for node in nodes:
        if type(node) is not main_type:
            return True

    return False
