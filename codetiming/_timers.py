"""Dictionary-like structure with information about timers"""

# Standard library imports
import collections
import math
import statistics
from typing import TYPE_CHECKING, Any, Callable, Dict, List

# Annotate generic UserDict
if TYPE_CHECKING:
    UserDict = collections.UserDict[str, float]  # pragma: no cover
else:
    UserDict = collections.UserDict


class Timers(UserDict):
    """Custom dictionary that stores information about timers"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Add a private dictionary keeping track of all timings"""
        super().__init__(*args, **kwargs)
        self._timings: Dict[str, List[float]] = collections.defaultdict(list)

    def add(self, name: str, value: float) -> None:
        """Add a timing value to the given timer"""
        self._timings[name].append(value)
        self.data.setdefault(name, 0)
        self.data[name] += value

    def clear(self) -> None:
        """Clear timers"""
        self.data.clear()
        self._timings.clear()

    def __setitem__(self, name: str, value: float) -> None:
        """Disallow setting of timer values"""
        raise TypeError(
            f"{self.__class__.__name__!r} does not support item assignment. "
            "Use '.add()' to update values."
        )

    def apply(self, func: Callable[[List[float]], float], name: str) -> float:
        """Apply a function to the results of one named timer"""
        if name in self._timings:
            return func(self._timings[name])
        raise KeyError(name)

    def count(self, name: str) -> float:
        """Number of timings"""
        return self.apply(len, name=name)

    def total(self, name: str) -> float:
        """Total time for timers"""
        return self.apply(sum, name=name)

    def min(self, name: str) -> float:
        """Minimal value of timings"""
        return self.apply(lambda values: min(values or [0]), name=name)

    def max(self, name: str) -> float:
        """Maximal value of timings"""
        return self.apply(lambda values: max(values or [0]), name=name)

    def mean(self, name: str) -> float:
        """Mean value of timings"""
        return self.apply(lambda values: statistics.mean(values or [0]), name=name)

    def median(self, name: str) -> float:
        """Median value of timings"""
        return self.apply(lambda values: statistics.median(values or [0]), name=name)

    def stdev(self, name: str) -> float:
        """Standard deviation of timings"""
        if name in self._timings:
            value = self._timings[name]
            return statistics.stdev(value) if len(value) >= 2 else math.nan
        raise KeyError(name)
