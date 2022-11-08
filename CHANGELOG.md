# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Changed

- Add type hints to tests ([#50])
- Drop explicit support for Python 3.6 ([#48])

## [1.4.0] - 2022-11-08

### Added

- `inital_text` parameter which, when present, will use logger to log that timer has been started (by [Matthew Price](https://github.com/pricemg) in [#47])

## [1.3.2] - 2022-10-07

### Added

- `__all__` to specify the public API (by [@alkatar21](https://github.com/alkatar21) in [#46])

## [1.3.1] - 2022-10-06

### Added

- A `py.typed` file to mark `codetiming` as typed as specified in [PEP 561](https://peps.python.org/pep-0561/#packaging-type-information) (by [@alkatar21](https://github.com/alkatar21) in [#38])

### Changed

- Use GitHub Actions instead of CircleCI for CI ([#33])
- Explicitly support Python 3.10 and 3.11 ([#32], [#34], [#35])

## [1.3.0] - 2021-02-09

### Added

- `text` can be a callable returning a formatted string, suggested by [@dchess](https://github.com/dchess) in [#29] ([#30]).
- Testing with [Interrogate](https://interrogate.readthedocs.io/) to enforce docstrings ([#27]).


## [1.2.0] - 2020-03-03

### Added

- Attributes that can be referenced in the `text` template string, suggested by [@mlisovyi](https://github.com/mlisovyi) in [#24] ([#25]).

### Changed

- `Timer.timers` changed from regular `dict` to a custom dictionary supporting basic statistics for named timers ([#23]).


## [1.1.0] - 2020-01-15

### Added

- `.last` attribute with the value of the last measured time (by [@janfreyberg](https://github.com/janfreyberg) in [#13]).
- `CHANGELOG.md` detailing changes made to `codetiming` since its initial publication ([#17]).
- `CONTRIBUTING.md` with guidelines on how to work with `codetiming` as a developer ([#18]).
- `AUTHORS.md` with a list of maintainers and contributors ([#18])


## [1.0.0] - 2019-12-31

Initial version of `codetiming`. Version 1.0.0 corresponds to the code in the tutorial [Python Timer Functions: Three Ways to Monitor Your Code](https://realpython.com/python-timer/).


[Unreleased]: https://github.com/realpython/codetiming/compare/v1.4.0...HEAD
[1.4.0]: https://github.com/realpython/codetiming/compare/v1.3.2...v1.4.0
[1.3.2]: https://github.com/realpython/codetiming/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/realpython/codetiming/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/realpython/codetiming/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/realpython/codetiming/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/realpython/codetiming/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/realpython/codetiming/releases/tag/v1.0.0

[#50]: https://github.com/realpython/codetiming/pull/50
[#48]: https://github.com/realpython/codetiming/pull/48
[#47]: https://github.com/realpython/codetiming/pull/47
[#46]: https://github.com/realpython/codetiming/pull/46
[#38]: https://github.com/realpython/codetiming/pull/38
[#35]: https://github.com/realpython/codetiming/pull/35
[#34]: https://github.com/realpython/codetiming/pull/34
[#33]: https://github.com/realpython/codetiming/pull/33
[#32]: https://github.com/realpython/codetiming/pull/32
[#30]: https://github.com/realpython/codetiming/pull/30
[#29]: https://github.com/realpython/codetiming/issues/29
[#27]: https://github.com/realpython/codetiming/pull/27
[#25]: https://github.com/realpython/codetiming/pull/25
[#24]: https://github.com/realpython/codetiming/issues/24
[#23]: https://github.com/realpython/codetiming/pull/23
[#18]: https://github.com/realpython/codetiming/pull/18
[#17]: https://github.com/realpython/codetiming/pull/17
[#13]: https://github.com/realpython/codetiming/pull/13
