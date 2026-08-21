# Resolver

**Script:** [Resolver (script)](../resolver.py) ·
**Flow:** [diagram](../__flow/resolver.md)

## Purpose
The single entry point that puts color on the RGB. Wired to three callers:
the **Task Scheduler** tasks (tick, forced wake), **Synapse slot files**
(`--shortcut`), and the GUI's **Apply now** / **Create shortcut files**
actions (which shell out to it, and import `write_set_folder` directly).

## Invocations

| Call | Effect |
|------|--------|
| *(no args, or `--tick`)* | Tick: resolve schedule → apply; skips when unchanged |
| `--dry-run` | Print the decision, touch nothing |
| `--color NAME` | Apply a named color directly |
| `--shortcut "SetName:key"` | Apply the binding that set binds to that key (stale slot = quiet no-op) |
| `--off` | All selected devices off |
| `--force` | Apply even when unchanged (used by the wake task and `--color`/`--shortcut`/`--off`, which always apply) |
| `--list-devices` | Show devices as the SDK server reports them |
| `--write-slots` | Regenerate `shortcuts/<SetName>/*.vbs` |

## Design
- **Change detection:** the tick stores its last decision in
  `logs/state.json`; a 10-minute tick therefore costs nothing while the
  preset is unchanged. `--force` bypasses the cache.
- **The cache is written ONLY on a verified apply** (2026-08-21):
  [Apply](../core/__about/apply.md) returns an `ApplyResult`, and
  `lastColor` is stored only when it is `trustworthy` — every selected
  device present AND reading its color back correctly. An unverified apply
  writes `{"unverifiedColor": ...}` with NO `lastColor` key, so the next
  tick can never mistake it for "already done". Writing the intended color
  regardless was the defect that left the RGB RAM uncolored for a whole
  session: a partial apply at log on cached success, and every tick after it
  answered `Unchanged since last tick — skipping apply`.
- **Power events bypass the cache:** the cached decision describes what we
  last WROTE, not what the hardware currently shows — sleep and power-off
  reset it (RGB RAM returns to its onboard effect). Log on and
  resume-from-sleep therefore run `--force` from their own scheduled task,
  never the cache-respecting tick — see [Tasks](../core/__about/tasks.md).
- **Logging:** rotating `logs/resolver.log`; top-level failures are logged
  and re-raised — never swallowed (root Rule #1).

## Connections

### Uses
- [Core (folder)](../core/___core.md) — settings, schedule, apply, actions, paths

### Used by
- Task Scheduler tasks `Ultra Vivid resolver` (tick) and `Ultra Vivid wake`
  (log on + resume, forced) — see [Tasks](../core/__about/tasks.md)
- [Shortcuts (folder)](../shortcuts/___shortcuts.md) — Synapse slot files
- [Shortcuts Tab](../gui/__about/shortcuts_tab.md) — imports `write_set_folder`
  directly to build a set's folder on "Create shortcut files"
- `main.py` — single-exe dispatch for the resolver CLI flags (Trivial tier,
  no separate doc — see [README](../README.md#file-structure))
