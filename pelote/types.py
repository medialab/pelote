import networkx as nx
from typing import Any, Union, TypeVar, Dict, Optional, List
from typing_extensions import TypedDict, Literal
from pathlib import Path
from io import IOBase

# Misc utils
FileHandle = Union[str, Path, IOBase]

# Networkx-related
NodeKey = TypeVar("NodeKey")

AnyGraph = Union[
    "nx.Graph[NodeKey]",
    "nx.DiGraph[NodeKey]",
    "nx.MultiGraph[NodeKey]",
    "nx.MultiDiGraph[NodeKey]",
]


# Graphology serialization
SerializedAttributes = Dict[str, Any]
GraphologyType = Literal["directed", "undirected", "mixed"]


class GraphologySerializedNode(TypedDict):
    key: str
    attributes: Optional[SerializedAttributes]


class GraphologySerializedEdge(TypedDict):
    key: Optional[str]
    source: str
    target: str
    attributes: Optional[SerializedAttributes]
    undirected: Optional[bool]


class GraphologySerializedOptions(TypedDict):
    allowSelfLoops: bool
    type: GraphologyType
    multi: bool


class GraphologySerializedGraph(TypedDict):
    options: Optional[GraphologySerializedOptions]
    attributes: Optional[SerializedAttributes]
    nodes: Optional[List[GraphologySerializedNode]]
    edges: Optional[List[GraphologySerializedEdge]]
