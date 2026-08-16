# /memory-ingest -- File Insights Back Into Memory

You capture valuable analysis, discoveries, or decisions from the current conversation and file them into the MEMORY.md wiki AND MemPalace verbatim store. This is the "query results file back" pattern: good answers shouldn't disappear into chat history.

**Arguments:** `$ARGUMENTS`

---

## Route by Arguments

| Input | Action |
|-------|--------|
| `"<topic>"` | File the current conversation's insights about this topic |
| `--session` | File a session summary (end-of-session compaction) |
| `--decision "<what>"` | File a specific decision with context and rationale |
| (empty) | Interactive: ask what to file |

---

## Process

### Step 1: Extract

From the current conversation, extract:
- **Facts learned** (new information about projects, people, tools)
- **Decisions made** (with rationale and alternatives considered)
- **Discoveries** (patterns, connections, insights)
- **Corrections** (things we got wrong and fixed)

### Step 2: Classify

For each extracted item, determine:
- **Memory type:** user | feedback | project | reference
- **Target file:** existing memory file to UPDATE, or new file to CREATE
- **Staleness risk:** will this be stale in days, weeks, or months?

### Step 3: File to MEMORY.md Layer

For each item:

**If updating existing file:**
1. Read the target file
2. Integrate new information (don't duplicate, merge)
3. Update the frontmatter description if scope changed
4. Verify MEMORY.md index entry still accurate

**If creating new file:**
1. Write file with proper frontmatter (name, description, type)
2. Follow body structure for type (feedback: rule + Why + How to apply; project: fact + Why + How to apply)
3. Add entry to MEMORY.md index under correct section
4. Keep index entry under 150 chars

### Step 4: File to MemPalace Layer

For each item, also store the verbatim conversation context in MemPalace:
```bash
mempalace add_drawer --wing eddie_memory --room <appropriate_room> --content "<verbatim context>"
```

This preserves the full reasoning that the wiki summary compresses away.

### Step 5: Cross-Reference

Check if the filed content relates to:
- Existing knowledge compiler KBs (research, design) -> suggest `/kb-ingest`
- Existing MemPalace wings -> note the connection
- Other memory files -> add cross-references

---

## Output

```
MEMORY INGEST -- {date}
==========================================

Filed {N} items:
  [UPDATE] {file} -- {what changed}
  [CREATE] {file} -- {one-liner}
  [PALACE] {wing}/{room} -- {drawer count} verbatim drawers

Cross-references:
  {file} relates to {other_file}

Index: {lines}/200 used
```

---

## Philosophy

The MEMORY.md wiki is the curated summary. MemPalace drawers hold the verbatim original. Neither is complete without the other. This command ensures both layers get updated together, so the wiki stays current and the verbatim store stays searchable.
