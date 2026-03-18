# VISION.md — Squire

> The operating system for AI-assisted development.

---

## Soul

Make AI coding agents reliable, productive, and predictable by encoding the behavioral corrections, workflows, and tooling that emerged from 2,990 real sessions into a single drop-in toolkit.

## Pillars

1. **Behavioral Ruleset (squire.md)** -- REALIZED
   The flagship artifact. Nine behavioral rules derived from analyzing 3,307 commits across 5 months. Each rule addresses a specific, recurring failure pattern where AI agents waste time or introduce bugs. Drop it into any project root or global config and agent behavior changes immediately.

2. **Slash Commands** -- REALIZED
   63 Claude Code commands covering the full development lifecycle: shipping (/ship), deployment (/deploy), research (/research), visualization (/visualize), planning (/blueprint), testing (/test), content publishing (/publish), and operations (/morning, /status). Each command is a detailed prompt file that instructs agents to use their built-in tools systematically.

3. **Skills Library** -- REALIZED
   328 specialized skills organized across 17 domains: frontend, backend, architecture, DevOps, AI/ML, SEO, CRO, content, marketing, financial, startup, operations, product management, design, UX, writing, and communication. Each skill provides domain expertise that agents lack by default.

4. **Custom Agents** -- REALIZED
   34 agents with tool access for architecture, security, DevOps, payment processing, database migrations, MCP servers, social media, market intelligence, and more. These are executable specialists, not static prompts.

5. **Stage-Gate Pipeline** -- REALIZED
   11-stage build system from Concept Lock to Listen & Iterate. Each stage has a gate question that must be answered before advancing, plus agent-native additions for AI-assisted development. The pipeline enforces discipline without slowing momentum.

6. **Community & Distribution** -- PARTIAL
   Published on GitHub with an MIT license, interactive installer, and comprehensive README. Community engagement remains limited -- no Discord, no contributor guidelines, no external adoption metrics beyond GitHub stars.

---

## Anti-Vision

Squire is NOT a product, a SaaS, or a framework with runtime dependencies. It is a collection of files. No lock-in, no accounts, no telemetry. If it ever requires a build step, a server, or a subscription to use, something has gone wrong.

## Edges

- Does not execute code itself -- it instructs agents to use their existing tools
- macOS-centric for some shell scripts (bash 3.2+ minimum)
- Assumes Claude Code as primary agent surface, though patterns apply broadly
- Skills are prompt-based, not validated against specific model capabilities
- No automated testing of prompt quality or behavioral compliance
