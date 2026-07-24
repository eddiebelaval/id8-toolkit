---
name: Ship
slug: ship
description: Full delivery pipeline — preflight, polish, commit, push, PR, merge in one command
category: operations
complexity: complex
version: "1.0.0"
author: "id8Labs"
triggers:
  - "ship"
  - "ship it"
  - "push and merge"
  - "create pr and merge"
  - "deliver this"
tags:
  - delivery
  - git
  - pipeline
  - operations
---

# Ship — Full Delivery Pipeline

Stage, commit, push, PR, merge, and verify — end-to-end shipping in one command. Respects all CLAUDE.md rules (preflight, no squash, regular merges, branch protection).

## Core Workflows

### Workflow 1: Full Ship (Default)
1. Detect context (project, branch, base)
2. Run preflight checks (typecheck, build, lint, tests)
3. Code quality pass (3 parallel review agents: reuse, quality, efficiency)
4. Stage and commit changes
5. Push to remote
6. Create PR
7. Merge (regular merge, no squash)
8. Verify merge succeeded

## Usage

```
/ship                          # Ship current branch changes with auto-generated commit message
/ship "feat: add auth flow"    # Ship with explicit commit message
/ship --no-merge               # Create PR but don't merge (for review)
/ship --base dev               # Target a specific base branch (default: main)
/ship --no-polish              # Skip the code quality pass (faster, for trivial changes)
/ship --dry-run                # Show what would happen without doing anything
```

## Instructions

### Step 0: Detect Context

1. Identify: project name, current branch, base branch (default: `main`).
2. State: "Shipping [PROJECT] | Branch: [BRANCH] -> [BASE]"
3. If on `main` — STOP. "Cannot ship from main. Create a feature branch first."
4. If working tree is clean and no commits ahead of base — STOP. "Nothing to ship."

### Step 1: Preflight Checks (MANDATORY)

Run ALL checks before proceeding. If any fail, fix them before continuing.

```bash
# 1. Type check (TypeScript projects)
npx tsc --noEmit 2>&1

# 2. Build
npm run build 2>&1

# 3. Lint (if available)
npm run lint 2>&1

# 4. Tests (if available)
npm test -- --passWithNoTests 2>&1
```

For Python projects, substitute:
```bash
python -m py_compile <changed_files>
pytest -x -q 2>&1
```

**If any check fails:**
- Fix the issue
- Re-run the failing check
- Maximum 2 fix attempts per check — if still failing after 2 fixes, STOP and report

If `--dry-run`: Show preflight results and exit.

### Step 1.5: Code Quality Pass (AUTO)

After preflight passes but BEFORE committing, run an automated quality sweep on the changed files. This catches the issues that tests and type-check miss: duplicate code, missing CSS, broken abstractions, memory leaks, unmemoized hot paths.

1. Get the diff: `git diff HEAD` (or `git diff --cached` if files are staged)
2. If the diff is trivial (< 20 lines changed, or only config/docs), SKIP this step.
3. Launch THREE review agents **in parallel** (use the Agent tool), passing each the full diff:

   **Agent 1 (Reuse):** Search for existing utilities/helpers that could replace new code. Flag duplicates, inline logic that could use existing utils, overlapping components.

   **Agent 2 (Quality):** Check for redundant state, copy-paste variations, stringly-typed code, leaky abstractions, missing CSS classes referenced by components, divergent types that should be unified.

   **Agent 3 (Efficiency):** Check for unbounded data structures, missing cleanup, unmemoized computations in render paths, per-request allocations that should be singletons, duplicate filtering.

4. Aggregate findings. Fix each issue directly (skip false positives silently).
5. If fixes were made, re-run preflight (Step 1) to confirm nothing broke.
6. Proceed to Step 2.

**Skip conditions:** `--no-polish` flag, or `--dry-run` mode.

### Step 2: Stage and Commit

