# /3pv - 3-point verification (alias for /plumb)

Run the three-gate close-out on this session: **PLUMB** (did we build what we set out to
build, or veer?), **SQUARE** (is every corner finished, charter *and* veers?), **LEVEL**
(does it actually function, per the original ask?).

Load and follow the skill at `~/.claude/skills/plumb/SKILL.md`. Execute it end to end.

## Arguments
$ARGUMENTS

## Quick Reference
- (none) — verify the current session against turn 1's charter
- `--session <uuid>` — verify a past session
- `--list` — list recent sessions with timestamps, then stop
- `--cwd <repo>` — verify a session from a different project
- `gate1` / `gate2` / `gate3` — run a single gate only
- `report-only` — no auto-remediation; findings and receipts only

## The rule that governs this command

No verdict without a receipt. Unproven is **UNVERIFIED**, never PASS. Never commit or push
to close a loop — the human gate stays.
