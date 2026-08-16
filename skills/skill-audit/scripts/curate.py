#!/usr/bin/env python3
"""Turn the raw capture ledger into an audit queue.

Capture is deliberately noisy. This is where signal gets separated: it ranks
skills by fault density and, more importantly, names the skills that never
fired at all -- the ones paying context rent with nothing to show for it.

    python3 curate.py --days 30

REPAIRED 2026-07-26 from the upstream skill-audit bundle. Defects fixed:

  1. Upstream keyed installed skills by `skill.parent.name`, so two skills
     with the same directory basename silently collapsed into one -- last
     write wins, one of them invisible. On this machine that erased 37 of
     420 entries. Now keyed by full path; colliding basenames are reported
     as their own finding, because a name collision is itself a MERGE signal.

  2. Upstream counted every SKILL.md under the roots, including copies nested
     in hidden dirs (gstack/.factory/skills/*, gstack/.agents/skills/*).
     Those are NOT registered by Claude Code -- verified: `ship` loads,
     `gstack-ship` does not -- so they cost zero context and must never appear
     as kill candidates. Hidden-dir paths are now excluded.

  3. Invocation names and directory names don't match. The Skill tool reports
     plugin skills as `plugin:skill` while the directory is just `skill`.
     Matching is now alias-based so a used plugin skill is not reported dead.
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Roots must be the REGISTERED surface only -- what actually costs context.
#
# NOT ~/.claude/plugins: that tree contains marketplaces/, a checkout cache of
# every plugin catalog ever browsed (190 stale clones / 71k SKILL.md / 14 GB as
# of 2026-07-26). Globbing it reported 71,427 "installed skills" against a real
# figure of 577. Only plugins/cache/ holds installed plugins -- confirmed against
# every installPath in installed_plugins.json.
# Pre-existing usage instrumentation, wired 2026-07-14 by skill-usage-log.py on
# PostToolUse(Skill), consumed by /assay. It already answers the single most
# valuable question here -- which skills never fire -- so this reads it rather
# than standing up a duplicate capture path and restarting the clock at zero.
USAGE_LOG = "~/Library/Logs/skill-usage/usage.jsonl"

DEFAULT_ROOTS = [
    "~/.claude/skills",
    "~/.claude/plugins/cache",
    ".claude/skills",
]


def _parse_ts(raw: str):
    """Accept both ledger UTC ('...Z') and usage-log naive-local timestamps."""
    dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.astimezone()


def load(path: Path, days: int, kind=None):
    """Read a JSONL event source.

    `kind` forces a kind onto every row, which is how the pre-existing
    skill-usage log is folded in: it predates this skill (wired 2026-07-14 via
    skill-usage-log.py) and has no `kind` field, but every row in it IS an
    invocation. Reusing it means the NEVER FIRED list works off real history
    today instead of starting a fresh 30-day clock.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    rows = []
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            if _parse_ts(row["ts"]) >= cutoff:
                if kind:
                    row["kind"] = kind
                rows.append(row)
        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            continue  # a malformed line must never stall the loop
    return rows


def hidden(path: Path) -> bool:
    """True if any path component is a dotdir other than .claude.

    Skills nested under .factory/ or .agents/ are vendored shadow copies that
    Claude Code does not register. They pay no context rent, so they are not
    kill candidates and counting them inflates the library size.
    """
    return any(p.startswith(".") and p != ".claude" for p in path.parts)


def installed(roots):
    """Map full SKILL.md path -> display name. Path-keyed, so collisions survive."""
    found = {}
    for root in roots:
        p = Path(root).expanduser()
        if not p.exists():
            continue
        for skill in p.glob("**/SKILL.md"):
            try:
                rel = skill.relative_to(p)
            except ValueError:
                continue
            if hidden(rel):
                continue
            if "node_modules" in rel.parts:
                continue
            found[skill] = skill.parent.name
    return found


