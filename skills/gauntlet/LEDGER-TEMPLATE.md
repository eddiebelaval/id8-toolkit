# LEDGER

**Goal:** <one line>
**Workdir:** <path>
**Bar seal (sha256):** <hash>  <- re-verified at the start of every wave
**Started:** <YYYY-MM-DD HH:MM TZ>
**Engine:** workflow | agent-fanout

## Pieces

| ID | Contract | Bar criteria | Artifact path |
|----|----------|--------------|---------------|
| P1 | <one line> | 1, 3 | <path> |
| P2 | | | |

---

## Rounds

Append only. One row per piece per round. Never edit a prior row.

| Wave | Piece | Round | Verdict | Score | Delta | Gap named | Evidence |
|------|-------|-------|---------|-------|-------|-----------|----------|
| 1 | P1 | 1 | LOSES | 5.5 | -- | <single largest gap> | <path to screenshot / test output> |

Verdicts: `BEATS_BAR` | `TIES` | `LOSES`
Delta: score change vs this piece's previous round.

---

## Tend passes

| Wave | Conflicts resolved | Files touched | Notes |
|------|--------------------|---------------|-------|
| 1 | | | |

---

## Status

| Piece | Final state | Rounds used | Final score | Remaining gap |
|-------|-------------|-------------|-------------|---------------|
| P1 | beats_bar / converged / capped | | | |

Convergence = score delta below 0.5 for three consecutive rounds, or the same gap named
three times. Capped = hit `--max-rounds` still short of the bar. Both are reported
honestly in the final report; neither is presented as a win.

---

## Halts

| When | Condition | What was surfaced |
|------|-----------|-------------------|
| | | |
