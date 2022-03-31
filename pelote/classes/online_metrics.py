# =============================================================================
# Pelote Online Metrics Class
# =============================================================================
#
import math
from typing import Generic, TypeVar, Dict, Generator, Tuple, Optional
from typing_extensions import Literal
from collections import Counter


Item = TypeVar("Item")


class OnlineMetric(Generic[Item]):
    """
    A class used to compute many similarity metrics online while performing
    various graph projections etc.
    """

    def __init__(self):
        self._norms: Dict[Item, float] = {}
        self._norm_acc: float = 0
        self._intersections: Dict[Item, float] = Counter()
        self._current_source_norm: float

    def _should_keep_norm(self) -> bool:
        return self._norm_acc > 0

    def _finalize_norm(self, norm: float) -> float:
        return norm

    def _accumulate(self, weight: float) -> None:
        raise NotImplementedError

    def accumulate_norm(self, weight: float) -> None:
        self._accumulate(weight)

    def add_norm(self, item: Item) -> None:
        if not self._should_keep_norm():
            return

        norm = self._finalize_norm(self._norm_acc)
        self._norm_acc = 0
        self._norms[item] = norm

    def finalize(self) -> None:
        pass

    def nodes(self) -> Generator[Item, None, None]:
        yield from self._norms.keys()

    def __getitem__(self, item: Item) -> float:
        return self._norms[item]

    def start_intersection(self, source: Item) -> None:
        self._current_source_norm = self._norms[source]
        self._intersections.clear()  # TODO: benchmark vs. GC

    def _compute_intersection_weight(self, w1: float, w2: float) -> float:
        raise NotImplementedError

    def intersect(self, target: Item, w1: float, w2: float) -> None:
        weight = self._compute_intersection_weight(w1, w2)
        self._intersections[target] += weight

    def _compute_metric(self, intersection: float, norm1: float, norm2: float) -> float:
        raise NotImplementedError

    def neighbors(self) -> Generator[Tuple[Item, float], None, None]:
        norm1 = self._current_source_norm

        for neighbor, intersection in self._intersections.items():
            norm2 = self._norms[neighbor]
            similarity = self._compute_metric(intersection, norm1, norm2)

            yield neighbor, similarity


class BinaryMetric(OnlineMetric[Item]):
    def _accumulate(self, weight: float):
        self._norm_acc += 1

    def _compute_intersection_weight(self, w1: float, w2: float) -> float:
        return 1


class IntersectionMetric(BinaryMetric[Item]):
    def _compute_metric(self, intersection: float, norm1: float, norm2: float) -> float:
        return intersection


class JaccardMetric(BinaryMetric[Item]):
    def _compute_metric(self, intersection: float, norm1: float, norm2: float) -> float:
        return intersection / (norm1 + norm2 - intersection)


class OverlapMetric(BinaryMetric[Item]):
    def _compute_metric(self, intersection: float, norm1: float, norm2: float) -> float:
        return intersection / min(norm1, norm2)


class DiceMetric(BinaryMetric[Item]):
    def _compute_metric(self, intersection: float, norm1: float, norm2: float) -> float:
        return (intersection * 2) / (norm1 + norm2)


class BinaryCosineMetric(BinaryMetric[Item]):
    def _finalize_norm(self, norm: float) -> float:
        return math.sqrt(norm)

    def _compute_metric(self, intersection: float, norm1: float, norm2: float) -> float:
        return intersection / (norm1 * norm2)


class DotProductMetric(BinaryMetric[Item]):
    def _compute_intersection_weight(self, w1: float, w2: float) -> float:
        return w1 * w2

    def _compute_metric(self, intersection: float, norm1: float, norm2: float) -> float:
        return intersection


class CosineMetric(BinaryCosineMetric[Item]):
    def _accumulate(self, weight: float):
        self._norm_acc += weight * weight

    def _compute_intersection_weight(self, w1: float, w2: float) -> float:
        return w1 * w2


class PMIMetric(BinaryMetric[Item]):
    def _should_keep_norm(self) -> bool:
        return self._norm_acc >= 0

    def _compute_metric(self, intersection: float, norm1: float, norm2: float) -> float:
        # TODO: what should we do when the result is 0?
        return math.log(intersection / (norm1 * norm2))


SUPPORTED_METRICS = {
    None: IntersectionMetric,
    "jaccard": JaccardMetric,
    "overlap": OverlapMetric,
    "cosine": CosineMetric,
    "dice": DiceMetric,
    "binary_cosine": BinaryCosineMetric,
    "dot_product": DotProductMetric,
    "pmi": PMIMetric,
}
Metric = Literal[
    "jaccard", "overlap", "cosine", "dice", "binary_cosine", "dot_product", "pmi"
]


def instantiate_online_metric(metric: Optional[Metric] = None) -> OnlineMetric:
    if metric not in SUPPORTED_METRICS:
        raise TypeError(
            'unknown metric "%s", expecting one of %s'
            % (metric, ", ".join('"%s"' % m for m in SUPPORTED_METRICS))
        )

    return SUPPORTED_METRICS[metric]()
