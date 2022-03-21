[![Build Status](https://github.com/medialab/pelote/workflows/Tests/badge.svg)](https://github.com/medialab/pelote/actions)

# Pelote

Pelote is a python library full of graph-related functions that can be used to complement [networkx](https://networkx.org/) for higher-level tasks.

It mainly helps with the following things:

- Conversion of tabular data to graphs (bipartites, citation etc. in the spirit of [Table2Net](https://medialab.github.io/table2net/))
- Conversion of graphs to tabular data
- Monopartite projections of bipartite graphs
- Miscellaneous graph helper functions (filtering out nodes, edges etc.)
- Sparsification of graphs
- Reading & writing of graph formats not found in `networkx` (such as [graphology](https://graphology.github.io/) JSON)

As such it is the perfect companion to [ipysigma](https://github.com/Yomguithereal/ipysigma), our Jupyter widget that can render interactive graphs directly within your notebooks.

## Installation

You can install `pelote` with pip with the following command:

```
pip install pelote
```

If you want to be able to use the library with `pandas`, you will need to install it also:

```
pip install pandas
```

## Usage

{toc}
{docs}
