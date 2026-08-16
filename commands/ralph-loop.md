---
name: ralph-loop
description: /ralph-loop - Verify work was done correctly before marking complete
---

# Ralph Loop - Work Verification

> Named after Ralph Wiggum — catches the obvious mistakes before they embarrass you.

## Purpose

Implements a feedback loop that confirms work was executed properly. Run after completing a chunk of work to verify it's actually working before moving on.

## When to Use

- After completing a feature or set of changes
- Before marking a task as complete
- Before committing significant changes
- After each phase of a multi-phase implementation

## Process

### 1. Identify What Changed

Check git diff for modified files and categorize them:
- **Pages/Routes** — New or modified page components
- **API Routes** — Backend endpoints
- **Components** — UI components
- **Database** — Migrations, schema changes
- **Config** — Configuration files, environment

### 2. Run Appropriate Checks

| Context | Verification Method |
|---------|---------------------|
| New pages/routes | Navigate with Playwright, check 200 status, no console errors |
| API routes | Call endpoints, verify response shape |
| Database changes | Run migration, verify schema |
| Components | Check TypeScript, run relevant tests |
| Builds | `npm run build`, verify no errors |
| Links | Check all hrefs resolve |
| Types | `npm run typecheck` or `npx tsc --noEmit` |

### 3. Report Results

```
RALPH LOOP VERIFICATION
=======================

Context: [what was worked on]
Files Changed: [count]

Checks Performed:
  [x] TypeScript compilation
  [x] Build succeeds
  [x] Routes accessible
  [ ] Console errors (FAILED - see below)

Result: PASS / FAIL

Issues Found:
  - [specific issue with file:line if applicable]

Suggested Fixes:
  - [actionable fix]
```

### 4. Fix or Escalate

- **Auto-fix simple issues**: Missing imports, type errors with obvious fixes
- **Report complex issues**: For user decision or further investigation

## Usage

After completing work:
```
/ralph-loop
```

With specific scope:
```
/ralph-loop pages
/ralph-loop api
/ralph-loop build
/ralph-loop types
```

## Verification Checklist by Work Type

### New Page Created
- [ ] Route accessible (200 status)
- [ ] No TypeScript errors
- [ ] No console errors in browser
- [ ] Mobile responsive (check viewport)
- [ ] Links resolve correctly

### API Route Created
- [ ] Endpoint returns expected shape
- [ ] Error cases handled
- [ ] Auth required routes reject unauthenticated requests

### Database Migration
- [ ] Migration applies cleanly
- [ ] Rollback works
- [ ] Types regenerated (`supabase gen types`)

### Component Updated
- [ ] No TypeScript errors
- [ ] Component renders without crashing
- [ ] Props validated
- [ ] Related tests pass

### Build Verification
- [ ] `npm run build` succeeds
- [ ] No type errors
- [ ] No unused imports/variables warnings

## Integration with ID8Pipeline

Ralph Loop is your gate keeper between phases:

| Phase Transition | Ralph Loop Scope |
|------------------|------------------|
| Stage 4 → 5 | `build` - Foundation working |
| Stage 5 → 6 | `pages api` - Features complete |
| Stage 6 → 7 | `build types` - Integration solid |
| Stage 7 → 8 | Full verification |

## Philosophy

> "I'm helping!" — Ralph Wiggum

Better to catch mistakes now than discover them in production. Ralph Loop is your safety net that prevents "it works on my machine" syndrome.

The goal isn't perfection — it's catching the obvious problems before they become embarrassing.
