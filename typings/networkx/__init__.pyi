from typing import Iterable, Generator, Dict, Any

Attributes = Dict[Any, Any]

class NodeView:
    def __call__(self, data: bool = ...) -> Generator[Any, None, None]: ...
    def __getitem__(self, key: Any) -> Attributes: ...
    def __iter__(self) -> Generator[Any, None, None]: ...

class AbstractGraph:
    nodes: NodeView

    def __iter__(self) -> Generator[Any, None, None]: ...
    def order(self) -> int: ...
    def size(self) -> int: ...
    def add_node(self, key: Any, **kwargs: Any) -> None: ...
    def add_nodes_from(self, nbunch: Iterable[Any]) -> None: ...

class Graph(AbstractGraph): ...
class DiGraph(AbstractGraph): ...
class MultiGraph(AbstractGraph): ...
class MultiDiGraph(AbstractGraph): ...