def aliases(name: str):
    """Every string that could refer to this skill in the ledger."""
    n = name.lower()
    out = {n}
    if ":" in n:                       # plugin:skill -> also match bare skill
        out.add(n.split(":", 1)[1])
    out.add(re.sub(r"^gstack-", "", n))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default="~/.claude/skills/LEDGER.jsonl")
    ap.add_argument("--usage-log", default=USAGE_LOG,
                    help="pre-existing skill-usage-log.py output; folded in as invocations")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--roots", nargs="*", default=DEFAULT_ROOTS)
    ap.add_argument("--show-dead", type=int, default=40,
                    help="max kill candidates to print (0 = all)")
    args = ap.parse_args()

    skills = installed(args.roots)

    rows, sources = [], []
    usage = Path(args.usage_log).expanduser()
    if usage.exists():
        u = load(usage, args.days, kind="invoked")
        rows += u
        sources.append(f"usage-log:{len(u)}")

    ledger = Path(args.ledger).expanduser()
    if ledger.exists():
        l = load(ledger, args.days)
        rows += l
        sources.append(f"ledger:{len(l)}")

    if not sources:
        print(f"\nNo event source found.")
        print(f"  looked for: {usage}")
        print(f"              {ledger}")
        print(f"{len(skills)} skills installed. Nothing to curate.\n")
        return
    invoked = Counter(str(r.get("skill", "")).lower()
                      for r in rows if r.get("kind") == "invoked")
    suspect = Counter(str(r.get("skill", "")).lower()
                      for r in rows if r.get("kind") == "suspect")
    faults = Counter(str(r.get("skill", "")).lower()
                     for r in rows if r.get("kind") == "fault")

    print(f"\n=== {args.days}d window | {len(rows)} events "
          f"({', '.join(sources)}) | {len(skills)} skills installed ===\n")

    if not rows:
        print("Ledger exists but is empty for this window. The clock has started;")
        print("come back after real usage has accumulated.\n")

    # --- name collisions: a MERGE signal in their own right -------------------
    by_name = defaultdict(list)
    for path, name in skills.items():
        by_name[name].append(path)
    dupes = {n: ps for n, ps in by_name.items() if len(ps) > 1}
    if dupes:
        print(f"NAME COLLISIONS -- {len(dupes)} names claimed by 2+ skills "
              f"(merge candidates; trigger surfaces compete):")
        for n, ps in sorted(dupes.items())[:15]:
            print(f"  {n}  ({len(ps)}x)")
        if len(dupes) > 15:
            print(f"  ... and {len(dupes) - 15} more")
        print()

    # --- never fired: the cleanest kill signal available ----------------------
    dead = sorted(
        name for path, name in skills.items()
        if not any(invoked[a] for a in aliases(name))
    )
    if dead:
        shown = dead if args.show_dead == 0 else dead[:args.show_dead]
        print(f"NEVER FIRED -- {len(dead)} kill candidates "
              f"(context cost, zero recorded lift):")
        for s in shown:
            print(f"  {s}")
        if len(dead) > len(shown):
            print(f"  ... and {len(dead) - len(shown)} more "
                  f"(--show-dead 0 for all)")
        print()

    # --- active, ranked by fault density --------------------------------------
    if invoked:
        print("ACTIVE -- ranked by fault density:")
        rank = []
        for s, n in invoked.items():
            if s == "unattributed":
                continue
            bad = faults[s] + suspect[s]
            rank.append((bad / n if n else 0, bad, n, s))
        for density, bad, n, s in sorted(rank, reverse=True)[:15]:
            flag = "   <-- audit" if density > 0.2 and n >= 3 else ""
            print(f"  {s:<34} {n:>4} runs  {bad:>3} faults  {density:>4.0%}{flag}")
        print()

    un = suspect["unattributed"]
    if un:
        attributed = sum(v for k, v in suspect.items() if k != "unattributed")
        print(f"{un} unattributed self-corrections vs {attributed} attributed.")
        if un > attributed * 3:
            print("Unattributed dwarfs attributed: the capture is measuring the")
            print("model, not the skills. Narrow it before trusting the ranking.")
        print()


if __name__ == "__main__":
    main()
