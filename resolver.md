# Resolver

**Script:** [Resolver (script)](resolver.py)

## Purpose
The single entry point that puts color on the RGB. Wired to three callers:
the **Task Scheduler** task (tick), **Synapse slot files** (`--shortcut`),
and — in Phase 2 — the hotkey daemon.

## Invocations

| Call | Effect |
|------|--------|
| *(no args)* | Tick: resolve schedule → apply; skips when unchanged |
| `--dry-run` | Print the decision, touch nothing |
| `--preset NAME` | Apply a named color preset now |
| `--shortcut "SetName:key"` | Apply the preset that set binds to that key (stale slot = quiet no-op) |
| `--off` | All selected devices off |
| `--force` | Apply even when unchanged |
| `--list-devices` | Show devices as the SDK server reports them |
| `--write-slots` | Regenerate `shortcuts/slot-*.vbs` |

## Design
- **Change detection:** the tick stores its last decision in
  `logs/state.json`; a 10-minute tick therefore costs nothing while the
  preset is unchanged.
- **Power events bypass the cache:** the cached decision describes what we
  last WROTE, not what the hardware currently shows — sleep and power-off
  reset it (RGB RAM returns to its onboard effect). Log on and
  resume-from-sleep therefore run `--force` from their own scheduled task,
  never the cache-respecting tick — see [Tasks](core/tasks.md).
- **Logging:** rotating `logs/resolver.log`; top-level failures are logged
  and re-raised — never swallowed (Rule #1).

## Connections

### Uses
- [Core (folder)](core/__index.md) — settings, schedule, apply

### Used by
- Task Scheduler tasks `Ultra Vivid resolver` (tick) and `Ultra Vivid wake`
  (log on + resume, forced) — see [Tasks](core/tasks.md)
- [Shortcuts (folder)](shortcuts/__index.md) — Synapse slot files
