import networkx as nx
from collections import Counter

with_triangles = nx.Graph()
with_triangles.add_edge(0, 1)
with_triangles.add_edge(0, 2)
with_triangles.add_edge(0, 5)
with_triangles.add_edge(1, 2)
with_triangles.add_edge(1, 3)
with_triangles.add_edge(2, 4)
with_triangles.add_edge(2, 6)
with_triangles.add_edge(6, 7)
with_triangles.add_edge(7, 8)
with_triangles.add_edge(7, 9)
with_triangles.add_edge(8, 9)
with_triangles.add_edge(8, 10)
with_triangles.add_edge(8, 11)
with_triangles.add_edge(9, 11)

with_quadrangles = nx.Graph()
with_quadrangles.add_edge(0, 1)
with_quadrangles.add_edge(0, 2)
with_quadrangles.add_edge(0, 3)
with_quadrangles.add_edge(1, 2)
with_quadrangles.add_edge(1, 3)
with_quadrangles.add_edge(2, 3)
with_quadrangles.add_edge(2, 4)
with_quadrangles.add_edge(3, 4)
with_quadrangles.add_edge(1, 5)
with_quadrangles.add_edge(1, 6)
with_quadrangles.add_edge(3, 5)
with_quadrangles.add_edge(3, 6)
with_quadrangles.add_edge(5, 6)
with_quadrangles.add_edge(6, 7)
with_quadrangles.add_edge(6, 8)
with_quadrangles.add_edge(7, 8)

with_quadrangles.add_edge(6, 4)
with_quadrangles.add_edge(2, 6)


def k_edge_strength(k, g):
    neighborhoods = {}
    variant = Counter()

    for n0 in g:
        N = set()

        if g.degree[n0] < k - 1:
            continue

        for n1 in g.neighbors(n0):
            if g.degree[n1] < k - 1:
                continue

            if k < 4:
                N.add((n1,))
                continue

            for n2 in g.neighbors(n1):
                if n2 == n1:
                    continue

                if g.degree[n2] < k - 1:
                    continue

                if n0 != n2:
                    s1, s2, s3 = sorted([n0, n1, n2])
                    variant[(s1, s2)] += 1
                    variant[(s2, s3)] += 1

                N.add(tuple(sorted((n0, n1, n2))))

        neighborhoods[n0] = N

    strengths = {}

    for u, v in g.edges:
        un = neighborhoods.get(u, set())
        vn = neighborhoods.get(v, set())

        strengths[u, v] = len(un.intersection(vn))

    return neighborhoods, strengths, variant


TESTS = [(3, with_triangles), (4, with_quadrangles)]

for k, g in TESTS:
    neighborhoods, strengths, variant = k_edge_strength(k, g)

    print("For k =", k)
    print("Neighborhood")
    for n, neighbors in neighborhoods.items():
        print(n, neighbors)

    print("Strengths")
    for e, strength in strengths.items():
        print(e, "=>", strength)

    print("Variant")
    for e, strength in variant.items():
        print(e, "=>", strength)

    print()

print(list(nx.all_simple_paths(with_quadrangles, 0, 2, cutoff=2)))
