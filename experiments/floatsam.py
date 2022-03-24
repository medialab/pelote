import csv
from ebbe import Timer

from pelote import (
    table_to_bipartite_graph,
    monopartite_projection,
    floatsam_threshold_learner,
)

from pelote.graph import largest_connected_component_order

with open("data/bipartite2.csv") as f:
    bipartite = table_to_bipartite_graph(csv.DictReader(f), "account", "post")

monopartite = monopartite_projection(bipartite, "account", metric="jaccard")

print(monopartite.order(), largest_connected_component_order(monopartite))

with Timer("floatsam"):
    threshold = floatsam_threshold_learner(
        monopartite, on_epoch=print, max_drifter_order=25
    )

print("Found threshold:", threshold)
