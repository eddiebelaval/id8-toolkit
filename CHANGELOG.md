# Changelog

All notable changes to Squire are recorded here. Squire has no build artifact, so a
release is a tagged commit plus an entry in this file. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); dates are ISO (YYYY-MM-DD).

## [Unreleased]

### Added
- **Community & Distribution layer.** Brought the full file-based community layer onto the
  default branch: contributor guidelines (`CONTRIBUTING.md`), GitHub issue templates
  (bug report, feature request, skill submission), and a PR template — built earlier but
  never merged to `main`.
- **`GOVERNANCE.md`** — benevolent-maintainer governance model, decision process, and the
  principles that constrain governance.
- **`CODE_OF_CONDUCT.md`** — extracted and expanded from the inline section in
  `CONTRIBUTING.md` into a recognized standalone file.
- **`SUPPORT.md`** — where to get help; establishes GitHub Discussions as the community
  channel (the file-based project's file-based forum).
- **`DISTRIBUTION.md`** — distribution channels and the no-telemetry, GitHub-native
  adoption signals used in place of install tracking.
- **`.github/ISSUE_TEMPLATE/config.yml`** — routes questions to Discussions and points
  contributors at the support and contributing docs.

### Changed
- `CONTRIBUTING.md` now references `CODE_OF_CONDUCT.md` instead of carrying the conduct
  rules inline.
- Triad updated: `VISION.md` pillar 6 (Community & Distribution) advanced from PARTIAL 55%
  to PARTIAL 80%; `SPEC.md` and `BUILDING.md` updated to reflect the shipped community
  layer.

## [0.1.0] - 2026-03-18

### Added
- Initial public release of Squire on GitHub: the `squire.md` behavioral ruleset (9 rules),
  63 slash commands, 328 skills, 34 custom agents, the 11-stage pipeline, 7 behavioral
  patterns, 6 thinking frameworks, the Triad documentation system, workspace generators,
  the `install.sh` installer, MIT license, and README.
