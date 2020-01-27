"""Dictionary-like structure with information about timers"""

# Standard library imports
import collections
import math
import statistics
from typing import Any, Callable, Dict, List, Optional


class Timers(collections.UserDict):
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

    def apply(
        self, func: Callable[[List[float]], float], name: Optional[str] = None
    ) -> float:
        """Apply function to timings"""
        if name is None:
            return {k: func(v) for k, v in self._timings.items()}
        if name in self._timings:
            return func(self._timings[name])
        raise KeyError(name)

    def count(self, name: Optional[str] = None) -> float:
        """Number of timings"""
        return self.apply(len, name=name)

    def total(self, name: Optional[str] = None) -> float:
        """Total time for timers"""
        return self.apply(sum, name=name)

    def min(self, name=None):
        """Minimal value of timings"""
        return self.apply(lambda values: min(values or [0]), name=name)

    def max(self, name=None):
        """Maximal value of timings"""
        return self.apply(lambda values: max(values or [0]), name=name)

    def mean(self, name=None):
        """Mean value of timings"""
        return self.apply(lambda values: statistics.mean(values or [0]), name=name)

    def median(self, name=None):
        """Median value of timings"""
        return self.apply(lambda values: statistics.median(values or [0]), name=name)

    def stdev(self, name=None):
        """Standard deviation of timings"""
        if name is None:
            return {
                k: statistics.stdev(v) if len(v) >= 2 else math.nan
                for k, v in self._timings.items()
            }
        if name in self._timings:
            value = self._timings[name]
            return statistics.stdev(value) if len(value) >= 2 else math.nan
        raise KeyError(name)
