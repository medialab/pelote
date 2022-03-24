import csv
from ebbe import Timer

from pelote import (
    table_to_bipartite_graph,
    monopartite_projection,
    floatsam_threshold_learner,
)

with open("data/bipartite2.csv") as f:
    bipartite = table_to_bipartite_graph(csv.DictReader(f), "account", "post")

monopartite = monopartite_projection(bipartite, "account", metric="jaccard")

with Timer("floatsam"):
    threshold = floatsam_threshold_learner(monopartite, on_epoch=print)

print("Found threshold:", threshold)
