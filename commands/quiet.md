# /quiet - Toggle Claude Code hook sounds (panic mute)

Fast on/off switch for the Mario / event sounds (`~/.claude/hooks/play-sound.sh`).
Flips the `~/.claude/SILENT` flag and kills any sound playing right now.

## What to do

Run the toggle script with `$ARGUMENTS` (default is toggle if no argument):

```bash
bash "$HOME/.claude/scripts/sound-toggle.sh" $ARGUMENTS
```

Then report ONLY the one-line result (e.g. `SOUNDS: OFF (silent)`). No preamble, no explanation - speed matters, this is often used mid-meeting.

## Arguments

- (none)  -> toggle: off if currently on, on if currently off
- `off`   -> force silent (also accepts `mute`)
- `on`    -> force sounds on (also accepts `unmute`)
- `status`-> report current state without changing it

## Faster than this command

A slash command still routes through the model (~2s). For an instant, no-model kill mid-panic, type this directly in the prompt - the `!` prefix runs it immediately:

```
! killall afplay; touch ~/.claude/SILENT
```

To restore after that: `! rm ~/.claude/SILENT`
