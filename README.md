# id8-toolkit

Open-source [Claude Code](https://docs.anthropic.com/en/docs/claude-code) tools by [id8Labs](https://id8labs.app). Slash commands, skills, and self-installing tools for AI-augmented development.

This is the public toolkit. I use all of these daily. When I build something useful, it ends up here.

**X:** [@eddiebe](https://x.com/eddiebe) | **GitHub:** [eddiebelaval](https://github.com/eddiebelaval) | **Site:** [id8labs.app](https://id8labs.app)

---

## What's Inside

### Standalone Tools

Tools that don't require installation. Drop a file into your project and go.

| Tool | What It Does | How to Use |
|------|-------------|------------|
| **[BUILDING-SETUP.md](BUILDING-SETUP.md)** | Self-installing build journal with auto-updates, periodic check-ins, and origin story interview | Copy to project root, tell Claude: "Read BUILDING-SETUP.md and follow the instructions" |

### Slash Commands

Install once, use in any Claude Code session. These are prompt files that live in `~/.claude/commands/`.

| Command | What It Does |
|---------|-------------|
| **`/visualize`** | Generate interactive HTML visualizations of architecture, workflows, codebases, or any concept |
| **`/blueprint`** | Generate persistent build plans with progress tracking, parallel batches, and copy-paste task prompts |
| **`/integration-audit`** | Audit a full-stack project for wiring gaps across database, API, auth, types, store, UI, and page layers |

### Skills

More complex tools that live in `~/.claude/skills/`.

| Skill | What It Does |
|-------|-------------|
| **`/audit`** | Read-only codebase health audit covering security, dead code, wiring gaps, type safety, and UI shells |

---

## BUILDING-SETUP.md

A self-installing, self-consuming setup wizard that creates a personalized **BUILDING.md** for any project — a living build journal that grows with your codebase.

**No installation required.** Just drop the file and read it.

### What You Get

- **Smart setup** — The wizard explores your project first (package.json, git history, file structure, deployment config) and figures out your stack, team size, and project maturity on its own. Then it only asks you the stuff it can't figure out.
- **Auto-updating build log** — After every significant piece of work, Claude automatically updates your BUILDING.md. No manual entries needed.
- **Periodic check-ins** — Every few milestones, Claude pauses and asks: How's it going? What's next? What have you learned? These capture the human side of the build.
- **Origin story interview** — After setup, a conversational interview captures how your project started. The spark, the problem, the early days. This becomes the opening chapter.
- **Self-cleaning** — The setup file deletes itself when done. All that's left is your personalized BUILDING.md.

### How to Use

```
1. Download BUILDING-SETUP.md (or copy the raw file)
2. Place it in your project root
3. Open Claude Code
4. Say: "Read BUILDING-SETUP.md and follow the instructions"
5. Answer 2-3 questions
6. Done — your BUILDING.md is ready and self-maintaining
```

### The Philosophy

Most project documentation is written after the fact, if at all. BUILDING.md is different — it's a living autobiography that grows as you build. The auto-updates capture what happened. The check-ins capture who was building it and how they felt. The origin story gives it a beginning. Six months from now, you don't just see code — you see the journey.

---

## /visualize — Interactive Visual Explanations

Turn any concept, architecture, workflow, or codebase structure into a self-contained HTML visualization. Dark-themed, animated, interactive — no external dependencies.

```
/visualize Homer architecture
/visualize how Supabase RLS works
/visualize the deployment pipeline
```

**Features:**
- Tabbed views, flow diagrams, tree views, interactive cards
- Animated SVG flow lines (flowing dashes, traveling pulses)
- Stats counters with count-up animation
- Expandable/collapsible sections
- Senior Dev Assessment tab with copy-paste fix prompts
- Factory-inspired design system (dark theme, warm neutrals, orange accents)

---

## /blueprint — Persistent Build Plans

Generate interactive build plans that survive context limits. Progress persists in `localStorage` — check off tasks as you complete them.

```
/blueprint Homer V2 — full rebuild with new dashboard
/blueprint DeepStack live trading
/blueprint --update homer-v2
```

**Features:**
- 6-round structured interview before generating (scope, architecture, phases, parallelism, risks, confirmation)
- Parallel batch columns — identify work that can run simultaneously
- localStorage checkbox persistence with progress bars
- SVG dependency graph showing critical path
- Copy-paste prompts for every task
- `--update` flag to re-read and regenerate with new progress

---

## /integration-audit — Full-Stack Feature Audit

Scan a project and map whether each feature is wired end-to-end across every layer: Database, API, Auth, Types, Store, UI, and Page.

```
/integration-audit ~/Development/Homer
/integration-audit
```

**Features:**
- 4 parallel agents scan simultaneously
- Integration matrix with color-coded cells (Y/N/P for each layer)
- Expandable rows showing actual file paths per layer
- Gap analysis with severity levels and copy-paste fix prompts
- Architecture flow diagram with animated connections

---

## /audit — Codebase Health Audit

Read-only structural audit covering 5 dimensions. Outputs a prioritized fix plan.

```
/audit
/audit security,dead-code
/audit src/api
```

**Dimensions:** Security, Dead Code, Wiring Gaps, Type Safety, UI Shells

---

## Design System

All HTML visualizations follow the **Factory-inspired** design language:

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#020202` | Near-black |
| Text | `#eeeeee` | Near-white |
| Accent | `#ef6f2e` | Orange — primary |
| Secondary | `#f59e0b` | Amber — secondary |
| Success | `#4ecdc4` | Teal — success |
| Fonts | Geist + Geist Mono | With system fallbacks |

**Rules:** No shadows, no gradients, no glow effects, no emojis. Typography and whitespace ARE the design.

---

## Installation

### Standalone Tools (no install needed)

For `BUILDING-SETUP.md` and any future standalone tools — just download the file and use it. No installation step.

### Slash Commands + Skills

Clone the repo and run the installer:

```bash
git clone https://github.com/eddiebelaval/id8-toolkit.git
cd id8-toolkit
chmod +x install.sh
./install.sh
```

Or install manually:

```bash
# Commands
cp commands/visualize.md ~/.claude/commands/
cp commands/blueprint.md ~/.claude/commands/
cp commands/integration-audit.md ~/.claude/commands/

# Skills
mkdir -p ~/.claude/skills/audit
cp skills/audit/SKILL.md ~/.claude/skills/audit/
```

### Options

```bash
./install.sh --dry-run        # Preview what will be installed
./install.sh --commands-only   # Skip the /audit skill
./install.sh --uninstall       # Remove all toolkit files
```

---

## How It Works

**Slash commands** are markdown files in `~/.claude/commands/`. When you type `/visualize` in Claude Code, it reads the `.md` file as a prompt — the instructions tell Claude how to generate the output.

**Skills** live in `~/.claude/skills/<name>/SKILL.md` and can include more complex behavior.

**Standalone tools** like `BUILDING-SETUP.md` are self-contained files you drop into a project. They contain instructions that Claude follows when it reads the file — no configuration, no dependencies.

All of these are **prompt engineering** — they don't execute code themselves. They instruct Claude to use its built-in tools (Glob, Grep, Read, Write, Bash) to scan, analyze, and generate.

---

## What's Coming

This repo is a living toolkit. As I build new tools, they show up here. If you want to see what I'm working on or suggest a tool, reach out:

**X:** [@eddiebe](https://x.com/eddiebe)
**GitHub:** [eddiebelaval](https://github.com/eddiebelaval)

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

Built with Claude Code by [Eddie Belaval](https://x.com/eddiebe) / [id8Labs](https://id8labs.app).
