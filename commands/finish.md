# /finish - run the whole quality chain

**One command for Stage 8.** Runs every gate in order, stops on a red, and reports
each one's real state — including the ones that did not run.

This is the definition-of-done doctrine made executable: *the last mechanical step is
yours*. `/finish` is what "done" means for code.

## The chain

```
1  /verify     does it work?           green baseline. everything below depends on it
2  /thrift     is this the right way?  change the APPROACH
3  /simplify   what can go?            shrink what survives
4  /polish     is it finished?         add the edges
5  /assay      is it worth keeping?    worth
6  /3pv        is it what he asked?    intent
```

**Order is load-bearing: largest blast radius first.** Approach → structure → edges →
worth → intent. Each gate operates inside the result of the one before it. Reordered,
the later gates spend their effort on code the earlier ones would have replaced.

Gates 2–4 CHANGE code. Gates 5–6 JUDGE it and change nothing.

## Arguments

- `--from <gate>` — start partway (`/finish --from simplify`). Baseline still runs.
- `--only <gate>[,<gate>]` — run just these, plus the baseline.
- `--skip <gate>[,<gate>]` — force-skip, recorded as SKIPPED(forced) in the report.
- `--dry-run` — every gate reports findings, nothing is applied.
- Empty = all six on the current branch's diff. The common case.

---

## THE ONE RULE

**A gate that did not run must never render as a gate that passed.**

Three terminal states, visually distinct, never collapsed:

| State | Means |
|---|---|
| **PASS** | ran to completion on the real target |
| **SKIPPED** | deliberately not run — *always carries its reason* |
| **STOP** | ran and failed, or could not run (UNVERIFIED) |

A run of six gates where four were skipped is a **2/6 run**, and the summary line says
so. It is not a green checkmark. This is the whole reason the runner exists as its own
file rather than as a sentence telling you to run five commands: a human running them
by hand skips silently and remembers a pass.

---

## Step 0: baseline (never skippable)

```bash
BASE=$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)
git diff $BASE...HEAD --name-only; git diff --name-only; git diff --cached --name-only
npx tsc --noEmit; echo "tsc=$?"
npm test -- --run > /tmp/gate-tests.log 2>&1; echo "tests=$?"; tail -20 /tmp/gate-tests.log
```

**`npm test` alone hangs in most of these repos** — `test` is aliased to `vitest`,
which is watch mode and never exits. Always pass the one-shot flag (`-- --run`), and
never read a status through a pipe. `$?` after
`... | tail` is *tail's* exit code and is always 0, and bash's `${PIPESTATUS[0]}`
expands to the EMPTY STRING under zsh (which is the shell here) — an empty status
reads as no-failure. Redirect to a file and check `$?` directly, as above. Either mistake turns a hung or failing suite into a green report, which is
precisely the failure this runner exists to make impossible.

Record: file count, tsc exit, **exact test count**. This is the number every later gate
compares against.

- **Red → STOP the whole run.** Report which check failed, with its output. Do not
  proceed; a chain run on a broken tree cannot attribute its own damage.
- **Could not run → UNVERIFIED, stop.** No test script, tsc missing, a hang. Say which,
  in those words.
- **Empty change set → stop and say so.** Nothing to finish is not a pass.

## Step 1: decide which gates are appropriate

Decide BEFORE running, from the change set, and write the decision into the report.
Default is to run. Skip only on these grounds:

| Gate | Skip when | Never skip when |
|---|---|---|
| `/thrift` | pure copy, markup, docs, or config — no logic, no queries, no loops | anything with a query, a loop, a model call, or a new dependency |
| `/simplify` | — *never skip.* it is cheap and always applies | — |
| `/polish` | nothing user-facing and no new entry point | any route, form, handler, or exported function changed |
| `/assay` | nothing NEW was created — only edits to existing artifacts | a new skill, command, script, table, route, or doc was added |
| `/3pv` | mechanical work with no stated ask (a rename, a version bump) | the session began with a request in the user's own words |

Anything not covered by a row above: **run it.** When unsure, run it — a gate that
runs and finds nothing costs a few minutes; a gate skipped on a hunch costs the finding.

## Step 2: run them in order

For each gate: read its command file and follow it. They are self-contained by
design — **do not delegate to `code-simplifier` or `feature-dev:code-reviewer`, which
are `false` in `settings.json` and would return a clean report having run nothing.**

Between gates:

- `npx tsc --noEmit` after **every** gate that applied a change. Fast, catches most.
- Full suite after every CHANGE gate (2–4) that applied a change. If a gate applied
  nothing, there is nothing to verify — say "no changes, verification not needed"
  rather than running the suite to produce a meaningless green.
- **Test count must never decrease.** Thrift and simplify hold it constant; polish may
  raise it. A drop means a test was deleted — STOP and report it.
- **No test file may be edited by gates 2–3.** `git diff --name-only | grep -E 'test|spec'`.
  A changed test under a refactor gate means behaviour changed. Revert, report, continue.

**On a red mid-chain:** revert that gate's specific change, re-verify, and record it as
STOP with what broke. Then **keep going with the remaining gates** — one failed gate
does not cancel the rest, and stopping the whole chain on one revert is how the last
three gates never get run. (Exception: a red baseline in step 0 stops everything,
because nothing downstream is interpretable.)

## Step 3: the report

One table. Every gate appears, including skipped ones.

```
FINISH — <branch> — <N> files

  baseline   tsc 0 · <K> tests green
  final      tsc 0 · <K+n> tests green · build 0

  1 verify     PASS       <K> tests, tsc 0
  2 thrift     PASS       1 applied · <before> -> <after>
  3 simplify   PASS       -<X> lines
  4 polish     PASS       2 fixed, 1 found-not-fixed
  5 assay      SKIPPED    nothing new was created, only edits
  6 3pv        PASS       matches the ask

  5/6 ran · 1 skipped

Applied         <one line each, with its receipt: number, line delta, or failing input>
Not applied     <one line each, with who decides and why>
Reverted        <one line each, with what broke>
Needs Eddie     <only genuine blocks — a decision, a credential, a client-surface call>
```

Rules:

- **The count line is mandatory** — `5/6 ran · 1 skipped`. It is the one line that
  makes a partial run impossible to mistake for a full one.
- Every skip prints its reason. "SKIPPED" alone is a bug in the report.
- Every applied change carries its receipt: a measured number (thrift), a line delta
  (simplify), or the concrete input that used to break (polish).
- **Nothing found is a real outcome.** Say so plainly. Do not pad.
- **Never auto-apply** anything touching money, consent, auth, or a client surface —
  those land in "not applied" regardless of which gate found them.
- Shipping stays Eddie's gate. `/finish` never commits, pushes, or deploys.

$ARGUMENTS
