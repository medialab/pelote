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

* [Network to Tabular](#network-to-tabular)
  * [to_nodes_dataframe](#to_nodes_dataframe)
  * [to_edges_dataframe](#to_edges_dataframe)
  * [to_dataframes](#to_dataframes)

### Network to Tabular

#### to_nodes_dataframe

Function converting the given networkx graph into a pandas DataFrame of
its nodes.

*Arguments*

* **nx.AnyGraph** <span style="color: #268bd2">None</span> - a networkx graph instance
* **node_key_col** <span style="color: #268bd2">?str</span> <span style="color: #cb4b16;">"key"</span> - name of the DataFrame column containing
the node keys. If None, the node keys will be used as the DataFrame
index.

*Returns*

<span style="color: #268bd2">pd.DataFrame</span> - A pandas DataFrame

#### to_edges_dataframe

Function converting the given networkx graph into a pandas DataFrame of
its edges.

*Arguments*

* **nx.AnyGraph** <span style="color: #268bd2">None</span> - a networkx graph instance
* **edge_source_col** <span style="color: #268bd2">?str</span> <span style="color: #cb4b16;">"source"</span> - name of the DataFrame column containing
the edge source.
* **edge_target_col** <span style="color: #268bd2">?str</span> <span style="color: #cb4b16;">"target"</span> - name of the DataFrame column containing
the edge target.

*Returns*

<span style="color: #268bd2">pd.DataFrame</span> - A pandas DataFrame

#### to_dataframes

Function converting the given networkx graph into two pandas DataFrames:
one for its nodes, one for its edges.

*Arguments*

* **nx.AnyGraph** <span style="color: #268bd2">None</span> - a networkx graph instance
* **node_key_col** <span style="color: #268bd2">?str</span> <span style="color: #cb4b16;">"key"</span> - name of the node DataFrame column containing
the node keys. If None, the node keys will be used as the DataFrame
index.
* **edge_source_col** <span style="color: #268bd2">?str</span> <span style="color: #cb4b16;">"source"</span> - name of the edge DataFrame column containing
the edge source.
* **edge_target_col** <span style="color: #268bd2">?str</span> <span style="color: #cb4b16;">"target"</span> - name of the edge DataFrame column containing
the edge target.

*Returns*

<span style="color: #268bd2">None</span> - (pd.DataFrame, pd.DataFrame)
