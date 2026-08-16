# /memory-lint -- MEMORY.md Health Check

You audit Eddie's auto-memory system for staleness, contradictions, dead links, bloat, and missed connections.

> **Lane note (2026-07-14):** the nightly **memory sentinel** (`~/Development/id8/observatory/sentinel.py`, 09:45 launchd) now runs the mechanical subset of these checks automatically -- index integrity, orphans, signatures, staleness, census parity -- and self-heals within a narrow authority list. Use /memory-lint for INTERACTIVE deep dives: contradiction scans, `--deep` MemPalace cross-reference, merge-candidate judgment. Before re-reporting mechanical findings, check the sentinel's latest verdict at `~/Development/id8/observatory/data/health.json`.

**Arguments:** `$ARGUMENTS`

---

## Route by Arguments

| Input | Action |
|-------|--------|
| (empty) | Full lint |
| `--quick` | Index-only lint (fast, checks MEMORY.md only) |
| `--fix` | Lint + auto-fix safe issues (dead links, empty files) |
| `--deep` | Full lint + cross-reference against MemPalace |

---

## Setup

1. Read `~/.claude/projects/-Users-eddiebelaval-Development-id8/memory/MEMORY.md`
2. Inventory all `.md` files in the memory directory (recursively)
3. If `--deep`: check MemPalace availability via `mempalace status`

---

## Lint Checks

Run these checks in order. Classify each finding as ERROR, WARNING, or INFO.

### 1. Index Integrity (ERROR)

Scan every link in MEMORY.md (`[title](path)` format):
- [ ] Target file exists at the referenced path
- [ ] No duplicate entries pointing to the same file
- [ ] Every line in the index is under 150 characters (truncation rule)
- Report: dead links, duplicates, overlong entries

### 2. Orphan Files (WARNING)

Scan all `.md` files in memory/ that are NOT referenced in MEMORY.md:
- [ ] List each orphan with its type (from frontmatter) and last modified date
- [ ] Suggest: add to index, merge into existing file, or delete
- Exclude: MEMORY.md itself

### 3. Staleness Check (WARNING)

For each memory file, check the `type` field and content for time-sensitive claims:
- **Project memories:** Check if project status matches current reality
  - Look for mentions of dates, deadlines, "this week", "target: [date]"
  - If the date is >14 days ago, flag as potentially stale
- **Reference memories:** Check if referenced URLs/paths still exist
  - File paths: verify with glob
  - External systems: flag for manual check
- **Feedback memories:** Generally stable (skip staleness check)
- **User memories:** Generally stable (skip staleness check)
- Report: stale entries with suggested action (verify, update, or archive)

### 4. Contradiction Scan (WARNING)

Read all memory files and look for:
- [ ] Two files making contradictory claims about the same entity
  - e.g., project status "FROZEN" in one file, active work described in another
- [ ] Outdated status that conflicts with more recent entries
- [ ] Same fact stored in multiple files (duplication)
- Report: pairs of contradicting files with the specific conflict

### 5. Index Bloat Check (INFO)

- [ ] Count total lines in MEMORY.md (must stay under 200)
- [ ] Count total memory files
- [ ] Flag entries in "Current Focus" section older than 7 days
- [ ] Check if any single section has >30 entries (suggest splitting)
- Report: line count, file count, bloat risks

### 6. Frontmatter Consistency (INFO)

For each memory file, verify:
- [ ] Has `name`, `description`, `type` fields
- [ ] Type is one of: user, feedback, project, reference
- [ ] Description is specific enough to judge relevance (>20 chars)
- Report: files with missing or invalid frontmatter

### 7. Cross-Layer Opportunities (INFO, --deep only)

If MemPalace is available:
- [ ] Search MemPalace for topics mentioned in MEMORY.md that have rich verbatim content not captured in the wiki layer
- [ ] Identify MemPalace wings/rooms that have no corresponding memory file
- [ ] Suggest new memory files for frequently-searched MemPalace topics
- Report: bridge opportunities between layers

### 8. Session Log Compaction (INFO)

Check `session-log.md`:
- [ ] Entries older than 7 days that haven't been compacted
- [ ] Insights from old entries that should be promoted to topic files
- [ ] Total size (flag if >500 lines)
- Report: compaction candidates

---

## Output

Print results grouped by severity:

```
MEMORY LINT -- {date}
==========================================

ERRORS ({count})
  {file}: {description}

WARNINGS ({count})
  {file}: {description}

INFO ({count})
  {description}

RECOMMENDATIONS
  1. {highest priority action}
  2. {second priority}
  3. {third priority}

Health Score: {A|B|C|D|F}
  Index: {ok|bloated|broken}
  Freshness: {ok|stale|very stale}
  Coverage: {ok|orphans found|gaps found}
```

### Health Score Rubric

| Grade | Criteria |
|-------|----------|
| A | 0 errors, 0 warnings, index under 150 lines |
| B | 0 errors, <5 warnings |
| C | 0 errors, 5+ warnings OR 1+ stale critical entries |
| D | 1+ errors (dead links, broken refs) |
| F | 5+ errors OR index over 200 lines |

---

## Auto-Fix (--fix flag)

Safe fixes applied automatically:
- Remove dead links from MEMORY.md index
- Add orphan files to MEMORY.md index (with generated one-liner)
- Update "Current Focus" dates to absolute format
- Trim MEMORY.md lines over 150 chars

Unsafe fixes reported but NOT applied:
- Deleting orphan files
- Resolving contradictions
- Archiving stale entries
