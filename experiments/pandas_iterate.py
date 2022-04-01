from ebbe import Timer
import pandas as pd

"""
Experiment on pandas dataframe iteration speed:
iter with iterrows: 3s, 946ms
iter with itertuples and get dicts: 120ms, 302µs
iter with zip and get dicts: 60ms, 224µs
iter with itertuples and get tuples: 111ms, 277µs
iter with zip and get tuples: 34ms, 987µs
"""

diamonds = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv')

data = ["carat", "cut", "color", "clarity", "price"]


def iter_iterrows(df, columns):
    rows = []
    table = (row for _, row in df[columns].iterrows())
    for row in table:
        rows.append([row[col] for col in columns])
    return rows


def iter_tuples_itertuples(df, columns):
    rows = []
    table = df[columns].itertuples(index=False)
    columns = range(len(columns))
    for row in table:
        rows.append([row[col] for col in columns])
    return rows


def iter_tuples_zip(df, columns):
    rows = []
    table = zip(*(df[col].values for col in columns))
    columns = range(len(columns))
    for row in table:
        rows.append([row[col] for col in columns])
    return rows


def iter_dict_itertuples(df, columns):
    rows = []
    table = (dict(zip(columns, row)) for row in df[columns].itertuples(index=False))
    for row in table:
        rows.append([row[col] for col in columns])
    return rows


def iter_dict_zip(df, columns):
    rows = []
    table = (dict(zip(columns, row)) for row in zip(*(df[col].values for col in columns)))
    for row in table:
        rows.append([row[col] for col in columns])
    return rows


with Timer("iter with iterrows"):
    a = iter_iterrows(diamonds, data)


with Timer("iter with itertuples and get dicts"):
    b = iter_dict_itertuples(diamonds, data)


with Timer("iter with zip and get dicts"):
    c = iter_dict_zip(diamonds, data)


with Timer("iter with itertuples and get tuples"):
    d = iter_tuples_itertuples(diamonds, data)


with Timer("iter with zip and get tuples"):
    e = iter_tuples_zip(diamonds, data)

assert a == b
assert a == c
assert a == d
assert a == e
