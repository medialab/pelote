from ebbe import Timer
import pandas as pd


diamonds = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv')

data = ["carat", "cut", "color", "clarity", "price"]


def iter_iterrows(df, columns):
    rows = []
    for i, row in df[columns].iterrows():
        rows.append([row[col] for col in columns])
    return rows


def iter_zip(df, columns):
    rows = []
    for row in zip(*(df[col].values for col in columns)):
        rows.append(list(row))
    return rows


def iter_itertuples(df, columns):
    rows = []
    indices = {col: i for i, col in enumerate(df[columns].columns)}
    for row in df[columns].itertuples(index=False):
        rows.append([row[indices[col]] for col in columns])
    return rows


with Timer("iter with iterrows"):
    a = iter_iterrows(diamonds, data)


with Timer("iter with itertuples"):
    c = iter_itertuples(diamonds, data)


with Timer("iter with zip"):
    b = iter_zip(diamonds, data)

assert a == b
assert a == c
