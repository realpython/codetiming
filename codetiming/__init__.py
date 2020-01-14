"""A flexible, customizable timer for your Python code

You can use `codetiming.Timer` in several different ways:

1. As a **class**:

    t = Timer(name="class")
    t.start()
    # Do something
    t.stop()

2. As a **context manager**:

    with Timer(name="context manager"):
        # Do something

3. As a **decorator**:

    @Timer(name="decorator")
    def stuff():
        # Do something
"""

# Codetiming imports
from codetiming._timer import Timer, TimerError  # noqa

# Versioning is handled by bump2version
__version__ = "1.0.0"
