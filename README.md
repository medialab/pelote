[![Build Status](https://github.com/medialab/pelote/workflows/Tests/badge.svg)](https://github.com/medialab/pelote/actions)

# Pelote

Pelote is a python library full of network-related functions.

It mainly helps with the following things:

- Conversion of tabular formats to networks (bipartites, citation etc. in the spirit of [Table2Net](https://medialab.github.io/table2net/))
- Conversion of networks to tabular formats
- Monopartite projections of bipartite networks
- Miscellaneous
- Reading & writing of graph formats not found in `networkx` (such as [graphology](https://graphology.github.io/) JSON)

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

* [Tabular to network](#tabular-to-network)
  * [to_bipartite_graph](#to_bipartite_graph)
* [Network to tabular](#network-to-tabular)
  * [to_nodes_dataframe](#to_nodes_dataframe)
  * [to_edges_dataframe](#to_edges_dataframe)
  * [to_dataframes](#to_dataframes)
* [Graph projection](#graph-projection)
  * [monopartite_projection](#monopartite_projection)
* [Graph utilities](#graph-utilities)
  * [largest_connected_component](#largest_connected_component)
  * [crop_to_largest_connected_components](#crop_to_largest_connected_components)
  * [remove_edges](#remove_edges)
* [Reading & Writing](#reading-&-writing)
  * [read_graphology_json](#read_graphology_json)

### Tabular to network

#### to_bipartite_graph

Function creating a bipartite graph from the given tabular data.

*Arguments*

* **table** <span style="color: #268bd2">Iterable[Indexable] or pd.DataFrame</span> - input tabular data. It can
be a large variety of things as long as it is 1. iterable and 2.
yields indexable values such as dicts or lists. This can for instance
be a list of dicts, a csv.DictReader stream etc. It also supports
pandas DataFrame if the library is installed.
* **first_part_col** <span style="color: #268bd2">str or int</span> - the name of the column containing the
value representing a node in the resulting graph's first part.
It could be the index if your rows are lists or a key if your rows
are dicts instead.
* **second_par_col** <span style="color: #268bd2">str or int</span> - the name of the column containing the
value representing a node in the resulting graph's second part.
It could be the index if your rows are lists or a key if your rows
are dicts instead.
* **node_part_attr** <span style="color: #268bd2">?str</span> <span style="color: #cb4b16;">"part"</span> - name of the node attribute containing
the part it belongs to.
* **edge_weight_attr** <span style="color: #268bd2">?str</span> <span style="color: #cb4b16;">"weight"</span> - name of the edge attribute containing
its weight, i.e. the number of times it was found in the table.
* **first_part_data** <span style="color: #268bd2">?Sequence or Callable</span> <span style="color: #cb4b16;">None</span> - sequence (i.e. list, tuple etc.)
of column from rows to keep as node attributes for the graph's first part.
Can also be a function returning a dict of those attributes.
Note that the first row containing a given node will take precedence over
subsequent ones regarding data to include.
* **second_part_data** <span style="color: #268bd2">?Sequence or Callable</span> <span style="color: #cb4b16;">None</span> - sequence (i.e. list, tuple etc.)
of column from rows to keep as node attributes for the graph's second part.
Can also be a function returning a dict of those attributes.
Note that the first row containing a given node will take precedence over
subsequent ones regarding data to include.
* **disjoint_keys** <span style="color: #268bd2">?bool</span> <span style="color: #cb4b16;">False</span> - set this to True as an optimization
mechanism if you know your part keys are disjoint, i.e. if no
value for `first_part_col` can also be found in `second_part_col`.
If you enable this option wrongly, the result can be incorrect.

### Network to tabular

#### to_nodes_dataframe

Function converting the given networkx graph into a pandas DataFrame of
its nodes.

```python
from pelote import to_nodes_dataframe

df = to_nodes_dataframe(graph)
```

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

### Graph projection

#### monopartite_projection



*Arguments*


### Graph utilities

#### largest_connected_component

Function returning the largest connected component of given networkx graph
as a set of nodes.

*Arguments*

* **graph** <span style="color: #268bd2">nx.AnyGraph</span> - target graph.

*Returns*

<span style="color: #268bd2">set</span> - set of nodes representing the largest connected component.

#### crop_to_largest_connected_components

Function mutating the given networkx graph in order to keep only the
largest connected component.

*Arguments*

* **graph** <span style="color: #268bd2">nx.AnyGraph</span> - target graph.

#### remove_edges

Function removing all edges that do not pass a predicate function from a
given networkx graph.

Note that this function mutates the given graph.

*Arguments*

* **graph** <span style="color: #268bd2">nx.AnyGraph</span> - a networkx graph.
* **predicate** <span style="color: #268bd2">callable</span> - a function taking each edge source, target and
attributes and returning True if you want to keep the edge or False
if you want to remove it.

### Reading & Writing

#### read_graphology_json

Function reading and parsing the given json file as a networkx graph.

*Arguments*

* **target** <span style="color: #268bd2">str or Path or file or dict</span> - target to read and parse. Can
be a string path, a Path instance, a file buffer or already
parsed JSON data as a dict.

*Returns*

<span style="color: #268bd2">nx.AnyGraph</span> - a networkx graph instance.
