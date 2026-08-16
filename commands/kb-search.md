# /kb-search -- Knowledge Base Search

You search across id8Labs knowledge bases for articles matching a query. Faster than `/kb-query` -- this finds what exists, not synthesizes answers.

**Arguments:** `$ARGUMENTS`

---

## Route by Arguments

Parse `$ARGUMENTS`:

| Input | Action |
|-------|--------|
| `<term>` | Search all KBs for articles matching the term |
| `<term> --kb <name>` | Search a specific KB only |
| `<term> --type <concepts\|sources\|connections>` | Filter by article type |
| (empty) | Show KB stats (article counts per KB) |

---

## Setup

1. Read `~/Development/id8/knowledge/manifest.json`
2. For each target KB, read `wiki/_index.md`

---

## Search Process

### Step 1: Load Indexes

For each target KB:
- Read `{kb}/wiki/_index.md`
- Parse all article entries (the `[[wikilinks]]` and their descriptions)
- Build a flat list of: `{kb_name, article_path, display_name, description, type}`

### Step 2: Fuzzy Match

Search the flat list against the query term:
- Match against display name, description, and article type
- Case-insensitive substring matching
- Also search frontmatter tags if articles have them (read the first 10 lines of each matching candidate)
- Rank by relevance: exact title match > title contains > description contains > tag match

### Step 3: Deep Search (if few results)

If fewer than 3 matches from index search:
- Use Grep to search inside `wiki/**/*.md` for the term
- Report files that contain the term with a snippet of context
- This catches content that isn't surfaced in the index descriptions

### Step 4: Report

Display results grouped by KB:

```
## Search: "{term}"

### research (N matches)
- [[concepts/constraint-as-consciousness|Constraint as Consciousness]] -- F-005, write-protection as precondition
- [[registries/findings|Findings Registry]] -- contains 2 mentions

### design (N matches)
- [[concepts/shadow-as-border|Shadow-as-Border]] -- Vercel's 0px 0px 0px 1px pattern
- [[sources/vercel|Vercel]] -- shadow-as-border technique

### memory (N matches)
- (none)

Total: N articles across M knowledge bases
```

If no results: "No matches for '{term}'. Try a broader search or run `/kb-lint --all` to check if content needs recompiling."
