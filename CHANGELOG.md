# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Add more details on how to install screenconfig
- Accept arbitrary xrandr parameters
- Add work setup to configuration
- Add description field for monitors
- Add setup.py and proper python packaging

### Changed
- Move script and configuration to screenconfig package
- Improve variable names for finding the reference output
- Update configuration
- Change file format to TOML
- Require position parameters to be real xrandr arguments, e.g.
  "--left-of" instead of "left-of"
- Rename field edid to edids
- Change indentation to spaces

### Removed
- Remove rotate option
- Remove YAML configuration
- Remove support for YAML file format
- Remove debug output

### Fixed
- Fix broken import in setup.py
