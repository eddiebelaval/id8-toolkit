# BUILDING.md — Squire

> How the most complete Claude Code toolkit was built, one friction pattern at a time.

Last updated: 2026-07-08

---

## Origin (Oct 2025 - Jan 2026)

Squire did not start as a toolkit. It started as a single file -- `CLAUDE.md` -- in Eddie Belaval's global config. Every time an AI agent wasted a session (planning instead of building, pushing broken code, dismissing visual bugs), the fix was written down as a rule. After 161 sessions across 8 days in February 2026, the first formal analysis identified 56 wrong-approach incidents, 35 buggy-code incidents, and 15+ plan-then-stall sessions. Those patterns became the 9 behavioral rules.

## The 9 Rules

The behavioral ruleset emerged from data, not theory. Each rule addresses a specific, measured failure mode:

1. Default to implementation (agent plans endlessly)
2. Plan means plan (user asks for plan, gets audit)
3. Preflight before push (broken code pushed without checks)
4. Investigate bugs directly (errors dismissed as "stale cache")
5. Scope changes to target (one-project change applied globally)
6. Verify after each edit (batch edits create cascading errors)
7. Visual output verification (agent re-reads CSS instead of checking rendered output)
8. Check your environment (CLI runs against wrong project)
9. Don't over-engineer (simple feature gets unnecessary abstractions)

## Slash Commands (Jan - Mar 2026)

Commands were extracted from repeated prompt patterns. `/ship` came from the 20+ times Eddie typed the same deploy sequence. `/visualize` came from wanting consistent HTML architecture diagrams. Each command crystallized a workflow that was being done manually into a reusable prompt file.

Key commands by emergence order:
- `/visualize` and `/blueprint` -- the first two, originally in their own repo (claude-code-visualize)
- `/ship` -- full delivery pipeline: preflight, commit, push, PR, merge
- `/research` -- research orchestrator with queue and compound operations
- `/morning` -- daily standup brief across all active projects
- `/reconcile` -- Triad document maintenance with drift detection

## Skills Library (Feb - Mar 2026)

328 skills across 17 domains. Built by identifying every type of specialized work done across 12+ products and encoding domain expertise into prompt files. The skills cover engineering (frontend, backend, architecture, DevOps), business (marketing, finance, startup, operations), and creative (content, design, UX, writing) domains.

## The Triad (Mar 2026)

A three-document system replacing PRDs: VISION.md (future), SPEC.md (present), BUILDING.md (past). The gap between VISION and SPEC IS the roadmap. Any two documents can reconstruct the third. Self-correcting -- when one drifts, the others expose it. Self-installing via `BUILDING-SETUP.md`.

## Pipeline (Feb - Mar 2026)

The 11-stage build system was derived from shipping 12+ products through the same sequence. Each stage has a gate question, agent-native additions, and branch hygiene rules. The pipeline enforces discipline without requiring a project management tool.

## The Numbers

| Metric | Count |
|--------|-------|
| Sessions analyzed | 2,990 |
| Commits analyzed | 3,307 |
| Products shipped using these patterns | 12+ |
| Duration | 5 months (Oct 2025 - Mar 2026) |
| Skills built | 328 |
| Slash commands | 63 |
| Custom agents | 34 |

## Community & Distribution Layer (Jul 2026)

The Community & Distribution pillar read as "partially shipped" for a non-obvious reason:
the community infrastructure had been **built but never merged to the default branch**. A
prior heal session (Mar 2026) authored `CONTRIBUTING.md`, the GitHub issue templates, and
the PR template on a heal branch, but that branch was never merged — so `main`, the branch
every external contributor sees, still had none of it. The gap was branch topology, not
missing work.

This heal session did two things:

1. **Rescued the orphaned work.** Brought `CONTRIBUTING.md`, the three issue templates
   (bug report, feature request, skill submission), and the PR template onto the default
   branch so they finally reach contributors.

2. **Completed the file-based community layer** — the parts genuinely still missing, built
   the Squire way (files, not infrastructure, honoring the no-server/no-telemetry
   anti-vision):
   - **`GOVERNANCE.md`** — closes the "no formal governance body" gap with an honest
     benevolent-maintainer model, decision process, and the principles that constrain
     governance (the anti-vision is not negotiable per-PR).
   - **`CODE_OF_CONDUCT.md`** — extracted and expanded from the inline section in
     `CONTRIBUTING.md` into a recognized standalone file.
   - **`SUPPORT.md`** — closes the "community forum" gap by establishing GitHub Discussions
     as the community channel: the file-based project's file-based forum, no Discord to
     host or moderate.
   - **`DISTRIBUTION.md`** — closes the "no adoption metrics beyond stars" gap by defining
     the no-telemetry, GitHub-native signals adoption is actually read from (forks,
     dependency graph, traffic, Discussions and contributor activity). Telemetry was never
     an option — it violates the anti-vision — so the fix is to define what *is* measured.
   - **`CHANGELOG.md`** — distribution/versioning hygiene; a release is a tagged commit
     plus a changelog entry, no build artifact.
   - **`.github/ISSUE_TEMPLATE/config.yml`** — routes questions to Discussions and points
     contributors at the support and contributing docs.

**Why not "REALIZED"?** Two documented gaps remain by design, not by omission: no dedicated
Discord (Discussions is the deliberate file-based substitute) and no live adoption
dashboard (adoption is read from public GitHub signals, never tracked telemetry). For a
files-over-infrastructure product, the file-based layer *is* the realization — so the
pillar advanced from PARTIAL 55% to PARTIAL 80% rather than to REALIZED.

## Migration from claude-code-visualize

The `/visualize` and `/blueprint` commands originally lived in their own repo (claude-code-visualize, published as claude-code-artifacts). When Squire formed as the unified toolkit, both commands migrated here. The original repo now redirects to Squire.
