import networkx as nx
from typing import Any, Union, Dict, List, Iterable
from typing_extensions import TypedDict, Literal, NotRequired, Protocol
from pathlib import Path
from io import IOBase

from pelote.shim import pd

# Misc utils
FileHandle = Union[str, Path, IOBase]
GenericKey = Union[str, int]


class Indexable(Protocol):
    def __getitem__(self, key: Any) -> Any:
        ...


Tabular = Union["pd.DataFrame", Iterable[Indexable]]

# Networkx-related
AnyGraph = Union[
    nx.Graph,
    nx.DiGraph,
    nx.MultiGraph,
    nx.MultiDiGraph,
]
Attributes = Dict[Any, Any]

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
