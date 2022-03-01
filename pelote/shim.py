from contextlib import contextmanager

try:
    import pandas

    pd = pandas
    original_pandas = pandas
except ImportError:
    pd = None
    original_pandas = None


from pelote.exceptions import MissingPandasException


def obliterate_pandas():
    """
    Function forcing the library to consider that `pandas` was not installed,
    which can be useful when unit testing.
    """

    global pd
    pd = None


def resurrect_pandas():
    """
    Function forcing the library to acknowledge that `pandas` is back to life,
    which can be useful when unit testing.
    """

    global pd, original_pandas

    if original_pandas is not None:
        pd = original_pandas


@contextmanager
def missing_pandas():
    obliterate_pandas()

    try:
        yield
    finally:
        resurrect_pandas()


def is_pandas_available() -> bool:
    """
    Function returning whether `pandas` is installed.
    """
    return pd is not None


def check_pandas() -> None:
    """
    Function raising if `pandas` is not installed.

    Note that I could use a decorator but I don't because those cannot be
    usefully typed before python v3.10.
    """
    if pd is None:
        raise MissingPandasException(
            "pandas must be installed for this function to work"
        )
