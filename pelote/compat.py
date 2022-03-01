# =============================================================================
# Pelote Compatibility Utilities
# =============================================================================
#
# Various constants and helpers dealing with optional deps such as pandas.
#
from functools import wraps

try:
    import pandas

    pd = pandas
except ImportError:
    pd = None


def requires_pandas(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if pd is None:
            raise TypeError("pandas is required for this function to work")

        return f(*args, **kwargs)

    return wrapper


__all__ = ["pd"]
