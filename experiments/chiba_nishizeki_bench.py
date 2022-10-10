import networkx as nx
from pelote.metrics.chiba_nishizeki import (
    triangles,
    triangular_strength,
    naive_triangular_strength,
)
from ebbe import Timer

g = nx.planted_partition_graph(5, 1000, 0.1, 0.05)

print(g.order(), g.size())

with Timer("triangles"):
    for _ in triangles(g):
        ...

with Timer("triangular_strength"):
    triangular_strength(g)

with Timer("naive_triangular_strength"):
    naive_triangular_strength(g)
