# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.4] - 2024-11-27

### Added

- Added `id` field with UUID to each HourlyLmp on data retrieval.

## [0.0.3] - 2024-11-25

### Changed

- Changed synchronous HTTP GET calls to ISO New England to async requests per day.

## [0.0.2] - 2024-11-21

### Added

- Added detailed instructions for running on MacOS.
- Added functionality to aggregate data by hour (default), day, month, or year.

### Fixed

- Fixed `main()` function to correctly call the `collect()` function.
- Fixed `conver_to_csv` paramter of the `collect()` function to be correctly named `convert_to_csv`.

## [0.0.1] - 2024-11-16

### Added

- Initial functionality

[unreleased]: https://github.com/danieljmehler/iso-newengland/compare/0.0.4...HEAD
[0.0.4]: https://github.com/danieljmehler/iso-newengland/compare/0.0.2...0.0.4
[0.0.3]: https://github.com/danieljmehler/iso-newengland/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/danieljmehler/iso-newengland/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/danieljmehler/iso-newengland/releases/tag/0.0.1
