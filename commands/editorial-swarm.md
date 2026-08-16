# /editorial-swarm - Six-Agent Parallel Editorial Pipeline

**Trigger when:** the user wants to polish long-form prose — articles, essays, white papers, release notes, Shipped. magazine drafts, Bible essays, founding documents. Not for code, not for short social posts.

You are running the 6-agent editorial swarm on a prose draft. The goal: take a B+ draft to A-grade through parallel expert review, iterate on feedback, and stop when the rubric hits the target score.

**Philosophy:** one pass can't catch everything. Six specialists in parallel — each with a narrow brief — catches structural, voice, factual, narrative, line, and adversarial issues simultaneously. A merger agent resolves non-conflicts, Claude surfaces conflicts for user decision, then we iterate.

**Source:** Claude Code Insights Report - 2026-04-22. The pattern was already in use informally; this command codifies it.

---

## Arguments

Parse `$ARGUMENTS`:
- **`<draft-path>`** (required) — path to the markdown draft to polish
- **`--target <score>`** — rubric target, default `9`. Range 1-10.
- **`--max-iterations <n>`** — hard cap on iteration rounds, default `3`. Prevents runaway loops.
- **`--skip <agents>`** — comma-separated list of agents to skip (e.g., `--skip factcheck,skeptic` for fiction).
- **`--dry-run`** — run one pass, output feedback, do not apply edits. Useful for first-read assessment.
- **`--quiet`** — only report final result + changelog, not per-agent output.

If no path is provided, error out with usage.

---

## Step 0: Pre-flight

1. Confirm the draft file exists and is a `.md` or `.mdx` file. If it's a `.txt` or code file, refuse with "editorial-swarm is for prose drafts, not code — did you mean /polish?"
2. Read the full draft into context. Record word count.
3. Detect draft type from path + frontmatter:
   - `shipped/**` → magazine piece, apply `voice: narrative + literary`
   - `knowledge/**/raw/**` → research essay, apply `voice: scholarly + grounded`
   - `products/**/VISION.md|SPEC.md|BUILD.md` → triad doc, apply `voice: doctrine + precise`
   - default → `voice: professional + clear`
4. Snapshot the original: `cp <draft> <draft>.pre-swarm.bak` so the user can diff or restore.

---

## Step 1: Launch the Six Agents in Parallel

**CRITICAL:** Dispatch all six via the Task tool in a single message. Use the `general-purpose` subagent_type with distinct system prompts — each agent must have a narrow brief and return structured JSON.

### Agent 1: Structural Editor
**Brief:** Does the piece have a clear spine? Is the argument/narrative order correct? Are transitions working? Is anything out of place?
**Returns JSON:**
```json
{
  "agent": "structural",
  "score": 7,
  "severity": "medium",
  "issues": [
    {"section": "intro", "problem": "...", "suggested_fix": "..."},
    ...
  ],
  "overall": "one sentence takeaway"
}
```

### Agent 2: Voice Editor
**Brief:** Does the tone stay consistent? Does it match the detected draft type? Flag register shifts, jargon, corporate-speak, overqualification. Respect Eddie's voice preferences from `feedback_no_em_en_dashes.md` and `feedback_autobiography_voice_landed.md`.
**Returns same JSON shape.**

### Agent 3: Technical Factchecker
**Brief:** Verify any technical claims, numbers, dates, named people, product names, quoted material. Cross-reference against knowledge/ wiki pages where relevant. Flag anything that smells invented per `feedback_no_fabricated_origins.md`.
**Returns same JSON shape with `verifiable: true|false|uncertain` per claim.**

### Agent 4: Narrative Editor
**Brief:** Does the piece pull the reader through? Where does attention drop? Is the hook strong? Is the close earned? Is there a cliffhanger or thematic resolution?
**Returns same JSON shape.**

### Agent 5: Line Editor
**Brief:** Sentence-level craft. Redundancy, weak verbs, passive voice, wordy phrases, rhythm, clarity. No em/en dashes (hard rule). Concrete over abstract.
**Returns same JSON shape plus `line_edits: [{before, after, reason}]`.**

### Agent 6: Adversarial Skeptic
**Brief:** Argue against the piece. Where is it soft? What would a hostile reader say? What claims are unsupported? What's the weakest paragraph and why? Do NOT suggest rewrites — surface only.
**Returns same JSON shape.**

Skip any agents named in `--skip`.

---

## Step 2: Merge and Present

1. Collect all six JSON outputs.
2. Classify edits into two buckets:
   - **Auto-apply:** line edits, typos, grammar, em-dash removal, consistent tense, passive-to-active swaps, dash replacements. Anything the line editor proposed with clear before/after and no semantic shift.
   - **Needs decision:** structural reordering, voice shifts, factcheck flags, narrative restructures, skeptic concerns.
3. Apply the auto-apply bucket to the draft using Edit.
4. Present the "needs decision" bucket to the user as a numbered list, grouped by agent, with the agent's severity rating. The user picks which ones to apply, skip, or defer.

For `--dry-run`, skip application — just present both buckets and stop.

---

## Step 3: Rubric Score and Iterate

Compute an aggregate rubric score:
```
overall = avg([structural, voice, factcheck, narrative, line, skeptic])
```

If `overall >= target` OR iteration count >= `max-iterations`: **STOP**. Go to Step 4.

Otherwise:
- Increment iteration counter.
- Re-read the updated draft.
- Re-launch the six agents in parallel (Step 1).
- Merge and present again (Step 2).

Agents should see the changelog of what already changed so they don't re-flag resolved issues.

---

## Step 4: Final Report

Output a concise changelog, even if `--quiet`:

```
editorial-swarm complete on <draft-path>
  iterations: <n>
  final score: <x>/10
  word count: <before> -> <after>

edits applied:
  - [structural] moved section 3 before section 2 (reader confusion)
  - [line] 47 sentence-level edits (verb strength, redundancy)
  - [voice] 6 register fixes
  - [dash removal] 12 em/en dashes replaced per rule

deferred (you declined):
  - [skeptic] paragraph on X unsupported
  - [factcheck] date on Y couldn't verify

backup: <draft>.pre-swarm.bak (delete when satisfied)
```

---

## Step 5: Post-Swarm Options

Offer these as a follow-up:
- "Publish to shipped/pipeline/?" (if in shipped/)
- "Queue for X?" (uses tweet-queue if applicable)
- "File to knowledge/?" (if the piece is research-flavored)
- "Commit on a feature branch?" (per git workflow rules)

Do NOT auto-publish. Every publish is an explicit decision.

---

## Hard Rules

- NO em or en dashes anywhere in Eddie's prose (per `feedback_no_em_en_dashes.md`). The line editor must flag and replace all of them.
- NO fabricated biographical anecdotes (per `feedback_no_fabricated_origins.md`). The factchecker must flag any origin story, quote, or scene not grounded in the triad or Eddie's own words.
- NO heavy-handed rewrites. If an agent proposes rewriting more than 30% of a paragraph, bump it to "needs decision" regardless of severity.
- Respect the detected voice. A shipped/ piece should not be flattened to a LinkedIn post.
- Always back up before the first pass. Eddie may want to revert.

---

## Agents Not to Use

Do not use `technical-writer` or `copywriter` agents — those are generalists. The swarm is the specialist lineup. The merger logic is you (Claude), not a sub-agent.
