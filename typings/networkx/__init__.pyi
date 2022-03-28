from typing import Optional, Iterable, Generator, Dict, Any, Tuple, Set, overload
from typing_extensions import Literal

from pelote.types import AnyGraph

Attributes = Dict[Any, Any]

class DegreeView:
    @overload
    def __call__(self, key: Any, weight: Optional[str] = ...) -> int: ...
    @overload
    def __call__(self, weight: Optional[str] = ...) -> Dict[int, int]: ...
    def __getitem__(self, key: Any) -> int: ...

class NodeView:
    @overload
    def __call__(
        self, data: Literal[True]
    ) -> Generator[Tuple[Any, Attributes], None, None]: ...
    @overload
    def __call__(self, data: str) -> Generator[Tuple[Any, Any], None, None]: ...
    @overload
    def __call__(self) -> Generator[Any, None, None]: ...
    def __getitem__(self, key: Any) -> Attributes: ...
    def __iter__(self) -> Generator[Any, None, None]: ...
    def data(self) -> Generator[Tuple[Any, Attributes], None, None]: ...

class EdgeView:
    @overload
    def __call__(
        self, nbunch: Any, data: Literal[True]
    ) -> Generator[Tuple[Any, Any, Attributes], None, None]: ...
    @overload
    def __call__(
        self, nbunch: Any, data: str
    ) -> Generator[Tuple[Any, Any, Any], None, None]: ...
    @overload
    def __call__(
        self, data: Literal[True], keys: Literal[True]
    ) -> Generator[Tuple[Any, Any, Any, Attributes], None, None]: ...
    @overload
    def __call__(
        self, data: Literal[True]
    ) -> Generator[Tuple[Any, Any, Attributes], None, None]: ...
    @overload
    def __call__(self, data: str) -> Generator[Tuple[Any, Any, Any], None, None]: ...
    @overload
    def __call__(self) -> Generator[Any, None, None]: ...
    def __iter__(self) -> Generator[Any, None, None]: ...
    @overload
    def data(
        self, data: Literal[True]
    ) -> Generator[Tuple[Any, Any, Attributes], None, None]: ...
    @overload
    def data(self, data: str) -> Generator[Tuple[Any, Any, Any], None, None]: ...
    @overload
    def data(self) -> Generator[Tuple[Any, Any, Attributes], None, None]: ...

class AtlasView:
    def __getitem__(self, key: Any) -> Attributes: ...
    def __iter__(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[Tuple[Any, Attributes], None, None]: ...

class AbstractGraph:
    nodes: NodeView
    edges: EdgeView
    degree: DegreeView

    def __iter__(self) -> Generator[Any, None, None]: ...
    def __contains__(self, key: Any) -> bool: ...
    def __getitem__(self, key: Any) -> AtlasView: ...
    def __len__(self) -> int: ...
    def order(self) -> int: ...
    def size(self) -> int: ...
    def is_directed(self) -> bool: ...
    def is_multigraph(self) -> bool: ...
    def has_node(self, key: Any) -> bool: ...
    def has_edge(self, source: Any, target: Any) -> bool: ...
    def add_node(self, key: Any, **kwargs: Any) -> None: ...
    def add_nodes_from(self, nbunch: Iterable[Any]) -> None: ...
    def add_edge(
        self, source: Any, target: Any, key: Any = ..., **kwargs: Any
    ) -> None: ...
    def add_edges_from(self, ebunch: Iterable[Tuple[Any, Any]]) -> None: ...
    def add_weighted_edges_from(
        self, ebunch: Iterable[Tuple[Any, Any, float]]
    ) -> None: ...
    def remove_node(self, key: Any) -> None: ...
    def remove_edge(self, source: Any, target: Any) -> None: ...

class Graph(AbstractGraph): ...
class DiGraph(AbstractGraph): ...
class MultiGraph(AbstractGraph): ...
class MultiDiGraph(AbstractGraph): ...

def create_empty_copy(
    graph: AbstractGraph, with_data: Optional[bool] = ...
) -> AnyGraph: ...
def connected_components(graph: AbstractGraph) -> Generator[Set[Any], None, None]: ...
def weakly_connected_components(
    graph: AbstractGraph,
) -> Generator[Set[Any], None, None]: ...
