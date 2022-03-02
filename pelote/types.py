import networkx as nx
from typing import Union, TypeVar

NodeKey = TypeVar("NodeKey")

AnyGraph = Union[
    "nx.Graph[NodeKey]",
    "nx.DiGraph[NodeKey]",
    "nx.MultiGraph[NodeKey]",
    "nx.MultiDiGraph[NodeKey]",
]
