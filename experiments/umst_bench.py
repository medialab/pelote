import networkx as nx
from pelote import union_of_maximum_spanning_trees
from ebbe import Timer

g = nx.planted_partition_graph(5, 1000, 0.1, 0.05)

print(g.order(), g.size())

with Timer("umst"):
    for _ in union_of_maximum_spanning_trees(g):
        ...
