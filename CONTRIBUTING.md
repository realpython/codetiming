# Contributing to `codetiming`

Thank you for considering to contribute to `codetiming`. This guide is meant to help you find your way around the project, and let you know which standards that are used.

If you are looking for tutorials or tips on how to use `codetiming`, have a look at the [documentation](https://github.com/realpython/codetiming/blob/master/README.md) and the accompanying article [Python Timer Functions: Three Ways to Monitor Your Code](https://realpython.com/python-timer/).


# Reporting Issues or Suggesting New Features

Have you found an issue with `codetiming`, or do you have a suggestion for a new feature? Great! Have a look at the [known issues](https://github.com/realpython/codetiming/issues/new) to see if anyone has reported it already. If not, please post a [new issue](https://github.com/realpython/codetiming/issues/new).

When reporting an issue, please include as much of the following information as possible:

- Your version of `codetiming`: `print(codetiming.__version__)`
- Your version of Python: `print(sys.version)`
- Your operating system
- A description of your issue, ideally including a short code snippet that reproduces the issue

When suggesting a new feature, try to include an example of how your feature could be used.


# Contributing Code

Do you want to contribute code to `codetiming`? Fantastic! We welcome contributions as **pull requests**.


## Setting Up Your Environment

`codetiming` uses [`flit`](https://flit.readthedocs.io) for package management. You should first install `flit`:

```
$ python -m pip install flit
```

You can then install `codetiming` locally for development with `flit`:

```
$ python -m flit install --pth-file --deps all
```

This will install `codetiming` and all its dependencies, including development tools like [`black`](https://black.readthedocs.io) and [`mypy`](http://mypy-lang.org/). The `--pth-file` option allows you to test your changes without reinstalling. On Linux and Mac, you can use `--symlink` for the same effect.


## Running Tests

Run tests using [`tox`](https://tox.readthedocs.io/). `tox` helps to enforce the following principles:

- Consistent code style using [`black`](https://black.readthedocs.io). You can automatically format your code as follows:

    ```
    $ black codetiming/
    ```

- Static type hinting using [`mypy`](http://mypy-lang.org/). Test your type hints as follows:

    ```
    $ mypy --strict codetiming/
    ```

    See Real Python's [Python Type Checking guide](https://realpython.com/python-type-checking/) for more information.

- Unit testing using [`pytest`](https://docs.pytest.org/). You can run your tests and see a coverage report as follows:

    ```
    $ pytest --cov=codetiming --cov-report=term-missing
    ```

- All modules, functions, classes, and methods must have docstrings. This is enforced by [Interrogation](https://interrogate.readthedocs.io/). You can test compliance as follows:

    ```
    $ interrogate -c pyproject.toml -vv
    ```

Feel free to ask for help in your PR if you are having challenges with any of these tests.