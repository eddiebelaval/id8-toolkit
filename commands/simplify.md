# /simplify - the subtraction gate

**The one question: what can go?**

Every other gate asks whether the code is right, safe, worth keeping, or what he asked
for. This one asks only whether the same behaviour could be expressed in fewer moving
parts.

**The headline is places-a-rule-lives, not line count.** Line count is a proxy and it
lies in one specific direction: collapsing three copies of a formatting rule into one
documented helper plus three calls can END UP LONGER and still be the right call,
because the rule can no longer drift between copies. Report the net delta always, but
judge the pass on duplication killed and call sites collapsed. A net increase is
acceptable ONLY when it buys a genuine collapse — a 50-line abstraction that removes
two duplicates is the failure this rule exists to catch; a 14-line helper that removes
nine duplicated expressions across three idioms is a pass.

Runs SELF-CONTAINED. Do not delegate to `code-simplifier` or `feature-dev:code-reviewer`
— both plugins are disabled in `settings.json`, so a command that reaches for them
reports a clean pass having done nothing. That is the exact failure this file was
written after.

## Where it sits

```
/verify     does it work?           <- REQUIRED FIRST. green baseline or stop
/thrift     is this the right way?  <- the approach changes before the shape does
/simplify   what can go?            <- YOU ARE HERE. subtract
/polish     is it finished?         <- then add: edge cases, empty states, error paths
/assay      is it worth keeping?    <- worth
/3pv        is it what he asked?    <- intent
ship
```

`/finish` runs the whole chain in order.

**Largest blast radius first: approach → structure → edges → worth → intent.** Subtract
before you finish — an empty state written for a component that gets inlined gets
written twice — and let thrift settle the mechanism before you spend effort shrinking
one it is about to replace.

**Not `/cleanup`.** That one is whole-project maintenance — file organisation, stale
docs, unused dependencies, lint, `.env.example`, vulnerable packages — and it ranges
across the repo. This one touches only the current change set and only its code. They
overlap on dead code alone; if the job is "tidy the project", it is `/cleanup`.

## Arguments

- `--files <glob>` — restrict to a path. Default: everything changed on this branch vs base.
- `--dry-run` — report what would go, change nothing.
- Empty = the current branch's diff. The common case.

---

## Step 0: the baseline, and the refusal

A simplification is a claim that behaviour did not change. That claim is unfalsifiable
without a green starting point, so establish one FIRST:

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

Record the exact **test count** and the tsc exit code. Then:

- **Baseline red → STOP.** Report which check failed and its output. Do not simplify a
  broken tree; you will not be able to tell your damage from what was already there.
- **Baseline could not run** (no test script, tsc missing, command hung) → report
  **UNVERIFIED**, in those words, and stop. A fail-open path must never print a pass.
  "No test script" is a finding about the repo, not permission to proceed blind.

Then get the file list:

```bash
BASE=$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)
git diff $BASE...HEAD --name-only
git diff --name-only && git diff --cached --name-only
```

State the scope out loud before touching anything: `N files, M lines, baseline: tsc 0 / K tests green`.

---

## Step 1: read for subtraction

Read every file in scope. Look for these, in rough order of how much they pay:

1. **Duplicated logic** — the same operation written twice. Collapse to one, and put
   it where the narrower caller lives, not in a new `utils/`.
2. **An abstraction with one caller** — a wrapper, a hook, a config object, an
   interface implemented once. Inline it. Indirection earns its keep at two callers.
3. **Dead code** — unreferenced exports, unreachable branches, a flag that is never
   false, a parameter every caller passes the same value for.
4. **Defensive code guarding an impossible state** — a null check on a value the type
   system already guarantees, a try/catch around code that cannot throw.
5. **Conditional chains** — early returns instead of nesting, a lookup table instead
   of a switch that only maps.
6. **Ceremony** — a variable used once on the next line, a comment restating the code,
   a type alias for a primitive, re-exports that only forward.

**Naming is not simplification.** A better name is a polish item. Renaming during a
subtraction pass makes the diff unreadable and hides the deletions inside it.

## Step 2: what you must not touch

- Anything marked `// IMPORTANT: ... DO NOT REMOVE` or equivalent. Honour it silently.
- **Comments explaining WHY.** A comment naming the bug a guard exists for is the most
  valuable text in the file. Deleting it is how the guard gets deleted next year.
- **Test fixtures drawn from real data.** A fixture that looks redundant is usually a
  real case somebody hit. Tidying it makes the test pass and prove nothing.
- **Any code that touches money, consent, auth, or a client surface** — flag it as a
  candidate, do not apply it. Those get a human read.
- Files outside the detected change set. Do not improve the neighbourhood.

## Step 3: apply, one at a time

For each deletion, before you make it, write down **what you believe this code was
for**. If you cannot say, that is not a clean deletion — it is a guess, and it goes in
the report as a candidate for a human instead of an applied change.

Apply in small groups, re-running `tsc` between them. It is much cheaper to find the
one that broke than to bisect twenty.

## Step 4: prove behaviour is unchanged

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

Three conditions, all required:

1. **tsc exit 0.** Read the exit code of `tsc` itself — not of a pipeline whose last
   command was `head` or `tail`.
2. **The same test count, all green.** Fewer tests means you deleted one.
3. **No test file was edited.** Check it: `git diff --name-only | grep -E 'test|spec'`.
   **If a test had to change for the suite to stay green, that is not a simplification
   — it is a behaviour change.** Revert it, and report it as a finding instead.

Any failure: `git checkout -- <file>` on the specific change, re-run, and report what
broke. Revert, do not fix forward — fixing forward inside a subtraction pass is how a
refactor turns into a rewrite.

## Step 5: report

```
SIMPLIFY — <branch> — <N> files

  baseline    tsc 0 · <K> tests green
  after       tsc 0 · <K> tests green · no test file edited
  net         -<X> lines (<before> -> <after>)

Applied
  <file:line>  removed <what>  (-N)   was: <what it did>
  <file:line>  inlined <what>  (-N)   had one caller: <where>

Candidates, NOT applied
  <file:line>  <what>  — <why a human decides: consent / money / could not name its purpose>

Reverted
  <file:line>  <what> — broke <which test / which type>
```

Rules for the report:

- **Report the net line delta always, and never hide a positive one.** If it went up,
  say so in the headline and name the collapse that bought it. Do not pad the report
  with renames to look busy.
- **Nothing to simplify is a real and common outcome.** Report it as PASS with a net
  of 0 and one line on what you looked for. A pass that always finds something is
  a pass that is inventing work.
- Every candidate names the specific reason a human is deciding instead of you.

$ARGUMENTS
