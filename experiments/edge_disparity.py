import csv
from ebbe import Timer

from pelote import table_to_bipartite_graph, edge_disparity, monopartite_projection

with open("data/bipartite2.csv") as f:
    bipartite = table_to_bipartite_graph(csv.DictReader(f), "account", "post")

with Timer("projection"):
    monopartite = monopartite_projection(bipartite, "account", metric="jaccard")

print(monopartite.order(), monopartite.size())

with Timer("edge_disparity"):
    edge_disparity(monopartite)
