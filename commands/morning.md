# /morning - Daily Morning Brief

Load context, check status across all projects, surface priorities for the day.

## Pre-computed Context

```bash
TODAY=$(date +%Y-%m-%d)
DAY_OF_WEEK=$(date +%A)
```

**Date:** $TODAY ($DAY_OF_WEEK)

## Process

### 1. Load Memory Context

Read `~/.claude/MEMORY.md` for:
- Active projects and their status
- Current focus area
- Any deadlines or reminders

Read `~/.claude/projects/-Users-eddiebelaval-Development/memory/session-log.md` for:
- What was worked on yesterday
- Any unfinished tasks or blockers

### 1b. Warden Posture (Sentinel Swarm)

Read `~/.claude/argus-fortress/POSTURE.md` — the overnight Sentinel Swarm verdict.
- **GREEN**: one line, "Fortress GREEN", move on.
- **YELLOW**: surface the single ranked finding near the top of the brief.
- **RED**: lead with it — Eddie was already pinged, but it heads the brief.
If the file is missing or its date is not today, note "Warden swarm did not report" (do not fabricate a posture).

### 2. Cross-Project Git Status

Check each active project for uncommitted work and open PRs:

```bash
# Homer
cd ~/Development/Homer && echo "=== HOMER ===" && git status -s && git log --oneline -3

# Parallax
cd ~/Development/id8/products/parallax && echo "=== PARALLAX ===" && git status -s && git log --oneline -3

# Rune
cd ~/Development/id8/products/rune && echo "=== RUNE ===" && git status -s && git log --oneline -3

# Vox
cd ~/Development/id8/products/vox && echo "=== VOX ===" && git status -s && git log --oneline -3

# Claude Code Artifacts
cd ~/Development/claude-code-visualize && echo "=== ARTIFACTS ===" && git status -s && git log --oneline -3
```

Check for open PRs across repos:
```bash
gh pr list --state open --json title,url,repository 2>/dev/null
```

### 3. Active Tasks

Scan workspace task directories for active tasks:

```bash
# Homer tasks
ls ~/Development/Homer/workspace/tasks/*.md 2>/dev/null

# Parallax tasks
ls ~/Development/id8/products/parallax/workspace/tasks/*.md 2>/dev/null
```

Sort by priority (high > medium > low).

### 4. Infrastructure Health

Check HYDRA job status:
```bash
launchctl list | grep -i hydra 2>/dev/null
```

Check for any failed launchd jobs:
```bash
launchctl list | grep -E "hydra|vox|e2e" 2>/dev/null
```

### 5. Deadlines & Reminders

Check MEMORY.md for any upcoming deadlines. Known recurring:
- Annual Report: May 1, 2026 ($138.75)
- Capital One Spark Classic: Call by March 10, 2026

### 6. Triangle Health Check

For each active project that has VISION.md + SPEC.md at its root:

1. Read SPEC.md frontmatter for `last-reconciled` date
2. Count git commits since that date: `git log --oneline --since="[date]" | wc -l`
3. Check BUILDING.md for entries newer than last reconciliation

Report inline:
```
TRIANGLE HEALTH
- [Project]: CURRENT (reconciled [date])
- [Project]: DRIFTED — [N] commits since reconcile on [date]
```

If any project has >5 commits since last reconciliation, use AskUserQuestion:
- "[PROJECT] has [N] commits since SPEC was last reconciled [date]. Quick sync?"
- Options: "Reconcile now" / "Skip today" / "Nothing meaningful, bump date"

Known triangle projects: Parallax (`~/Development/id8/products/parallax`), Homer (`~/Development/Homer`), Rune (`~/Development/id8/products/rune`)

### 7. Upstream Contributions Check

Quick check on open source contribution activity:
- Read `~/Development/upstream-contributions/TRACKER.md`
- Check for responses on filed issues (use `gh` CLI to check issue status)
- If it's Friday: flag any Bug Journal entries from the week that need investigation
- If unverified bugs have been logged for >3 days, remind to investigate or discard