1. Check `git status` for unstaged/untracked changes.
2. Stage relevant files (prefer specific files over `git add -A`):
   - NEVER stage `.env`, credentials, or secret files
   - NEVER stage `node_modules/`, `.next/`, `dist/`, `__pycache__/`
3. If no commit message was provided in args:
   - Analyze the diff to generate a descriptive commit message
   - Follow the project's commit convention:
     - ID8 Pipeline projects: `[Stage N: Name] type: description`
     - Other projects: conventional commits (`feat:`, `fix:`, `refactor:`, etc.)
   - End with `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`
4. If a commit message WAS provided, use it exactly (still append Co-Authored-By).

Use HEREDOC for the commit message:
```bash
git commit -m "$(cat <<'EOF'
commit message here

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

### Step 3: Push

1. Check if branch has an upstream: `git rev-parse --abbrev-ref @{upstream} 2>/dev/null`
2. If no upstream: `git push -u origin [BRANCH]`
3. If upstream exists: `git push`
4. Verify push succeeded.

### Step 4: Create PR

1. Check if a PR already exists for this branch: `gh pr list --head [BRANCH] --state open`
2. If PR exists: skip creation, show existing PR URL.
3. If no PR:
   - Generate title from commit(s) — keep under 70 characters
   - Generate body with:
     ```
     ## Summary
     <1-3 bullet points from the diff>

     ## Verification
     - Build: PASS
     - TypeCheck: PASS
     - Tests: PASS/SKIPPED
     - Lint: PASS/SKIPPED

     Generated with [Claude Code](https://claude.com/claude-code)
     ```
   - Create: `gh pr create --title "..." --body "..." --base [BASE]`

### Step 5: Merge (unless --no-merge)

1. Wait for CI checks if any are running: `gh pr checks [PR_NUMBER] --watch`
   - Timeout after 5 minutes — if still pending, report and skip merge
2. **NEVER squash merge.** Always use: `gh pr merge [PR_NUMBER] --merge`
3. If merge fails (conflicts, failed checks):
   - Report the failure
   - Do NOT force merge
   - Exit with the PR URL so Eddie can review

### Step 5b: Cortex Decision Capture (after merge)

After a successful merge, record the decision in Cortex so future sessions and other surfaces know what shipped:

1. Use the `mcp__cortex__cortex_write` tool (if available) to write a context object:
   - **type:** `decision`
   - **title:** The PR title (e.g., "feat: add auth flow for Parallax")
   - **body:** 1-2 sentence summary of what was shipped and why. Include the PR URL.
   - **project:** The detected project name from Step 0
   - **tags:** `["shipped", "pr-merge"]`
   - **confidence:** `high`

2. If the MCP tool is not available, skip silently — do not block the ship pipeline.

### Step 6: Cleanup and Report

1. After successful merge:
   - `git checkout [BASE] && git pull`
   - Delete the feature branch: `git branch -d [BRANCH]`
   - Delete remote branch: `git push origin --delete [BRANCH]` (only if we created it this session)
2. Output final report:

```
Ship Complete
=============
Branch:  [BRANCH] -> [BASE]
Commit:  [SHORT_SHA] [message]
PR:      [URL]
Merged:  YES/NO
Build:   PASS
Tests:   PASS/SKIPPED

Cleanup: local branch deleted, remote branch deleted
```

If `--no-merge`:
```
PR Created (not merged)
=======================
Branch:  [BRANCH] -> [BASE]
Commit:  [SHORT_SHA] [message]
PR:      [URL]
Status:  Ready for review

Merge manually: gh pr merge [NUMBER] --merge
```

## Rules

| Rule | Why |
|------|-----|
| NEVER ship from main | Branch protection — always use feature branches |
| NEVER squash merge | Preserves granular commit history (CLAUDE.md rule) |
| Preflight is mandatory | Build/test/lint must pass before push |
| Never stage secrets | .env, credentials, API keys stay local |
| Never force merge | If it conflicts, Eddie decides |
| Always use --merge flag | Regular merges, not squash or rebase |
| Report PR URL | Eddie needs the link for tracking |
