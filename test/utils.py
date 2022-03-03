# =============================================================================
# Pelote Unit Test Utilities
# =============================================================================
from os.path import join, dirname

RESOURCES_DIR = join(dirname(__file__), "resources")


def get_resource_path(name: str) -> str:
    return join(RESOURCES_DIR, name)
