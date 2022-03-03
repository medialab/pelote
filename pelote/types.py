import networkx as nx
from typing import Any, Union, TypeVar, Dict, List
from typing_extensions import TypedDict, Literal, NotRequired
from pathlib import Path
from io import IOBase

# Misc utils
FileHandle = Union[str, Path, IOBase]

# Networkx-related
NodeKey = TypeVar("NodeKey")

AnyGraph = Union[
    nx.Graph,
    nx.DiGraph,
    nx.MultiGraph,
    nx.MultiDiGraph,
]


# Graphology serialization
SerializedAttributes = Dict[str, Any]
GraphologyType = Literal["directed", "undirected", "mixed"]


class GraphologySerializedNode(TypedDict):
    key: str
    attributes: NotRequired[SerializedAttributes]


class GraphologySerializedEdge(TypedDict):
    key: NotRequired[str]
    source: str
    target: str
    attributes: NotRequired[SerializedAttributes]
    undirected: NotRequired[bool]


class GraphologySerializedOptions(TypedDict):
    allowSelfLoops: bool
    type: GraphologyType
    multi: bool


class GraphologySerializedGraph(TypedDict):
    options: NotRequired[GraphologySerializedOptions]
    attributes: NotRequired[SerializedAttributes]
    nodes: NotRequired[List[GraphologySerializedNode]]
    edges: NotRequired[List[GraphologySerializedEdge]]
