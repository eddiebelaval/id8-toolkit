# /kb-ingest -- Knowledge Base Ingest

You ingest raw source material into an id8Labs knowledge base for later compilation.

**Arguments:** `$ARGUMENTS`

---

## Route by Arguments

Parse `$ARGUMENTS`:

| Input | Action |
|-------|--------|
| `<kb-name> <file-path>` | Ingest a local file |
| `<kb-name> <url>` | Fetch and ingest a web page (uses defuddle) |
| `<kb-name> --paste` | Ingest pasted content from the user's next message |
| `<kb-name> status` | Show raw/ inventory (processed vs unprocessed) |
| (empty) | Show help |

---

## Setup

1. Read `~/Development/id8/knowledge/manifest.json`
2. Locate the target KB
3. Check KB type: if `mirror`, reject ingest (read-only). If `read_only_raw`, reject ingest to raw (suggest manual addition to source repo).
4. Read `~/.claude/skills/knowledge/SKILL.md` for article templates

---

## Ingest Process

### For Local Files

1. Read the source file
2. Generate a slug from the content title or filename (kebab-case, max 40 chars)
3. Copy to `{kb}/raw/{slug}.md` with frontmatter:

```markdown
---
source_url: "local"
source_path: "{original file path}"
source_type: {article | paper | repo | dataset | image | reference}
ingested: YYYY-MM-DD
processed: false
---

{file contents}
```

### For URLs

1. Use the defuddle skill to fetch and convert the web page to clean markdown
2. Generate a slug from the page title
3. Save to `{kb}/raw/{slug}.md` with frontmatter:

```markdown
---
source_url: "{url}"
source_type: article
ingested: YYYY-MM-DD
processed: false
---

{defuddled markdown content}
```

4. If the page has images, note their URLs in the frontmatter for potential later download

### For Paste

1. Prompt user: "Paste the content you want to ingest."
2. Accept the content
3. Ask for a title if not obvious from content
4. Save to `{kb}/raw/{slug}.md` with frontmatter (source_url: "paste")

---

## Post-Ingest

After saving the raw file:

1. Report: "Ingested `{filename}` to `{kb}/raw/`. Source type: {type}."
2. Quick scan: extract 3-5 key topics/claims from the source
3. Check against existing `wiki/_index.md` for overlap: "This relates to existing articles: [[concept-x]], [[concept-y]]"
4. Suggest: "Run `/kb-compile {kb-name}` to process this into wiki articles."

---

## Research KB Special Handling

For the research KB, ingest delegates to the existing `/research ingest` logic when the source is a research paper or argument. This preserves the expert panel evaluation and claim extraction pipeline.

If the source is a general article or reference (not research-grade), use the standard ingest process above.

---

## Design KB Note

The design KB has `read_only_raw: true`. If the user tries to ingest:
- Reject: "The design KB's raw sources are from an external GitHub repo (design-references). To add a new site reference, add it to ~/Development/design-references/design-md/ and run `/kb-compile design`."