```bash
# Check Lightpanda issue responses
gh issue view 1800 --repo lightpanda-io/browser --json state,comments 2>/dev/null
gh issue view 1801 --repo lightpanda-io/browser --json state,comments 2>/dev/null
gh issue view 1802 --repo lightpanda-io/browser --json state,comments 2>/dev/null
```

Report inline:
```
UPSTREAM
- [Repo]: [N] issues filed, [status of responses]
- Bug journal: [N] unverified entries
```

### 8. Life Triad Health Check

Check the life triangle at `~/life/` for staleness and alignment.

#### Auto-Scan

```bash
# Check last-updated dates in all life files
for f in HEADING NOW GOALS MONEY PEOPLE BODY RHYTHM; do
  echo "=== $f ===" && grep -i "last updated" ~/life/$f.md 2>/dev/null || echo "no date found"
done
```

Staleness thresholds:
- NOW.md: >3 days = flag
- GOALS.md: >7 days = flag (weekly section must match current week)
- MONEY.md, PEOPLE.md, BODY.md: >14 days = flag
- HEADING.md, RHYTHM.md: >30 days = flag

#### Goal Deadline Check

Parse GOALS.md "This Week" section. If the date range doesn't include today, flag as stale.
Check "This Month" goals -- if it's the last week of the month, flag for review.

#### Auto-Update NOW.md Observable Fields

Read recent git activity across active repos (last 24h) and session-log.md.
If NOW.md Work section is >3 days stale, auto-update the observable fields:
- Session count (approximate from logs)
- Last active projects
- Do NOT touch: mental state, relationships, health, revenue

Update the "Last updated" date in NOW.md if auto-updates were made.

#### Life Alignment Report

```
LIFE ALIGNMENT
- HEADING: [CURRENT / N days since update]
- NOW: [CURRENT / auto-updated today / N days stale]
- GOALS: [This Week current / stale -- needs refresh]
- MONEY/PEOPLE/BODY: [CURRENT / N days stale]
```

#### Life Delta Report

Read `~/life/DELTA.md`. If it exists and is <7 days old, include in the brief:

```
LIFE DELTA: [NET STATUS] (computed [date])
- Top commitments: [top 2 from this week's actions]
- Diverging: [any dimensions flagged as diverging, or "none"]
```

Also query `life_commitments` from hydra.db for the current week:
```bash
sqlite3 ~/.hydra/hydra.db "SELECT dimension, commitment, score FROM life_commitments WHERE week = '$(date +%G-W%V)' ORDER BY dimension;"
```

If mid-week or later, show scored vs pending counts.

If any file exceeds its staleness threshold, use AskUserQuestion:
- "[FILE] hasn't been touched in [N] days. Quick update?"
- Options: "Update now" / "Skip" / "Nothing changed, bump date"

If it's Friday, prompt for weekly GOALS review:
- "It's Friday. Want to review This Week goals and set next week?"
- Options: "Yes" / "Skip this week"

If it's the 1st of the month (or first /morning of the month), prompt for monthly review:
- "New month. Full life reconcile?"
- Options: "Full review" / "Just goals" / "Skip"

### 9. Present Morning Brief

Format the output as a concise brief:

```
Morning Brief - [date]

YESTERDAY
- [Summary of last session's work]

UNCOMMITTED WORK
- [Project]: [description of changes]

OPEN PRs
- [PR title] -> [repo] (ready to merge? / needs review?)

PRIORITY TASKS
1. [High priority task]
2. [Medium priority task]
3. [Low priority task]

INFRASTRUCTURE
- HYDRA: [status]
- Vox: [status]

DEADLINES
- [Any upcoming deadlines within 30 days]

LIFE DELTA: [NET STATUS] (computed [date])
- [Top 2 commitments for the week]
- Diverging: [dimensions or "none"]

RECOMMENDED FOCUS
Based on priorities and momentum: [recommendation]
```

## Notes

- This command takes no arguments — it figures out what matters
- Keep the brief concise (fit on one screen)
- Recommend focus based on: deadlines > blockers > momentum > new work
- If it's Monday, include a week-ahead view
- If a project has been dormant >7 days, mention it as "needs attention" or "intentionally paused"
