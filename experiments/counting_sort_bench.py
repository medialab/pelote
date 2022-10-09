from ebbe import Timer
import networkx as nx
from pelote.utils import counting_sort

g = nx.fast_gnp_random_graph(500_000, 0.00001)

print(g.order(), g.size())

with Timer("sorted"):
    sorted(g, key=g.degree)

with Timer("counting_sort"):
    counting_sort(g, key=g.degree)
