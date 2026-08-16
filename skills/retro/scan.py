#!/usr/bin/env python3
"""
retro/scan.py -- the committed reach + classification engine for /retro.

Exists because two failure modes recur when this logic is re-derived as inline
shell each run:

  1. WRONG REACH. `find -maxdepth 2 -name .git -type d` + local `main` can
     undercount human commits ~3x. Submodules store .git as a FILE, worktrees live
     at depth 3, and work lands on branches other than main. This scans depth 4,
     accepts .git as file OR dir, EXCLUDES .worktrees/ (shares parent object DB),
     uses `git log --all`, and dedupes globally by commit SHA.

  2. TEST PATHS WITHOUT A LEADING SLASH. A `test/foo.mjs` dir (no leading slash)
     slips past a `/tests?/` regex, mislabeling test LOC as code. The classifier
     below anchors on (^|/).

PRs: GitHub squash-merges stamp ` (#NNN)` on the subject and are authored as the
merging identity, so a filter on your commit name alone can miss them. This counts
`(#NNN)`-stamped human subjects plus classic merge-pr commits.

IDENTITY (portable): "human" commits are yours. By default this AUTO-DETECTS your
git identity from `git config user.name` / `user.email` in the first repo it finds
(or the current dir). Override with --authors "Name One" "name@email" ... or the
RETRO_AUTHORS env var (comma-separated). Everyone else is counted as "automated".

Usage:
  python3 scan.py --days 7
  python3 scan.py --since "2026-08-06 22:00:00"
  python3 scan.py --days 7 --roots ~/Development ~/code
  python3 scan.py --days 7 --authors "Jane Dev" "jane@acme.com"
Prints a single JSON object to stdout. Everything the narrative needs is in it.
"""
import argparse, json, os, re, subprocess, sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

EXCLUDE_SUBSTR = ["/plugins/marketplaces/", "/.worktrees/"]
BULK_THRESHOLD = 60000  # single-commit insertions above this = import/synthetic; excluded + reported


def sh(args, cwd=None, timeout=90):
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout).stdout
    except Exception:
        return ""


def find_repos(roots):
    repos = set()
    for root in roots:
        root = os.path.expanduser(root)
        if not os.path.isdir(root):
            continue
        # depth 4, .git as file or dir
        out = sh(["find", root, "-maxdepth", "4", "-name", ".git", "-type", "d"]) \
            + sh(["find", root, "-maxdepth", "4", "-name", ".git", "-type", "f"])
        for line in out.splitlines():
            p = line.strip()
            if not p:
                continue
            repo = p[:-5] if p.endswith("/.git") else os.path.dirname(p)
            if any(s in repo + "/" for s in EXCLUDE_SUBSTR):
                continue
            repos.add(repo)
    return sorted(repos)


def resolve_identity(cli_authors, repos):
    """Return (human_set, author_patterns).

    human_set   -- lowercased strings compared against %an for the human flag.
    author_patterns -- strings passed to `git log --author=` (OR-matched) for the streak scan.

    Priority: --authors flag  >  RETRO_AUTHORS env  >  auto-detect from git config.
    """
    raw = list(cli_authors) if cli_authors else []
    if not raw:
        env = os.environ.get("RETRO_AUTHORS", "")
        if env.strip():
            raw = [a.strip() for a in env.split(",") if a.strip()]
    if not raw:
        # auto-detect from the first repo (or cwd) git config
        probe_dirs = repos[:1] or ["."]
        for d in probe_dirs:
            name = sh(["git", "-C", d, "config", "user.name"]).strip()
            email = sh(["git", "-C", d, "config", "user.email"]).strip()
            if name:
                raw.append(name)
            if email:
                raw.append(email)
            if raw:
                break
    # build the lowercase membership set (name, email, email local-part)
    human_set = set()
    patterns = []
    for a in raw:
        if not a:
            continue
        patterns.append(a)
        human_set.add(a.strip().lower())
        if "@" in a:
            human_set.add(a.split("@", 1)[0].strip().lower())
    return human_set, patterns


def is_test(f):
    return bool(re.search(r"(\.(test|spec)\.[a-z0-9]+$|(^|/)__tests__/|(^|/)tests?/|\.test\.mjs$|\.spec\.mjs$)", f))


