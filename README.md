[![Python Timer Functions: Three Ways to Monitor Your Code](https://files.realpython.com/media/Three-Ways-to-Time-Your-Code_Watermarked.8d561fcc7a35.jpg)](https://realpython.com/python-timer)

# `codetiming` - A flexible, customizable timer for your Python code

[![Latest version](https://img.shields.io/pypi/v/codetiming.svg)](https://pypi.org/project/codetiming/)
[![Python versions](https://img.shields.io/pypi/pyversions/codetiming.svg)](https://pypi.org/project/codetiming/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![CircleCI](https://circleci.com/gh/realpython/codetiming.svg?style=shield)](https://circleci.com/gh/realpython/codetiming)

Install `codetiming` from PyPI:

```
$ python -m pip install codetiming
```

The source code is [available at GitHub](https://github.com/realpython/codetiming).

For a complete tutorial on how `codetiming` works, see [Python Timer Functions: Three Ways to Monitor Your Code](https://realpython.com/python-timer) on [Real Python](https://realpython.com/).

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

In the template text, you can also use explicit attributes to refer to the `name` of the timer, or log the elapsed time in `milliseconds`, `seconds` (the default), or `minutes`. For example:

```python
t1 = Timer(name="NamedTimer", text="{name}: {minutes:.1f} minutes")
t2 = Timer(text="Elapsed time: {milliseconds:.0f} ms")
```

Note that the strings used by `text` are **not** f-strings. Instead they are used as templates that will be populated using `.format()` behind the scenes. If you want to combine the `text` template with an f-string, you need to use double braces for the template values:

```python
t = Timer(text=f"{__file__}: {{:.4f}}")
```


## Capturing the Elapsed Time

When using `Timer` as a class, you can capture the elapsed time when calling `.stop()`:

```python
elapsed_time = t.stop()
```

You can also find the last measured elapsed time in the `.last` attribute. The following code will have the same effect as the previous example:

```python
t.stop()
elapsed_time = t.last
```


## Named Timers

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

You can also get simple statistics about your named timers. Continuing from the example above:

```python
>>> Timer.timers.max("example")
3.5836678670002584

>>> Timer.timers.mean("example")
2.6563487200000964

>>> Timer.timers.stdev("example")
1.311427314335879
```

`timers` support `.count()`, `.total()`, `.min()`, `.max()`, `.mean()`, `.median()`, and `.stdev()`.


## Acknowledgements

`codetiming` is based on a similar module originally developed for the [Midgard Geodesy library](https://kartverket.github.io/midgard/) at the [Norwegian Mapping Authority](https://www.kartverket.no/en/).