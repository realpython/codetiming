# `codetiming` - A flexible, customizable timer for your Python code

[![Latest version](https://img.shields.io/pypi/v/codetiming.svg)](https://pypi.org/project/codetiming/)
[![Python versions](https://img.shields.io/pypi/pyversions/codetiming.svg)](https://pypi.org/project/codetiming/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![CircleCI](https://circleci.com/gh/realpython/codetiming.svg?style=shield)](https://circleci.com/gh/realpython/codetiming)

Install `codetiming` from PyPI:

```
$ python -m pip install codetiming
```

The source code is [available at GitHub](https://github.com/realpython/codetiming).


## Basic Usage

You can use `codetiming.Timer` in several different ways:

1. As a **class**:

    ```python
    t = Timer(name="class")
    t.start()
    # Do something
    t.stop()
    ```

2. As a **context manager**:

    ```python
    with Timer(name="context manager"):
        # Do something
    ```

3. As a **decorator**:

    ```python
    @Timer(name="decorator")
    def stuff():
        # Do something
    ```


## Arguments

`Timer` accepts the following arguments when it's created, all are optional:

- **`name`:** An optional name for your timer
- **`text`:** The text shown when your timer ends. It should contain a `{}` placeholder that will be filled by the elapsed time in seconds (default: `"Elapsed time: {:.4f} seconds"`)
- **`logger`:** A function/callable that takes a string argument, and will report the elapsed time when the logger is stopped (default: `print()`)

You can turn off explicit reporting of the elapsed time by setting `logger=None`.

When using `Timer` as a class, you can capture the elapsed time when calling `.stop()`:

```python
elapsed_time = t.stop()
```

Named timers are made available in the class dictionary `Timer.timers`. The elapsed time will accumulate if the same name or same timer is used several times. Consider the following example:

```python
>>> import logging
>>> from codetiming import Timer

>>> t = Timer("example", text="Time spent: {:.2f}", logger=logging.warning)

>>> t.start()
>>> t.stop()
WARNING:root:Time spent: 3.58
3.5836678670002584

>>> with t:
...     _ = list(range(100000000))
... 
WARNING:root:Time spent: 1.73

>>> Timer.timers
{'example': 5.312697440000193}
```

The example shows how you can redirect the timer output to the logging module. Note that the elapsed time spent in the two different uses of `t` has been accumulated in `Timer.timers`.


## Acknowledgements

`codetiming` is based on a similar module originally developed for the [Midgard Geodesy library](https://kartverket.github.io/midgard/) at the [Norwegian Mapping Authority](https://www.kartverket.no/en/).