# Changelog

All notable changes to Squire are recorded here. Squire has no build artifact, so a
release is a tagged commit plus an entry in this file. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); dates are ISO (YYYY-MM-DD).

## [0.2.1] - 2026-08-16

### Added
- **2 skills** (346 -> 348): `retro` (portable engineering-retrospective scanner,
  auto-detects git identity) and `epistemic-matrix` (Rumsfeld four-quadrant blind-spot
  audit). Both cleared the leak scan; `epistemic-matrix` had one proper noun genericized.

### Held (not published, by design)
- `learning-loop` and the `sell-*` family were evaluated for inclusion and **withheld**:
  their substance is client-confidential (named deals, deal sizes, client internal
  politics, partners). Genericizing them would leave a hollow shell and still risk
  outing clients, so they stay private.

## [0.2.0] - 2026-08-16

Growth refresh. Six months of daily use since the initial release, curated for public
distribution (client-derived and personal components held back).

### Added
- **17 commands** (63 -> 80): `3pv`, `editorial-swarm`, `finish`, `kb-compile`,
  `kb-extract`, `kb-ingest`, `kb-lint`, `kb-query`, `kb-search`, `loud`, `memory-ingest`,
  `memory-lint`, `quiet`, `ralph-loop`, `recap`, `simplify`, `thrift`.
- **21 skills** (325 -> 346): `automation-architect`, `community-builder`,
  `competitor-tracker`, `copywriter`, `document-design-foundation`, `dslop`, `gauntlet`,
  `graphic-designer`, `make-interfaces-feel-better`, `performance-profiler`,
  `pitch-deck-builder`, `plan-ceo-review`, `referral-program-designer`, `review`,
  `skill-audit`, `social-caption-writer`, `social-post-creator`, `terminal-ui-design`,
  `two-stage-review`, `creator-partnership-manager`, `remote-event-prep`.
- **1 agent** (34 -> 35): `editor-in-chief`.

### Changed
- Component counts refreshed to match actual repo contents: **80 commands, 346 skills,
  35 agents** (README component table and metrics table).
- **Metrics moved to a verifiable, reproducible basis.** Replaced the frozen
  "2,990 sessions / 3,307 commits" figure (set 2026-03-12, never recomputed) with
  **19,030 default-branch commits across 104 repositories, March--August 2026** -- a
  number anyone can reproduce by summing `git rev-list --count HEAD` across the
  development tree. Reconciled `squire.md`, which separately claimed
  "1,075 sessions / 3,667 commits." The original ~3,000 analyzed sessions are preserved
  as dated v1-corpus provenance, not a current live count.

### Notes
- Every added component passed a two-pass leak scan (client names, third-party people,
  contact info, secrets) before inclusion. Client- and person-specific tooling
  (forward-deployment doctrine, brand-genome/halo systems, voice/craft personas,
  client-call loops) is deliberately withheld from the public toolkit.

## [0.1.0] - 2026-03-18

### Added
- Initial public release of Squire on GitHub: the `squire.md` behavioral ruleset (9 rules),
  63 slash commands, 328 skills, 34 custom agents, the 11-stage pipeline, 7 behavioral
  patterns, 6 thinking frameworks, the Triad documentation system, workspace generators,
  the `install.sh` installer, MIT license, and README.
