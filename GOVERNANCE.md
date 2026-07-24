# Governance

Squire is a file-based toolkit, and its governance is file-based too. There is no
foundation, no steering committee, and no membership tiers. This document describes
how decisions get made, who makes them, and how that can change as the project grows.

The goal is not bureaucracy. It is to make the project legible to contributors: if you
submit a skill, a command, or a rule, you should know who decides, on what basis, and
how long it takes.

---

## Roles

| Role | Who | Responsibility |
|------|-----|----------------|
| **Maintainer** | Eddie Belaval ([@eddiebe](https://x.com/eddiebe)) | Final say on what lands, sets project direction, reviews and merges PRs, cuts releases. |
| **Contributor** | Anyone who opens an issue or PR | Proposes skills, commands, agents, rules, fixes, and docs. |
| **Reviewer** | Contributors invited by the maintainer | Trusted contributors who help triage issues and review PRs. Advisory, not binding. |

Squire currently runs on a **benevolent-maintainer** model: one maintainer with final
authority, operating transparently and in public. This is the honest state of the
project, not an aspiration. As sustained contributors emerge, the maintainer may invite
Reviewers and, eventually, co-maintainers with merge rights.

---

## How Decisions Get Made

Every change follows the same path, documented in [CONTRIBUTING.md](CONTRIBUTING.md):

1. **Issue first.** A contributor opens an issue describing the change and the real
   problem it solves. Discussion happens in the open.
2. **Alignment check.** The maintainer (or a Reviewer) checks the proposal against the
   [VISION.md](VISION.md) anti-vision and design principles. A change that adds runtime
   dependencies, a server, a build step, or model-specific tricks is declined regardless
   of quality — those are settled positions, not per-PR debates.
3. **Contribution.** The contributor forks, branches, follows the existing patterns, and
   opens a PR referencing the issue.
4. **Review and merge.** The maintainer reviews for fit, simplicity, and grounding in
   real usage, then merges or requests changes.

For the rare irreversible or identity-defining decision (renaming the project, changing
the license, altering the anti-vision), the maintainer decides in public and records the
rationale in the relevant Triad document's evolution log.

---

## Principles That Constrain Governance

Governance does not get to override the project's design principles. Specifically:

- **The anti-vision is not negotiable per-PR.** No runtime dependencies, no server, no
  accounts, no telemetry, no lock-in. See [VISION.md](VISION.md).
- **Files over infrastructure.** Governance itself is a file. If governing Squire ever
  requires a platform, a bot, or a paid service, something has gone wrong.
- **Transparency by default.** Decisions, and the reasoning behind them, happen in public
  issues and PRs — not in DMs.

---

## Changing This Document

Governance evolves as the contributor base does. Proposed changes to this file go through
the same issue-first process as any other change. Material changes are recorded in
[CHANGELOG.md](CHANGELOG.md).

Last reviewed: 2026-07-08.
