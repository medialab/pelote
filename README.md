[![Build Status](https://github.com/medialab/pelote/workflows/Tests/badge.svg)](https://github.com/medialab/pelote/actions)

# Pelote

Pelote is a python library full of network-related functions.

It mainly helps with the following things:

- Conversion of networks to tabular formats
- Conversion of tabular formats to networks (bipartites, citation etc.)
- Monopartite projections

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

* [Network to Tabular](#network_to_tabular)
  * [to_nodes_dataframe](#to_nodes_dataframe)

### Network to Tabular

#### to_nodes_dataframe

Function converting the given networkx graph into a pandas DataFrame of
its nodes.

*Arguments*

* **nx.AnyGraph** *None*: a networkx graph instance
* **node_key_col** *?str* [`"key"`]: name of the DataFrame column containing
the node keys. If None, the node keys will be used as the DataFrame
index.
