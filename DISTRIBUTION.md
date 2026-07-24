# Distribution & Adoption

How Squire reaches developers, and how adoption is measured without violating the
anti-vision. Squire has **no telemetry** — no phone-home, no install pings, no analytics.
That is a settled position ([VISION.md](VISION.md) anti-vision), not a gap to be closed.
This document defines what adoption *is* measured by instead.

---

## Distribution Channels

Squire ships three ways, in increasing weight:

1. **Single-file curl.** The core artifact, `squire.md`, copied into a project root or
   `~/.claude/CLAUDE.md`. No installer, no directory, one file.
   ```bash
   curl -fsSL https://raw.githubusercontent.com/eddiebelaval/squire/main/squire.md -o squire.md
   ```
2. **Full installer.** `./install.sh` places commands, skills, agents, and pipeline files.
   Supports `--dry-run`, `--commands-only`, and `--uninstall`.
3. **Cherry-pick.** Clone or download the repo and copy the directories you want
   (`commands/`, `skills/`, `prompts/`). Components are independent by design.

Announcement surfaces: GitHub, Reddit (see `reddit-post.md`), Hacker News, and X
([@eddiebe](https://x.com/eddiebe)).

---

## How Adoption Is Measured

Because there is no telemetry, adoption is read from **GitHub-native, public signals** that
require no code in the toolkit and no data collection from users:

| Signal | What it indicates | Where to read it |
|--------|-------------------|------------------|
| **Stars** | Passive interest / bookmarking | Repo header |
| **Forks** | Intent to use or modify | Repo header, Insights → Forks |
| **Dependency graph / "Used by"** | Repos that reference Squire | Insights → Dependency graph |
| **Traffic (clones, unique visitors)** | Actual pull-through, 14-day window | Insights → Traffic (maintainer-only) |
| **Discussions activity** | Live community engagement | Discussions tab |
| **Issues & PRs opened by non-maintainers** | Contributor pull-through | Issues / PRs, filtered by author |
| **Inbound links & mentions** | Organic distribution | Reddit/HN/X threads, search |

These are the honest metrics for a no-telemetry, file-based toolkit. They undercount
(curl installs and cherry-picks are invisible) and that is an accepted trade: privacy and
zero-lock-in beat a precise install count.

### What we do NOT do

- No install beacons, no `curl | sh` that reports back, no analytics pixel in any file.
- No accounts, no registration, no "sign up to use."
- No proprietary registry. GitHub is the registry.

---

## Release & Versioning

Squire is versioned so distributors and contributors can point at a known state. Changes
are recorded in [CHANGELOG.md](CHANGELOG.md). Because Squire has no build artifact, a
"release" is simply a tagged commit plus a changelog entry — no packaging step, no binary.

---

## Adoption Goals

Adoption is directional, not a KPI dashboard. The signals above are reviewed periodically
and summarized in the [BUILDING.md](BUILDING.md) status section. The bar for the
Community & Distribution pillar is not a number of stars — it is whether an external
developer can find Squire, understand it, install it, get help, and contribute back
without ever talking to the maintainer. Every file in this community layer exists to make
that path complete.

Last reviewed: 2026-07-08.