def is_prose(f):
    return f.lower().endswith((".md", ".mdx", ".txt"))


def is_html(f):
    return f.lower().endswith((".html", ".htm"))


def is_generated(f):
    return (f.endswith(("package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Cargo.lock", "poetry.lock"))
            or "/drizzle/meta/" in f or f.endswith((".min.js", ".min.css"))
            or "/dist/" in f or "/build/" in f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--since", type=str, default=None, help="explicit git --since string (overrides --days)")
    ap.add_argument("--roots", nargs="+", default=["~/Development", "."])
    ap.add_argument("--authors", nargs="+", default=None,
                    help="your git identities (name and/or email). Overrides auto-detect.")
    ap.add_argument("--tz-hours", type=int, default=-4, help="display TZ offset in hours (default ET, -4)")
    args = ap.parse_args()

    tz = timezone(timedelta(hours=args.tz_hours))
    now = datetime.now(tz)
    if args.since:
        since = args.since
        since_label = args.since
    else:
        since_dt = now - timedelta(days=args.days)
        since = since_dt.strftime("%Y-%m-%d %H:%M:%S")
        since_label = since

    repos = find_repos(args.roots)
    human_authors, author_patterns = resolve_identity(args.authors, repos)

    seen = set()
    commits = []
    for repo in repos:
        log = sh(["git", "-C", repo, "log", "--all", "--no-merges", f"--since={since}",
                  "--pretty=format:@@@%H|%an|%at|%s"])
        for line in log.splitlines():
            if not line.startswith("@@@"):
                continue
            try:
                h, an, at, subj = line[3:].split("|", 3)
            except ValueError:
                continue
            if h in seen:
                continue
            seen.add(h)
            commits.append({"h": h, "an": an, "at": int(at), "subj": subj,
                            "repo": os.path.basename(repo), "path": repo,
                            "human": an.strip().lower() in human_authors})

    sha_meta = {c["h"]: c for c in commits}
    # numstat per deduped sha
    for repo in repos:
        out = sh(["git", "-C", repo, "log", "--all", "--no-merges", f"--since={since}",
                  "--pretty=format:@@@%H", "--numstat"])
        cur = None
        for line in out.splitlines():
            if line.startswith("@@@"):
                cur = line[3:].strip()
                continue
            if cur is None or cur not in sha_meta:
                continue
            m = re.match(r"^(\d+|-)\t(\d+|-)\t(.+)$", line)
            if not m:
                continue
            ins = int(m.group(1)) if m.group(1) != "-" else 0
            f = m.group(3)
            c = sha_meta[cur]
            c["ins"] = c.get("ins", 0) + ins
            if is_test(f):
                c["test"] = c.get("test", 0) + ins
            elif is_prose(f):
                c["prose"] = c.get("prose", 0) + ins
            elif is_html(f):
                c["html"] = c.get("html", 0) + ins
            elif is_generated(f):
                c["gen"] = c.get("gen", 0) + ins
            else:
                c["code"] = c.get("code", 0) + ins

    tot = defaultdict(int)
    types = defaultdict(int)
    hourly = defaultdict(int)
    repo_stats = defaultdict(lambda: defaultdict(int))
    days = set()
    human, auto, bulk = [], [], []
    for c in commits:
        if not c["human"]:
            auto.append(c)
            continue
        if c.get("ins", 0) >= BULK_THRESHOLD:
            bulk.append(c)
            continue
        human.append(c)
        for k in ("ins", "test", "prose", "html", "gen", "code"):
            tot[k] += c.get(k, 0)
        rs = repo_stats[c["repo"]]
        rs["commits"] += 1
        for k in ("code", "test", "prose", "html"):
            rs[k] += c.get(k, 0)
        m = re.match(r"^(\w+)", c["subj"])
        t = (m.group(1).lower() if m else "other")
        if t not in ("feat", "fix", "refactor", "test", "chore", "docs", "style",
                     "perf", "build", "ci", "infra", "wip"):
            t = "unprefixed"
        types[t] += 1
        dt = datetime.fromtimestamp(c["at"], tz)
        hourly[dt.hour] += 1
        days.add(dt.strftime("%Y-%m-%d"))

    # PRs: squash-merge stamp ` (#NNN)` on human subjects + classic merge-pr commits.
    pr_keys = set()
    for c in human:
        for num in re.findall(r"\(#(\d+)\)", c["subj"]):
            pr_keys.add((c["repo"], num))
    for repo in repos:
        out = sh(["git", "-C", repo, "log", "--all", "--merges", f"--since={since}",
                  "--pretty=format:%an|%s"])
        for line in out.splitlines():
            an, _, subj = line.partition("|")
            if an.strip().lower() not in human_authors:
                continue
            m = re.search(r"[Mm]erge pull request #(\d+)", subj)
            if m:
                pr_keys.add((os.path.basename(repo), m.group(1)))

    # sessions (45-min gap) on human epochs
    epochs = sorted(c["at"] for c in human)
    sessions = deep = med = micro = 0
    active_min = 0.0
    if epochs:
        sstart = prev = epochs[0]
        sessions = 1
        for t in epochs[1:]:
            if t - prev > 2700:
                d = (prev - sstart) / 60
                active_min += d
                if d >= 50:
                    deep += 1
                elif d >= 20:
                    med += 1
                else:
                    micro += 1
                sessions += 1
                sstart = t
            prev = t
        d = (prev - sstart) / 60
        active_min += d
        if d >= 50:
            deep += 1
        elif d >= 20:
            med += 1
        else:
            micro += 1

    # streak: your-authored days back from today (uses the resolved identity, not a hardcoded name)
    hdays = set()
    author_args = []
    for p in author_patterns:
        author_args += [f"--author={p}"]
    if author_args:
        for repo in repos:
            out = sh(["git", "-C", repo, "log", "--all", "--no-merges", "--since=90 days ago",
                      *author_args, "--pretty=format:%at"])
            for line in out.splitlines():
                line = line.strip()
                if line.isdigit():
                    hdays.add(datetime.fromtimestamp(int(line), tz).strftime("%Y-%m-%d"))
    streak = 0
    d = now.date()
    while d.isoformat() in hdays:
        streak += 1
        d -= timedelta(days=1)

    code = tot["code"]
    out = {
        "generated_at": now.isoformat(),
        "window_since": since_label,
        "identity": author_patterns,
        "roots": args.roots,
        "repos_scanned": len(repos),
        "commits_human": len(human),
        "commits_automated": len(auto),
        "bulk_excluded": [{"repo": c["repo"], "ins": c.get("ins", 0), "subj": c["subj"][:80]} for c in bulk],
        "repos_touched_human": len({c["repo"] for c in human}),
        "insertions_authored": tot["ins"],
        "code_loc": tot["code"], "test_loc": tot["test"], "prose_loc": tot["prose"],
        "html_loc": tot["html"], "generated_loc": tot["gen"],
        "test_ratio_vs_code": round(tot["test"] / code, 3) if code else None,
        "active_days": len(days),
        "sessions": sessions, "deep_sessions": deep, "medium_sessions": med, "micro_sessions": micro,
        "active_minutes": round(active_min),
        "avg_session_minutes": round(active_min / sessions) if sessions else 0,
        "code_loc_per_session_hour": round(code / (active_min / 60)) if active_min else 0,
        "types": dict(types),
        "hourly": {str(h): hourly.get(h, 0) for h in range(24)},
        "peak_hour": max(hourly, key=hourly.get) if hourly else None,
        "prs_merged": len(pr_keys),
        "per_repo": {r: dict(s) for r, s in sorted(repo_stats.items(), key=lambda x: -x[1]["commits"])},
        "focus_repo": max(repo_stats, key=lambda r: repo_stats[r]["commits"]) if repo_stats else None,
        "focus_pct": round(100 * max((s["commits"] for s in repo_stats.values()), default=0) / max(len(human), 1)),
        "automated_breakdown": {a: n for a, n in sorted(
            ((k, sum(1 for c in auto if c["an"] == k)) for k in {c["an"] for c in auto}),
            key=lambda x: -x[1])},
        "streak_days": streak,
    }
    json.dump(out, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
