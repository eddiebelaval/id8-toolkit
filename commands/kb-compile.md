# /kb-compile -- Knowledge Base Compiler

You are the knowledge compiler for id8Labs. You read raw sources and compile them into a structured .md wiki with concept articles, source summaries, and connection articles.

**Arguments:** `$ARGUMENTS`

---

## Route by Arguments

Parse `$ARGUMENTS`:

| Input | Action |
|-------|--------|
| `<kb-name>` | Incremental compile (process new raw sources only) |
| `<kb-name> --full` | Full recompile (regenerate all wiki articles from raw) |
| `status` | Show compile status for all KBs |
| (empty) | Show compile status for all KBs |

---

## Setup

1. Read `~/Development/id8/knowledge/manifest.json` to locate the target KB
2. Resolve the KB path: `~/Development/id8/knowledge/{kb.path}/`
3. Read the skill reference: `~/.claude/skills/knowledge/SKILL.md` for article templates and conventions
4. Read `{kb}/wiki/_index.md` to understand current wiki state

---

## Compile Process

### Step 1: Inventory Raw Sources

Scan `{kb}/raw/` recursively for all files. For each file:
- Check frontmatter for `processed: true/false`
- If `--full` flag: ignore processed status, process everything
- If incremental (default): only process files where `processed: false` or no frontmatter

For the **design** KB: raw sources are DESIGN.md files inside `raw/design-md/`. Each site directory is one source. Also include `raw/MCM-DIGITAL-DESIGN-RESEARCH.md` as a source.

For the **research** KB: raw sources are in `raw/` plus the registries at `wiki/registries/` contain the compiled knowledge. Generate concept articles from findings, not just raw files.

### Step 2: Generate Source Summaries

For each unprocessed raw source, create a summary in `wiki/sources/`:

- **File name:** `{slug}.md` (kebab-case from source title)
- **Content:** Follow the Source Summary template from SKILL.md
- **Extract:** Key claims, concepts mentioned, relationships to existing concepts
- Use Obsidian `[[wikilinks]]` for all internal references

### Step 3: Extract and Cluster Concepts

From all source summaries (new + existing), identify concept clusters:

- **New concepts:** Topics mentioned in 2+ sources that don't have a concept article yet
- **Updated concepts:** Existing concept articles that need updating based on new sources
- Create/update articles in `wiki/concepts/` using the Concept Article template
- Ensure bidirectional links: concept links to sources, sources link to concepts

### Step 4: Identify Connections

Look for cross-cutting patterns across concepts:

- **Pattern:** Two or more concepts that share a non-obvious relationship
- **Comparison:** Two approaches to the same problem
- **Evolution:** How a concept changed across multiple sources
- Create articles in `wiki/connections/` using the Connection Article template

### Step 5: Rebuild Index

Rewrite `{kb}/wiki/_index.md`:

1. Preserve existing frontmatter (aliases, tags)
2. List all concept articles under `## Concepts`
3. List all source summaries under `## Sources`
4. List all connection articles under `## Connections`
5. Each entry: `- [[path|Display Name]] -- {one-line description}`
6. For extended KBs: preserve existing sections (Registries, Wings, Modules, etc.)

### Step 6: Mark Processed

For raw files with frontmatter, update `processed: true` and add `compiled: YYYY-MM-DD`.

---

## Design KB Special Handling

The design KB has 54 DESIGN.md files as read-only raw sources. When compiling:

1. **Source summaries:** One per site in `wiki/sources/`. Extract: color philosophy, typography system, component patterns, layout approach, depth strategy.
2. **Concept articles:** Cross-cutting patterns like "dark-mode-native", "inter-font-system", "shadow-as-border", "developer-tool-aesthetics", "saas-dashboard-patterns".
3. **Connections:** Relationships between sites (e.g., "Vercel and Linear share the same elevation philosophy").
4. Do NOT modify anything in `raw/design-md/` (read-only external repo).

---

## Research KB Special Handling

The research KB has registries (findings, contradictions, open-questions) as its primary compiled knowledge. When compiling:

1. **Source summaries:** From `raw/` files (external papers, articles ingested)
2. **Concept articles:** Generated from findings in `wiki/registries/findings.md`. Each major finding (F-NNN) or cluster of related findings becomes a concept article.
3. **Connections:** Cross-finding relationships, contradiction-resolution articles
4. Preserve all existing registry files and MOC sections (Registries, Wings, Modules, etc.)

---

## Output

After compiling, report:
- Sources processed: N new, M total
- Concepts: N new, M updated, K total
- Connections: N new, K total
- Index rebuilt: yes/no

Remind user they can view the compiled wiki in Obsidian at `02-Areas/Knowledge/{kb-name}/wiki/`.
