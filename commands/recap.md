# /recap - Friday Weekly Recap (5 min)

Score the week against Monday's war room commitments.

## Process

1. Find this week's war room file:
```bash
# Find the most recent Monday's war room file
ls ~/Development/id8/war-room/*.md 2>/dev/null | tail -1
```

2. Read the file. Extract the Commitments section and The One Thing.

3. For each commitment, score it:
   - **DONE** — Shipped, merged, sent, or completed
   - **PARTIAL** — Started but not finished
   - **MISSED** — Didn't happen

4. Score The One Thing separately (this is the headline).

5. Pull quick metrics to compare against Monday's scorecard:
   - Any new signups?
   - Any content published?
   - Any PRs merged?

6. Append to the war room file:

```markdown
## Friday Recap — [date]

### The One Thing: [DONE/PARTIAL/MISSED]
[One line on what happened]

### Commitments
- [x] Commitment 1 — DONE
- [ ] Commitment 2 — MISSED (reason)
- [~] Commitment 3 — PARTIAL (what's left)

### Week Score: [N]/[total] commitments done

### Carry Forward
- [Anything that missed and still matters]

### Wins
- [Best thing that happened this week, even if unplanned]
```

7. Update `session-log.md` with recap summary.

## Rules
- Be honest. MISSED means missed. Don't soften it.
- Carry forward is mandatory for missed items. They don't disappear.
- Wins section exists because momentum matters. Always find at least one.
