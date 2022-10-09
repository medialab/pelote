from ebbe import Timer
from array import array
import numpy as np
from random import shuffle

l = []
a = array("L")

N = 10_000_000
R = list(range(N))
shuffle(R)

# Append
with Timer("list append"):
    for i in range(N):
        l.append(i)

with Timer("array append"):
    for i in range(N):
        a.append(i)

# Instantiation
with Timer("list instantiation"):
    l = list(range(N))

with Timer("array instantiation"):
    a = array("L", range(N))

with Timer("numpy instantiation"):
    n = np.arange(N, dtype="uint32")

# Set
with Timer("list set"):
    for i in range(N):
        l[i] = i * 2

with Timer("array set"):
    for i in range(N):
        a[i] = i * 2

with Timer("numpy set"):
    for i in range(N):
        n[i] = i * 2

# Random set
with Timer("list random set"):
    for i in R:
        l[i] = i * 2

with Timer("array random set"):
    for i in R:
        a[i] = i * 2

with Timer("numpy random set"):
    for i in R:
        n[i] = i * 2

# Read
with Timer("list read"):
    for i in range(N):
        i = l[i]

with Timer("array read"):
    for i in range(N):
        i = a[i]

with Timer("numpy read"):
    for i in range(N):
        i = n[i]

# Random read
with Timer("list random read"):
    for i in R:
        i = l[i]

with Timer("array random read"):
    for i in R:
        i = a[i]

with Timer("numpy random read"):
    for i in R:
        i = n[i]

# Iteration
with Timer("list iter"):
    for i in l:
        ...

with Timer("array iter"):
    for i in a:
        ...

with Timer("numpy iter"):
    for i in n:
        ...
