# /kb-query -- Knowledge Base Query

You answer questions against id8Labs knowledge bases, citing sources with Obsidian wikilinks.

**Arguments:** `$ARGUMENTS`

---

## Route by Arguments

Parse `$ARGUMENTS`:

| Input | Action |
|-------|--------|
| `<question>` | Query the most relevant KB (auto-detect from question content) |
| `<question> --kb <name>` | Query a specific KB |
| `<question> --all` | Query across all KBs (federated) |
| `<question> --save` | Save the answer to the KB's output/ directory |
| `<question> --kb <name> --save` | Query specific KB and save |
| `<question> --slides` | Output answer as Marp slide deck |
| `<question> --slides --save` | Generate slides and save to output/ |
| `list` | List all registered KBs with descriptions and tags |
| (empty) | List all registered KBs |

Flags can be combined: `--all --save`, `--kb research --save`, `--all --slides --save`

---

## Setup

1. Read `~/Development/id8/knowledge/manifest.json`
2. Read the skill reference: `~/.claude/skills/knowledge/SKILL.md`

---

## Query Process

### Step 1: Select Target KBs

- If `--kb <name>`: use only that KB
- If `--all`: use all KBs in manifest
- If no flag: read question, match against KB tags in manifest, select the most relevant 1-2 KBs

### Step 2: Load Indexes

For each target KB:
1. Read `{kb}/wiki/_index.md` to understand what articles exist
2. Scan section headers and article descriptions to identify relevant articles

### Step 3: Read Relevant Articles

Based on the question:
1. Identify which concept, source, and connection articles are relevant
2. Read those articles (use Glob to find files if needed)
3. For extended KBs (research): also check registries (findings, contradictions, open-questions)
4. For mirror KBs (memory): read the linked topic files

**Be selective.** Don't read the entire KB. Read the index, identify 3-8 relevant articles, read those.

### Step 4: Synthesize Answer

Answer the question using information from the articles:
- Cite sources using `[[wikilinks]]` (e.g., "According to [[concepts/dark-mode-native]], ...")
- If cross-KB query: clearly attribute which KB each insight comes from
- If information is insufficient: say so and suggest what raw sources might help
- Be concise but thorough

### Step 5: Save (if --save)

If `--save` flag is present:
1. Generate a slug from the question (kebab-case, max 40 chars)
2. Write the answer to `{kb}/output/{YYYY-MM-DD}-{slug}.md`
3. Include frontmatter:

```markdown
---
query: "{original question}"
kbs_queried: [{kb names}]
date: YYYY-MM-DD
articles_referenced: [{list of articles read}]
---
```

4. Tell user: "Answer saved to `{path}`. View in Obsidian at `02-Areas/Knowledge/{kb}/output/`."

---

## Cross-KB Queries

When `--all` is specified or when the question spans domains:

1. Load all KB indexes
2. For each KB, identify relevant articles
3. Synthesize across KBs, clearly labeling which KB contributes each insight
4. Look for connections between KBs (e.g., research findings that inform design decisions)
5. If `--save`: save to the most relevant KB's output/, or create a cross-kb output if no single KB is primary

---

## Output Format

```
## Answer

{Synthesized answer with [[wikilink]] citations}

## Sources Referenced

- [[kb/wiki/path|Article Title]] -- {what it contributed}
- [[kb/wiki/path|Article Title]] -- {what it contributed}

## Gaps

{What the KBs don't cover that might be relevant}
```

---

## Marp Slides Output (--slides)

When `--slides` flag is present, output the answer as a Marp slide deck instead of plain markdown.

### Marp Format Rules

1. File starts with Marp frontmatter
2. Slides separated by `---`
3. First slide is title + subtitle
4. Each subsequent slide covers one key point (keep to 5-8 slides max)
5. Use bullet points, not paragraphs (slides are visual, not essays)
6. Last slide is "Sources" with wikilinks
7. Save as `.md` file in `{kb}/output/` with `-slides` suffix

### Marp Template

```markdown
---
marp: true
theme: default
paginate: true
backgroundColor: #0a0a0a
color: #e5e5e5
style: |
  section {
    font-family: 'Inter', sans-serif;
  }
  h1 { color: #fff; font-size: 2.2em; }
  h2 { color: #fff; font-size: 1.6em; }
  strong { color: #86efac; }
  code { color: #a5b4fc; }
  a { color: #818cf8; }
---

# {Question as Title}

{One-line subtitle framing the answer}

---

## {Key Point 1}

- {Bullet}
- {Bullet}
- {Bullet with **emphasis** on key terms}

---

## {Key Point 2}

- {Bullet}
- {Bullet}

---

(... 3-6 more slides ...)

---

## Sources

- {Article 1} -- {what it contributed}
- {Article 2} -- {what it contributed}
- {Article 3} -- {what it contributed}

---

## Gaps

- {What the KBs don't cover}
- {Suggested next research}
```

### Save Location

If `--save` is also set:
- File: `{kb}/output/YYYY-MM-DD-{slug}-slides.md`
- Tell user: "Slides saved. Open in Obsidian with Marp plugin, or run `npx @marp-team/marp-cli {file} --html` to export as HTML/PDF."
