"""Definition of Timer.

See help(codetiming) for quick instructions, and
https://pypi.org/project/codetiming/ for more details.
"""

# Standard library imports
import math
import time
from contextlib import ContextDecorator
from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar, Optional, Union

# Codetiming imports
from codetiming._timers import Timers


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class."""


@dataclass
class Timer(ContextDecorator):
    """Time your code using a class, context manager, or decorator."""

    timers: ClassVar[Timers] = Timers()
    _start_time: Optional[float] = field(default=None, init=False, repr=False)
    name: Optional[str] = None
    initial_text: Optional[Union[bool, str]] = False
    text: Union[str, Callable[[float], str]] = "Elapsed time: {:0.4f} seconds"
    logger: Optional[Callable[[str], None]] = print
    last: float = field(default=math.nan, init=False, repr=False)

    def start(self) -> None:
        """Start a new timer."""
        if self.logger and self.initial_text:
            # Generate timer init statement for logger.
            if isinstance(self.initial_text, str):
                # To include timer name in text, include {name} within string (not as f-string!).
                initial_text = self.initial_text.format(name=self.name)
            elif self.name:
                # If no custom string specified print a default statement using timer name.
                initial_text = "Timer {name} started".format(name=self.name)
            else:
                # If no custom string or timer name is specified print a default statement.
                initial_text = "Timer started"
            self.logger(initial_text)

        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer, and report the elapsed time."""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        # Calculate elapsed time
        self.last = time.perf_counter() - self._start_time
        self._start_time = None

        # Report elapsed time
        if self.logger:
            if callable(self.text):
                text = self.text(self.last)
            else:
                attributes = {
                    "name": self.name,
                    "milliseconds": self.last * 1000,
                    "seconds": self.last,
                    "minutes": self.last / 60,
                }
                text = self.text.format(self.last, **attributes)
            self.logger(text)
        if self.name:
            self.timers.add(self.name, self.last)

        return self.last

    def __enter__(self) -> "Timer":
        """Start a new timer as a context manager."""
        self.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        """Stop the context manager timer."""
        self.stop()
