"""Tests for codetiming.Timer

Based on the Pytest test runner
"""
# Standard library imports
import math
import re
import time

# Third party imports
import pytest

# Codetiming imports
from codetiming import Timer, TimerError

#
# Constants, functions, and classes used by tests
#
TIME_PREFIX = "Wasted time:"
TIME_MESSAGE = f"{TIME_PREFIX} {{:.4f}} seconds"
RE_TIME_MESSAGE = re.compile(TIME_PREFIX + r" 0\.\d{4} seconds")
RE_TIME_MESSAGE_INITIAL_TEXT_TRUE = re.compile(
    f"Timer started\n{TIME_PREFIX}" + r" 0\.\d{4} seconds"
)
RE_TIME_MESSAGE_INITIAL_TEXT_CUSTOM = re.compile(
    f"Starting the party\n{TIME_PREFIX}" + r" 0\.\d{4} seconds"
)


def waste_time(num: int = 1000) -> None:
    """Just waste a little bit of time."""
    sum(n**2 for n in range(num))


@Timer(text=TIME_MESSAGE)
def decorated_timewaste(num: int = 1000) -> None:
    """Just waste a little bit of time."""
    sum(n**2 for n in range(num))


@Timer(text=TIME_MESSAGE, initial_text=True)
def decorated_timewaste_initial_text_true(num: int = 1000) -> None:
    """Just waste a little bit of time."""
    sum(n**2 for n in range(num))


@Timer(text=TIME_MESSAGE, initial_text="Starting the party")
def decorated_timewaste_initial_text_custom(num: int = 1000) -> None:
    """Just waste a little bit of time."""
    sum(n**2 for n in range(num))


@Timer(name="accumulator", text=TIME_MESSAGE)
def accumulated_timewaste(num: int = 1000) -> None:
    """Just waste a little bit of time."""
    sum(n**2 for n in range(num))


class CustomLogger:
    """Simple class used to test custom logging capabilities in Timer."""

    def __init__(self) -> None:
        """Store log messages in the .messages attribute."""
        self.messages = ""

    def __call__(self, message: str) -> None:
        """Add a log message to the .messages attribute."""
        self.messages += message


