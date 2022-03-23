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

* [Tabular data to graphs](#tabular-data-to-graphs)
  * [table_to_bipartite_graph](#table_to_bipartite_graph)
* [Graphs to tabular data](#graphs-to-tabular-data)
  * [graph_to_nodes_dataframe](#graph_to_nodes_dataframe)
  * [graph_to_edges_dataframe](#graph_to_edges_dataframe)
  * [graph_to_dataframes](#graph_to_dataframes)
* [Graph projection](#graph-projection)
  * [monopartite_projection](#monopartite_projection)
* [Graph sparsification](#graph-sparsification)
  * [global_threshold_sparsification](#global_threshold_sparsification)
  * [multiscale_backbone](#multiscale_backbone)
* [Miscellaneous graph-related metrics](#miscellaneous-graph-related-metrics)
  * [edge_disparity](#edge_disparity)
* [Graph utilities](#graph-utilities)
  * [largest_connected_component](#largest_connected_component)
  * [crop_to_largest_connected_component](#crop_to_largest_connected_component)
  * [remove_edges](#remove_edges)
  * [filter_edges](#filter_edges)
* [Learning](#learning)
  * [floatsam_threshold_learner](#floatsam_threshold_learner)
* [Reading & Writing](#reading-&-writing)
  * [read_graphology_json](#read_graphology_json)


---

### Tabular data to graphs

#### table_to_bipartite_graph

Function creating a bipartite graph from the given tabular data.

*Arguments*

* **table** *Iterable[Indexable] or pd.DataFrame* - input tabular data. It can
be a large variety of things as long as it is 1. iterable and 2.
yields indexable values such as dicts or lists. This can for instance
be a list of dicts, a csv.DictReader stream etc. It also supports
pandas DataFrame if the library is installed.
* **first_part_col** *str or int* - the name of the column containing the
value representing a node in the resulting graph's first part.
It could be the index if your rows are lists or a key if your rows
are dicts instead.
* **second_par_col** *str or int* - the name of the column containing the
value representing a node in the resulting graph's second part.
It could be the index if your rows are lists or a key if your rows
are dicts instead.
* **node_part_attr** *str, optional* `"part"` - name of the node attribute containing
the part it belongs to.
* **edge_weight_attr** *str, optional* `"weight"` - name of the edge attribute containing
its weight, i.e. the number of times it was found in the table.
* **first_part_data** *Sequence or Callable, optional* `None` - sequence (i.e. list, tuple etc.)
of column from rows to keep as node attributes for the graph's first part.
Can also be a function returning a dict of those attributes.
Note that the first row containing a given node will take precedence over
subsequent ones regarding data to include.
* **second_part_data** *Sequence or Callable, optional* `None` - sequence (i.e. list, tuple etc.)
of column from rows to keep as node attributes for the graph's second part.
Can also be a function returning a dict of those attributes.
Note that the first row containing a given node will take precedence over
subsequent ones regarding data to include.
* **disjoint_keys** *bool, optional* `False` - set this to True as an optimization
mechanism if you know your part keys are disjoint, i.e. if no
value for `first_part_col` can also be found in `second_part_col`.
If you enable this option wrongly, the result can be incorrect.

*Returns*

*nx.AnyGraph* - the bipartite graph.


---

### Graphs to tabular data

#### graph_to_nodes_dataframe

Function converting the given networkx graph into a pandas DataFrame of
its nodes.

```python
from pelote import to_nodes_dataframe

df = to_nodes_dataframe(graph)
```

*Arguments*

* **nx.AnyGraph**  - a networkx graph instance
* **node_key_col** *str, optional* `"key"` - name of the DataFrame column containing
the node keys. If None, the node keys will be used as the DataFrame
index.

*Returns*

*pd.DataFrame* - A pandas DataFrame

#### graph_to_edges_dataframe

Function converting the given networkx graph into a pandas DataFrame of
its edges.

*Arguments*

* **nx.AnyGraph**  - a networkx graph instance
* **edge_source_col** *str, optional* `"source"` - name of the DataFrame column containing
the edge source.
* **edge_target_col** *str, optional* `"target"` - name of the DataFrame column containing
the edge target.
* **source_node_data** *Iterable or Mapping, optional* `None` - iterable of attribute names
or mapping from attribute names to column name to be used to add
columns to the resulting dataframe based on source node data.
* **target_node_data** *Iterable or Mapping, optional* `None` - iterable of attribute names
or mapping from attribute names to column name to be used to add
columns to the resulting dataframe based on target node data.

*Returns*

*pd.DataFrame* - A pandas DataFrame

#### graph_to_dataframes

Function converting the given networkx graph into two pandas DataFrames:
one for its nodes, one for its edges.

*Arguments*

* **nx.AnyGraph**  - a networkx graph instance
* **node_key_col** *str, optional* `"key"` - name of the node DataFrame column containing
the node keys. If None, the node keys will be used as the DataFrame
index.
* **edge_source_col** *str, optional* `"source"` - name of the edge DataFrame column containing
the edge source.
* **edge_target_col** *str, optional* `"target"` - name of the edge DataFrame column containing
the edge target.
* **source_node_data** *Iterable or Mapping, optional* `None` - iterable of attribute names
or mapping from attribute names to column name to be used to add
columns to the edge dataframe based on source node data.
* **target_node_data** *Iterable or Mapping, optional* `None` - iterable of attribute names
or mapping from attribute names to column name to be used to add
columns to the edge dataframe based on target node data.

*Returns*

*None* - (pd.DataFrame, pd.DataFrame)


---

### Graph projection

#### monopartite_projection

Function returning the monopartite projection of a given bipartite graph
wrt one of both partitions of the graph.

That is to say the resulting graph will keep a single type of nodes sharing
weighted edges based on the neighbors they shared in the bipartite graph.

```python
import networkx as nx
from pelote import monopartite_projection

bipartite = nx.Graph()
bipartite.add_nodes_from([1, 2, 3], part='account')
bipartite.add_nodes_from([4, 5, 6], part='color')
bipartite.add_edges_from([
    (1, 4),
    (1, 5),
    (2, 6),
    (3, 4),
    (3, 6)
])

# Resulting graph will only contain nodes [1, 2, 3]
# with edges: (1, 3) and (2, 3)
monopartite = monopartite_projection(bipartite, 'account')
```

*Arguments*

* **bipartite_graph** *nx.AnyGraph* - target graph. The function will raise
if given graph is not truly bipartite.
* **part_to_keep** *Hashable or Collection* - partition to keep in the projected
graph. It can either be the value of the part node attribute in the
given graph (a string, most commonly), or a collection (a set, list etc.)
holding the nodes composing the part to keep.
* **node_part_attr** *str, optional* `"part"` - name of the node attribute containing
the part the node belongs to.
* **edge_weight_attr** *str, optional* `"weight"` - name of the edge attribute containing
the edge's weight.
* **metric** *str, optional* `None` - one of "jaccard", "overlap", "cosine", "dice"
or "binary_cosine". If not given, resulting weight will be seyto the
size of neighbor intersection.
* **bipartition_check** *bool, optional* `True` - whether to check if given graph
is truly bipartite. You can disable this as an optimization
strategy if you know what you are doing.
* **weight_threshold** *float, optional* `None` - if an edge weight should be less
than this threshold we would not add it to the projected
monopartite graph.

*Returns*

*nx.Graph* - the projected monopartite graph.


---

### Graph sparsification

#### global_threshold_sparsification

Function returning a copy of the given graph without edges whose weight
is less than a given threshold.

*Arguments*

* **graph** *nx.AnyGraph* - target graph.
* **weight_threshold** *float* - weight threshold.
* **reverse** *bool, optional* - whether to reverse the threshold condition.
That is to say an edge would be removed if its weight is greater
than the threshold.

*Returns*

*nx.AnyGraph* - the sparse graph.

#### multiscale_backbone

Function returning the multiscale backbone of the given graph, i.e. a copy
of the graph were we only kept "relevant" edges, as defined by a
statistical test where we compare the likelihood of a weighted edge existing
vs. the null model.

Article:
    Serrano, M. Ángeles, Marián Boguná, and Alessandro Vespignani. "Extracting
    the multiscale backbone of complex weighted networks." Proceedings of the
    national academy of sciences 106.16 (2009): 6483-6488.

References:
    - https://www.pnas.org/content/pnas/106/16/6483.full.pdf
    - https://en.wikipedia.org/wiki/Disparity_filter_algorithm_of_weighted_network

*Arguments*

* **graph** *nx.AnyGraph* - target graph.
* **alpha** *float, optional* `0.05` - alpha value for the statistical test. It can
be intuitively thought of as a p-value score for an edge to be
kept in the resulting graph.
* **edge_weight_attr** *str, optional* `"weight"` - name of the edge attribute holding
the edge's weight.

*Returns*

*nx.AnyGraph* - the sparse graph.


---

### Miscellaneous graph-related metrics

#### edge_disparity

Function computing the disparity score of each edge in the given graph. This
score is typically used to extract the multiscale backbone of a weighted
graph.

*Arguments*

* **graph** *nx.AnyGraph* - target graph.
* **edge_weight_attr** *str, optional* `"weight"` - name of the edge attribute containing
its weight.
* **reverse** *bool, optional* `False` - whether to reverse the metric, i.e. return
`1 - score`.

*Returns*

*dict* - Dictionnary with edges - (source, target) tuples - as keys and the disparity scores as values


---

### Graph utilities

#### largest_connected_component

Function returning the largest connected component of given networkx graph
as a set of nodes.

Note that this function will consider any given graph as undirected and
will therefore work with weakly connected components in the directed case.

*Arguments*

* **graph** *nx.AnyGraph* - target graph.

*Returns*

*set* - set of nodes representing the largest connected component.

#### crop_to_largest_connected_component

Function mutating the given networkx graph in order to keep only the
largest connected component.

Note that this function will consider any given graph as undirected and
will therefore work with weakly connected components in the directed case.

*Arguments*

* **graph** *nx.AnyGraph* - target graph.

#### remove_edges

Function removing all edges that do not pass a predicate function from a
given networkx graph.

Note that this function mutates the given graph.

*Arguments*

* **graph** *nx.AnyGraph* - a networkx graph.
* **predicate** *callable* - a function taking each edge source, target and
attributes and returning True if you want to keep the edge or False
if you want to remove it.

#### filter_edges

Function returning a copy of the given networkx graph but without the edges
filtered out by the given predicate function

*Arguments*

* **graph** *nx.AnyGraph* - a networkx graph.
* **predicate** *callable* - a function taking each edge source, target and
attributes and returning True if you want to keep the edge or False
if you want to remove it.

*Returns*

*nx.AnyGraph* - the filtered graph.


---

### Learning

#### floatsam_threshold_learner

Function using an iterative algorithm to try and find the best weight
threshold to apply to trim the given graph's edges while keeping the
underlying community structure.

It works by iteratively increasing the threshold and stopping as soon as
a significant connected component starts to drift away from the principal
one.

This is basically an optimization algorithm applied to a complex nonlinear
function using a very naive cost heuristic, but it works decently for typical
cases as it emulates the method used by hand by some researchers when they
perform this kind of task on Gephi, for instance.

*Arguments*

* **graph** *nx.Graph* - Graph to sparsify.
* **starting_threshold** *float, optional* `0.0` - Starting similarity threshold.
* **learning_rate** *float, optional* `0.05` - How much to increase the threshold
at each step of the algorithm.
* **max_drifter_order** *int, optional* - Max order of component to detach itself
from the principal one before stopping the algorithm. If not
provided it will default to the logarithm of the graph's largest
connected component's order.
* **edge_weight_attr** *str, optional* `"weight"` - Name of the weight attribute.

*Returns*

*float* - The found threshold


---

### Reading & Writing

#### read_graphology_json

Function reading and parsing the given json file as a networkx graph.

*Arguments*

* **target** *str or Path or file or dict* - target to read and parse. Can
be a string path, a Path instance, a file buffer or already
parsed JSON data as a dict.

*Returns*

*nx.AnyGraph* - a networkx graph instance.
