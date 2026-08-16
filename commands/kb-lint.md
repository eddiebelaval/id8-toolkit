# /kb-lint -- Knowledge Base Health Check

You audit id8Labs knowledge bases for consistency, completeness, and data integrity.

**Arguments:** `$ARGUMENTS`

---

## Route by Arguments

Parse `$ARGUMENTS`:

| Input | Action |
|-------|--------|
| `<kb-name>` | Lint a specific KB |
| `--all` | Lint all KBs in the manifest |
| (empty) | Lint all KBs |

---

## Setup

1. Read `~/Development/id8/knowledge/manifest.json`
2. Read `~/.claude/skills/knowledge/SKILL.md` for lint rules

---

## Lint Checks

For each target KB, run these checks in order:

### 1. Structure Check
- [ ] `raw/` directory exists
- [ ] `wiki/` directory exists with `_index.md`
- [ ] `wiki/concepts/`, `wiki/sources/`, `wiki/connections/` exist
- [ ] `output/` directory exists
- [ ] `health.md` exists
- [ ] For extended KBs: `ext/` directory and expected extensions exist

### 2. Orphaned Raw Files (ERROR)
Scan `raw/` for files with `processed: false` or no wiki article:
- List each orphaned file with its ingest date
- Older orphans are higher severity

### 3. Broken Wikilinks (ERROR)
Scan all `.md` files in `wiki/` for `[[wikilinks]]`:
- Resolve each link target
- Report any that point to non-existent files
- Suggest corrections (fuzzy match on filename)

### 4. Index Drift (WARNING)
Compare `_index.md` entries against actual files in `wiki/`:
- Articles in wiki/ not listed in _index.md
- Entries in _index.md pointing to missing articles
- Report count and list

### 5. Missing Backlinks (WARNING)
For each wikilink A -> B, check if B -> A exists:
- Only check within `wiki/concepts/` and `wiki/connections/`
- Source files don't need backlinks to concepts (one-directional is fine)

### 6. Stale Articles (WARNING)
Check `updated` date in article frontmatter against raw source modification time:
- If raw source is newer than article: stale
- Suggest recompile

### 7. Empty Directories (INFO)
Report any wiki subdirectories with no files.

### 8. Suggested Connections (INFO)
Look for concepts mentioned in 2+ source summaries that don't have a connection article:
- Suggest potential new connection articles
- Limit to top 3 suggestions

### 9. Cross-KB Opportunities (INFO, only with --all)
Look across all KBs for:
- Similar concepts that could be linked
- Research findings that relate to design patterns
- Memory entries that reference KB content

---

## Output

Write results to `{kb}/health.md`:

```markdown
# {KB Name} Health Report

Last lint: YYYY-MM-DD HH:MM

## Summary
- Errors: N
- Warnings: N
- Info: N

## Errors
{list with file paths and descriptions}

## Warnings
{list with file paths and descriptions}

## Info
{list with suggestions}

## Recommendations
1. {Highest priority action}
2. {Second priority}
3. {Third priority}
```

Also print a summary to the user:
```
KB: {name} -- {errors} errors, {warnings} warnings, {info} info
  Top issue: {description of highest priority item}
```