#
# Tests
#
def test_timer_as_decorator(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that decorated function prints timing information."""
    decorated_timewaste()

    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""


def test_timer_as_context_manager(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that timed context prints timing information."""
    with Timer(text=TIME_MESSAGE):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""


def test_explicit_timer(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that timed section prints timing information."""
    t = Timer(text=TIME_MESSAGE)
    t.start()
    waste_time()
    t.stop()

    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""


def test_error_if_timer_not_running() -> None:
    """Test that timer raises error if it is stopped before started."""
    t = Timer(text=TIME_MESSAGE)
    with pytest.raises(TimerError):
        t.stop()


def test_access_timer_object_in_context(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that we can access the timer object inside a context."""
    with Timer(text=TIME_MESSAGE) as t:
        assert isinstance(t, Timer)
        assert isinstance(t.text, str)
        assert t.text.startswith(TIME_PREFIX)
    _, _ = capsys.readouterr()  # Do not print log message to standard out


def test_custom_logger() -> None:
    """Test that we can use a custom logger."""
    logger = CustomLogger()
    with Timer(text=TIME_MESSAGE, logger=logger):
        waste_time()
    assert RE_TIME_MESSAGE.match(logger.messages)


def test_timer_without_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that timer with logger=None does not print anything."""
    with Timer(logger=None):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""


def test_accumulated_decorator(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that decorated timer can accumulate."""
    accumulated_timewaste()
    accumulated_timewaste()

    stdout, stderr = capsys.readouterr()
    lines = stdout.strip().split("\n")
    assert len(lines) == 2
    assert RE_TIME_MESSAGE.match(lines[0])
    assert RE_TIME_MESSAGE.match(lines[1])
    assert stderr == ""


def test_accumulated_context_manager(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that context manager timer can accumulate."""
    t = Timer(name="accumulator", text=TIME_MESSAGE)
    with t:
        waste_time()
    with t:
        waste_time()

    stdout, stderr = capsys.readouterr()
    lines = stdout.strip().split("\n")
    assert len(lines) == 2
    assert RE_TIME_MESSAGE.match(lines[0])
    assert RE_TIME_MESSAGE.match(lines[1])
    assert stderr == ""


def test_accumulated_explicit_timer(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that explicit timer can accumulate."""
    t = Timer(name="accumulated_explicit_timer", text=TIME_MESSAGE)
    total = 0.0
    t.start()
    waste_time()
    total += t.stop()
    t.start()
    waste_time()
    total += t.stop()

    stdout, stderr = capsys.readouterr()
    lines = stdout.strip().split("\n")
    assert len(lines) == 2
    assert RE_TIME_MESSAGE.match(lines[0])
    assert RE_TIME_MESSAGE.match(lines[1])
    assert stderr == ""
    assert total == Timer.timers["accumulated_explicit_timer"]


def test_error_if_restarting_running_timer() -> None:
    """Test that restarting a running timer raises an error."""
    t = Timer(text=TIME_MESSAGE)
    t.start()
    with pytest.raises(TimerError):
        t.start()


def test_last_starts_as_nan() -> None:
    """Test that .last attribute is initialized as nan."""
    t = Timer()
    assert math.isnan(t.last)


def test_timer_sets_last() -> None:
    """Test that .last attribute is properly set."""
    with Timer(logger=None) as t:
        time.sleep(0.02)

    assert t.last >= 0.02


def test_using_name_in_text_without_explicit_timer(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that the name of the timer can be referenced in the text."""
    name = "NamedTimer"
    with Timer(name=name, text="{name}: {:.2f}"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert re.match(f"{name}: " + r"0\.\d{2}", stdout)
    assert stderr == ""


def test_using_name_in_text_with_explicit_timer(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that timer name and seconds attribute can be referenced in the text."""
    name = "NamedTimer"
    with Timer(name=name, text="{name}: {seconds:.2f}"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert re.match(f"{name}: " + r"0\.\d{2}", stdout.strip())
    assert stderr == ""


def test_using_minutes_attribute_in_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that timer can report its duration in minutes."""
    with Timer(text="{minutes:.1f} minutes"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert stdout.strip() == "0.0 minutes"
    assert stderr == ""


def test_using_milliseconds_attribute_in_text(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that timer can report its duration in milliseconds."""
    with Timer(text="{milliseconds:.0f} {seconds:.3f}"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    milliseconds, _, seconds = stdout.partition(" ")
    assert int(milliseconds) == round(float(seconds) * 1000)
    assert stderr == ""


def test_text_formatting_function(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that text can be formatted by a separate function."""

    def format_text(seconds: float) -> str:
        """Function that returns a formatted text"""
        return f"Function: {seconds + 1:.0f}"

    with Timer(text=format_text):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert stdout.strip() == "Function: 1"
    assert not stderr.strip()


def test_text_formatting_class(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that text can be formatted by a separate class."""

    class TextFormatter:
        """Class that behaves like a formatted text."""

        def __init__(self, seconds: float) -> None:
            """Store the elapsed number of seconds"""
            self.seconds = seconds

        def __str__(self) -> str:
            """Represent the class as a formatted text"""
            return f"Class: {self.seconds + 1:.0f}"

    with Timer(text=TextFormatter):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert stdout.strip() == "Class: 1"
    assert not stderr.strip()


def test_timers_cleared() -> None:
    """Test that timers can be cleared."""
    with Timer(name="timer_to_be_cleared", logger=None):
        waste_time()

    assert "timer_to_be_cleared" in Timer.timers
    Timer.timers.clear()
    assert not Timer.timers


def test_running_cleared_timers(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that timers can still be run after they're cleared."""
    t = Timer(name="timer_to_be_cleared")
    Timer.timers.clear()

    accumulated_timewaste()
    with t:
        waste_time()

    capsys.readouterr()
    assert "accumulator" in Timer.timers
    assert "timer_to_be_cleared" in Timer.timers


def test_timers_stats() -> None:
    """Test that we can get basic statistics from timers."""
    name = "timer_with_stats"
    t = Timer(name=name, logger=None)
    for num in range(5, 10):
        with t:
            waste_time(num=100 * num)

    stats = Timer.timers
    assert stats.total(name) == stats[name]
    assert stats.count(name) == 5
    assert stats.min(name) <= stats.median(name) <= stats.max(name)
    assert stats.mean(name) >= stats.min(name)
    assert stats.stdev(name) >= 0


def test_stats_missing_timers() -> None:
    """Test that getting statistics from non-existent timers raises exception."""
    with pytest.raises(KeyError):
        Timer.timers.count("non_existent_timer")

    with pytest.raises(KeyError):
        Timer.timers.stdev("non_existent_timer")


def test_setting_timers_exception() -> None:
    """Test that setting .timers items raises exception."""
    with pytest.raises(TypeError):
        Timer.timers["set_timer"] = 1.23


def test_timer_as_decorator_with_initial_text_true(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that decorated function prints at start with default initial text."""
    decorated_timewaste_initial_text_true()

    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE_INITIAL_TEXT_TRUE.match(stdout)
    assert stdout.count("\n") == 2
    assert stderr == ""


def test_timer_as_context_manager_with_initial_text_true(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that timed context prints at start with default initial text."""
    with Timer(text=TIME_MESSAGE, initial_text=True):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE_INITIAL_TEXT_TRUE.match(stdout)
    assert stdout.count("\n") == 2
    assert stderr == ""


def test_explicit_timer_with_initial_text_true(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that timed section prints at start with default initial text."""
    t = Timer(text=TIME_MESSAGE, initial_text=True)
    t.start()
    waste_time()
    t.stop()

    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE_INITIAL_TEXT_TRUE.match(stdout)
    assert stdout.count("\n") == 2
    assert stderr == ""


def test_timer_as_decorator_with_initial_text_custom(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that decorated function prints at start with custom initial text."""
    decorated_timewaste_initial_text_custom()

    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE_INITIAL_TEXT_CUSTOM.match(stdout)
    assert stdout.count("\n") == 2
    assert stderr == ""


def test_timer_as_context_manager_with_initial_text_custom(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that timed context prints at start with custom initial text."""
    with Timer(text=TIME_MESSAGE, initial_text="Starting the party"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE_INITIAL_TEXT_CUSTOM.match(stdout)
    assert stdout.count("\n") == 2
    assert stderr == ""


def test_explicit_timer_with_initial_text_custom(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test that timed section prints at start with custom initial text."""
    t = Timer(text=TIME_MESSAGE, initial_text="Starting the party")
    t.start()
    waste_time()
    t.stop()

    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE_INITIAL_TEXT_CUSTOM.match(stdout)
    assert stdout.count("\n") == 2
    assert stderr == ""


def test_explicit_timer_with_initial_text_true_with_name(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test with default initial text referencing timer name."""
    t = Timer(name="named", text=TIME_MESSAGE, initial_text=True)
    t.start()
    waste_time()
    t.stop()

    stdout, stderr = capsys.readouterr()
    assert re.match(
        f"Timer named started\n{TIME_PREFIX}" + r" 0\.\d{4} seconds", stdout
    )
    assert stdout.count("\n") == 2
    assert stderr == ""


def test_explicit_timer_with_initial_text_with_name(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test with custom initial text referencing timer name."""
    t = Timer(name="the party", text=TIME_MESSAGE, initial_text="Starting {name}")
    t.start()
    waste_time()
    t.stop()

    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE_INITIAL_TEXT_CUSTOM.match(stdout)
    assert stdout.count("\n") == 2
    assert stderr == ""
