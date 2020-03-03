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
# Test functions
#
TIME_PREFIX = "Wasted time:"
TIME_MESSAGE = f"{TIME_PREFIX} {{:.4f}} seconds"
RE_TIME_MESSAGE = re.compile(TIME_PREFIX + r" 0\.\d{4} seconds")


def waste_time(num=1000):
    """Just waste a little bit of time"""
    sum(n ** 2 for n in range(num))


@Timer(text=TIME_MESSAGE)
def decorated_timewaste(num=1000):
    """Just waste a little bit of time"""
    sum(n ** 2 for n in range(num))


@Timer(name="accumulator", text=TIME_MESSAGE)
def accumulated_timewaste(num=1000):
    """Just waste a little bit of time"""
    sum(n ** 2 for n in range(num))


class CustomLogger:
    """Simple class used to test custom logging capabilities in Timer"""

    def __init__(self):
        self.messages = ""

    def __call__(self, message):
        self.messages += message


#
# Tests
#
def test_timer_as_decorator(capsys):
    """Test that decorated function prints timing information"""
    decorated_timewaste()
    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""


def test_timer_as_context_manager(capsys):
    """Test that timed context prints timing information"""
    with Timer(text=TIME_MESSAGE):
        waste_time()
    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""


def test_explicit_timer(capsys):
    """Test that timed section prints timing information"""
    t = Timer(text=TIME_MESSAGE)
    t.start()
    waste_time()
    t.stop()
    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""


def test_error_if_timer_not_running():
    """Test that timer raises error if it is stopped before started"""
    t = Timer(text=TIME_MESSAGE)
    with pytest.raises(TimerError):
        t.stop()


def test_access_timer_object_in_context(capsys):
    """Test that we can access the timer object inside a context"""
    with Timer(text=TIME_MESSAGE) as t:
        assert isinstance(t, Timer)
        assert t.text.startswith(TIME_PREFIX)
    _, _ = capsys.readouterr()  # Do not print log message to standard out


def test_custom_logger():
    """Test that we can use a custom logger"""
    logger = CustomLogger()
    with Timer(text=TIME_MESSAGE, logger=logger):
        waste_time()
    assert RE_TIME_MESSAGE.match(logger.messages)


def test_timer_without_text(capsys):
    """Test that timer with logger=None does not print anything"""
    with Timer(logger=None):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""


def test_accumulated_decorator(capsys):
    """Test that decorated timer can accumulate"""
    accumulated_timewaste()
    accumulated_timewaste()

    stdout, stderr = capsys.readouterr()
    lines = stdout.strip().split("\n")
    assert len(lines) == 2
    assert RE_TIME_MESSAGE.match(lines[0])
    assert RE_TIME_MESSAGE.match(lines[1])
    assert stderr == ""


def test_accumulated_context_manager(capsys):
    """Test that context manager timer can accumulate"""
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


def test_accumulated_explicit_timer(capsys):
    """Test that explicit timer can accumulate"""
    t = Timer(name="accumulated_explicit_timer", text=TIME_MESSAGE)
    total = 0
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


def test_error_if_restarting_running_timer():
    """Test that restarting a running timer raises an error"""
    t = Timer(text=TIME_MESSAGE)
    t.start()
    with pytest.raises(TimerError):
        t.start()


def test_last_starts_as_nan():
    """Test that .last attribute is initialized as nan"""
    t = Timer()
    assert math.isnan(t.last)


def test_timer_sets_last():
    """Test that .last attribute is properly set"""
    with Timer() as t:
        time.sleep(0.02)

    assert t.last >= 0.02


def test_using_name_in_text_without_explicit_timer(capsys):
    """Test that the name of the timer can be referenced in the text"""
    name = "NamedTimer"
    with Timer(name=name, text="{name}: {:.2f}"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert re.match(f"{name}: " + r"0\.\d{2}", stdout)


def test_using_name_in_text_with_explicit_timer(capsys):
    """Test that the name of the timer and the seconds attribute can be referenced in the text"""
    name = "NamedTimer"
    with Timer(name=name, text="{name}: {seconds:.2f}"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert re.match(f"{name}: " + r"0\.\d{2}", stdout.strip())


def test_using_minutes_attribute_in_text(capsys):
    """Test that timer can report its duration in minutes"""
    with Timer(text="{minutes:.1f} minutes"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert stdout.strip() == "0.0 minutes"


def test_using_milliseconds_attribute_in_text(capsys):
    """Test that timer can report its duration in milliseconds"""
    with Timer(text="{milliseconds:.0f} {seconds:.3f}"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    milliseconds, _, seconds = stdout.partition(" ")
    assert int(milliseconds) == round(float(seconds) * 1000)


def test_timers_cleared():
    """Test that timers can be cleared"""
    with Timer(name="timer_to_be_cleared"):
        waste_time()

    assert "timer_to_be_cleared" in Timer.timers
    Timer.timers.clear()
    assert not Timer.timers


def test_running_cleared_timers():
    """Test that timers can still be run after they're cleared"""
    t = Timer(name="timer_to_be_cleared")
    Timer.timers.clear()

    accumulated_timewaste()
    with t:
        waste_time()

    assert "accumulator" in Timer.timers
    assert "timer_to_be_cleared" in Timer.timers


def test_timers_stats():
    """Test that we can get basic statistics from timers"""
    name = "timer_with_stats"
    t = Timer(name=name)
    for num in range(5, 10):
        with t:
            waste_time(num=100 * num)

    stats = Timer.timers
    assert stats.total(name) == stats[name]
    assert stats.count(name) == 5
    assert stats.min(name) <= stats.median(name) <= stats.max(name)
    assert stats.mean(name) >= stats.min(name)
    assert stats.stdev(name) >= 0


def test_stats_missing_timers():
    """Test that getting statistics from non-existent timers raises exception"""
    with pytest.raises(KeyError):
        Timer.timers.count("non_existent_timer")

    with pytest.raises(KeyError):
        Timer.timers.stdev("non_existent_timer")


def test_setting_timers_exception():
    """Test that setting .timers items raises exception"""
    with pytest.raises(TypeError):
        Timer.timers["set_timer"] = 1.23
