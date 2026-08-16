#!/usr/bin/env bash
#
# Installs the /retro skill into Claude Code by symlinking this repo into
# ~/.claude/skills/retro. Because it's a symlink, `git pull` in this repo
# updates your live skill instantly — no re-copy needed.
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"
DEST="$SKILLS_DIR/retro"

mkdir -p "$SKILLS_DIR"

if [ -L "$DEST" ]; then
  rm "$DEST"
elif [ -e "$DEST" ]; then
  echo "A non-symlink already exists at $DEST — backing it up to ${DEST}.bak"
  rm -rf "${DEST}.bak"
  mv "$DEST" "${DEST}.bak"
fi

ln -s "$REPO_DIR" "$DEST"
chmod +x "$REPO_DIR/scan.py"

echo "Linked: $DEST -> $REPO_DIR"
echo
echo "Next:"
echo "  1. Restart Claude Code (or start a new session)."
echo "  2. In any repo, run: /retro"
echo
echo "To update later:  cd '$REPO_DIR' && git pull"
