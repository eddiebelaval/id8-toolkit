---
title: "SPEC.md"
date: [YYYY-MM-DD]
author: [Name]
product: [Product Name]
drift-status: CURRENT | DRIFTED | STALE
last-reconciled: [YYYY-MM-DD]
---

# SPEC.md -- Living Specification
## [Product Name]

> Last reconciled: [YYYY-MM-DD] | Build stage: [Stage N]
> Drift status: [CURRENT/DRIFTED/STALE]
> VISION alignment: [X]% ([N] of [M] pillars realized)

---

## Identity

[What this product IS -- present tense only. Not what it will be. Not what it was.
This section gets REWRITTEN (not appended) when the product changes.
2-3 sentences maximum.]

## Capabilities

What this product can do TODAY. Each capability is testable.

- **[Capability Name]:** [User can X / System does Y]
- **[Capability Name]:** [User can X / System does Y]

## Architecture Contract

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | [e.g., Next.js 16] | |
| Backend | [e.g., Supabase] | |
| AI | [e.g., Claude Sonnet 4.5] | |
| Hosting | [e.g., Vercel] | |
| Database | [e.g., Supabase Postgres] | |

### Data Model (core tables/entities)

| Entity | Purpose | Key Fields |
|--------|---------|------------|
| | | |

### Integrations

| Service | Purpose | Status |
|---------|---------|--------|
| | | Active / Planned / Deprecated |

## Boundaries

[What this product explicitly does NOT do right now. Not aspirational boundaries
(those go in VISION.md Anti-Vision) -- factual current scope limits.]

- Does NOT [X]
- Does NOT [Y]

## Verification Surface

Assertions that can be checked against the live product or codebase.
These are the audit targets -- if any of these fail, the spec is stale.

- [ ] [Testable assertion about the product]
- [ ] [Testable assertion about the product]
- [ ] [Testable assertion about the product]

## Drift Log

| Date | Section | What Changed | Why | VISION Impact |
|------|---------|-------------|-----|---------------|
| [YYYY-MM-DD] | [Section] | [What changed in the spec] | [Why it changed] | [Did VISION.md need updating too?] |

---

**Companion documents:** `VISION.md` (what it is BECOMING), `BUILDING.md` (how we got here).
**This document is the contract. Test against it. Audit against it.**
