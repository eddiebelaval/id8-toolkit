# /thrift - the approach gate

**The one question: is this the cheapest mechanism that does the job?**

Cheap meaning all four currencies: compute, latency, tokens, dollars. This is the
Model Cascade (`~/.claude/docs/model-cascade.md`) applied to implementation choice —
work funnels DOWN to the cheapest adequate tier, and a thing built one tier too high
costs that difference forever.

Runs SELF-CONTAINED. No plugin agents (`code-simplifier` and `feature-dev` are `false`
in `settings.json`).

## Where it sits — and why it is FIRST among the change gates

```
/verify     does it work?           green baseline, or nothing below is falsifiable
/thrift     is this the RIGHT WAY?  <- YOU ARE HERE. change the approach
/simplify   what can go?            shrink what survives
/polish     is it finished?         add the edges
/assay      is it worth keeping?    worth
/3pv        is it what he asked?    intent
```

**The chain runs largest blast radius first.** Approach → structure → edges → worth →
intent. Thrift can replace a whole mechanism; simplify only reshapes the one it finds;
polish only fills its gaps. Running them in any other order means shrinking and
finishing code you are about to throw away.

## What separates this from /simplify

`/simplify` works INSIDE the chosen approach and asks whether it could be smaller.
`/thrift` asks whether the approach is right at all. A simplify pass will happily shave
three lines off a bubble sort and never notice it should be a hash lookup. That gap is
what this gate covers, and it is the only thing it covers.

If a finding makes the code shorter but does not change the *mechanism*, it belongs to
`/simplify`. Hand it over rather than doing it here.

## Arguments

- `--files <glob>` — restrict to a path. Default: the branch diff vs base.
- `--dry-run` — report findings, change nothing.
- Empty = the current branch's diff.

---

## Step 0: baseline, and the refusal

```bash
npx tsc --noEmit; echo "tsc=$?"
npm test -- --run > /tmp/gate-tests.log 2>&1; echo "tests=$?"; tail -20 /tmp/gate-tests.log
```

**`npm test` alone hangs in most of these repos** — `test` is aliased to `vitest`,
which is watch mode and never exits. Always pass the one-shot flag (`-- --run`), and
never read a status through a pipe. `$?` after
`... | tail` is *tail's* exit code and is always 0, and bash's `${PIPESTATUS[0]}`
expands to the EMPTY STRING under zsh (which is the shell here) — an empty status
reads as no-failure. Redirect to a file and check `$?` directly, as above.
Each of those mistakes turns a hung or failing suite into a green report.

Record the tsc exit code and the exact test count.

- **Baseline red → STOP.** This gate makes the largest changes in the chain; making
  them on a broken tree means you cannot attribute the breakage.
- **Baseline could not run → report UNVERIFIED**, in those words, and stop. Never emit
  a pass message from a path that did not execute.

**Where a change is performance-shaped, measure BEFORE.** A timing, a query count, a
row count, a token count — whatever the finding claims to improve. An optimisation
with no before-number is a preference, not a finding, and it does not get applied.

---

## Step 1: the five questions

**1. Wrong tier.** The most expensive mistake and the easiest to miss, because the
code works. Walk down the ladder and stop at the first rung that actually does the job:

```
deterministic code  ->  regex / lookup table  ->  Haiku  ->  Sonnet  ->  Opus
```

An LLM call answering a question with one right answer is the flagship case. "Does
this sentence name Rebecca" is a string question — a model would give a different
answer on Tuesday, and cost money to be inconsistent. Same ladder for infrastructure:
a script before a service, a file before a table, a cron before a daemon.

**2. Redundant work.** Recomputing per iteration what is constant across it. Reading
the same file in a loop. Rebuilding the whole thing when an append would do.
Re-fetching what was just fetched. Anything computed and thrown away.

**3. Query shape.** N+1 — a query inside a loop over the results of a query. Sequential
awaits with no dependency between them (should be `Promise.all`). Fetching every row
to filter in memory. Selecting `*` to read one column. Missing an index on a column
that is always filtered on.

**4. Complexity class.** A nested loop over the same collection. A linear scan inside
a linear scan where a `Set` or `Map` makes it one pass. Sorting to find a max. These
matter at real data sizes, not fixtures — check what the collection actually holds in
production before flagging.

**5. Work done at the wrong time.** Computed per request when it could be per build.
Computed per render when it could be per mount. Done eagerly when it is usually not
needed. Done at runtime when the type system settles it at compile time.

## Step 2: what NOT to flag

- **Anything without a measurable before.** No number, no finding.
- **A hot-path claim about cold code.** Confirm it actually runs often. Optimising a
  once-per-deploy script is a cost with no benefit.
- **Readability traded for a gain nobody will notice.** A clever branchless trick that
  saves 40µs on a 300ms request is a net loss — you pay for it at every future read.
- **Anything touching money, consent, auth, or a client surface.** Report it, do not
  apply it.

**The stopping rule: correctness beats cost, always.** A cheaper mechanism that is
wrong more often is not cheaper. If dropping a tier means the answer degrades, the
tier was right — say so in the report and move on. That sentence is the whole reason
this gate can be trusted to run unattended.

## Step 3: apply, one at a time, with the number

Each change: re-measure, and re-run `tsc` + the suite. Same three conditions as
`/simplify` — tsc 0, same test count all green, **no test file edited**. A test that
had to change means behaviour changed, and a behaviour change is not an optimisation.

If the measured gain does not show up, **revert it**. An optimisation that did not
measurably optimise is pure added risk.

## Step 4: report

```
THRIFT — <branch> — <N> files

  baseline    tsc 0 · <K> tests green
  after       tsc 0 · <K> tests green · no test file edited

Applied
  <file:line>  <mechanism> -> <mechanism>
               before: <number>   after: <number>   (<how measured>)

Found, NOT applied
  <file:line>  <finding> — <why: needs a decision / client surface / gain unmeasured>

Correct as built
  <one line per thing checked and deliberately left alone, with the reason>
```

- **The "correct as built" section is the evidence the pass ran.** A report with no
  findings and no checked-list is indistinguishable from a gate that never executed.
- Every applied change carries a before and an after number. No number, no claim.
- Say plainly when the honest answer is "already at the right tier." That is a pass,
  and a gate that always finds something is a gate inventing work.

$ARGUMENTS
