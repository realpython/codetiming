# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog1.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

## [1.2.0] - 2020-03-03

### Added

- Attributes that can be referenced in the `text` template string, suggested by [@mlisovyi](https://github.com/mlisovyi) in [#24] ([#25]).

### Changed

- `Timer.timers` changed from regular to `dict` to a custom dictionary supporting basic statistics for named timers ([#23]).


## [1.1.0] - 2020-01-15

### Added

- `.last` attribute with the value of the last measured time (by [@janfreyberg](https://github.com/janfreyberg) in [#13]).
- `CHANGELOG.md` detailing changes made to `codetiming` since its initial publication ([#17]).
- `CONTRIBUTING.md` with guidelines on how to work with `codetiming` as a developer ([#18]).
- `AUTHORS.md` with a list of maintainers and contributors ([#18])


## [1.0.0] - 2019-12-31

Initial version of `codetiming`. Version 1.0.0 corresponds to the code in the tutorial [Python Timer Functions: Three Ways to Monitor Your Code](https://realpython.com/python-timer/).


[Unreleased]: https://github.com/realpython/codetiming/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/realpython/codetiming/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/realpython/codetiming/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/realpython/codetiming/releases/tag/v1.0.0

[#13]: https://github.com/realpython/codetiming/pull/13
[#17]: https://github.com/realpython/codetiming/pull/17
[#18]: https://github.com/realpython/codetiming/pull/18
[#23]: https://github.com/realpython/codetiming/pull/23
[#24]: https://github.com/realpython/codetiming/issues/24
[#25]: https://github.com/realpython/codetiming/pull/25
