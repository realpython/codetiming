"""Tests for codetiming.Timer

Based on the Pytest test runner
"""
# Standard library imports
import re

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


@Timer(text=TIME_MESSAGE)
def timewaster(num):
    """Just waste a little bit of time"""
    sum(n ** 2 for n in range(num))


@Timer(name="accumulator", text=TIME_MESSAGE)
def accumulated_timewaste(num):
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
    timewaster(1000)
    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""


def test_timer_as_context_manager(capsys):
    """Test that timed context prints timing information"""
    with Timer(text=TIME_MESSAGE):
        sum(n ** 2 for n in range(1000))
    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""


def test_explicit_timer(capsys):
    """Test that timed section prints timing information"""
    t = Timer(text=TIME_MESSAGE)
    t.start()
    sum(n ** 2 for n in range(1000))
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
        sum(n ** 2 for n in range(1000))
    assert RE_TIME_MESSAGE.match(logger.messages)


def test_timer_without_text(capsys):
    """Test that timer with logger=None does not print anything"""
    with Timer(logger=None):
        sum(n ** 2 for n in range(1000))

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""


def test_accumulated_decorator(capsys):
    """Test that decorated timer can accumulate"""
    accumulated_timewaste(1000)
    accumulated_timewaste(1000)

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
        sum(n ** 2 for n in range(1000))
    with t:
        sum(n ** 2 for n in range(1000))

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
    sum(n ** 2 for n in range(1000))
    total += t.stop()
    t.start()
    sum(n ** 2 for n in range(1000))
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
