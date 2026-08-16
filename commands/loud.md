# /loud - Turn Claude Code hook sounds back ON

Re-enables the Mario / event sounds (removes the `~/.claude/SILENT` flag). The counterpart to `/quiet`.

## What to do

```bash
bash "$HOME/.claude/scripts/sound-toggle.sh" on
```

Then report ONLY the one-line result (`SOUNDS: ON`). No preamble.

## Related

- `/quiet`       -> toggle (or force off with `/quiet off`)
- `/quiet status`-> check current state
- Instant restore with no model turn: type `! rm ~/.claude/SILENT` directly in the prompt
