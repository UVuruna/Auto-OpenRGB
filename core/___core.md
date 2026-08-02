# core/

The Ultra Vivid engine: pure decision logic plus the OpenRGB SDK applier.
Everything here is GUI-free; [Resolver](../__about/resolver.md) is one of
three entry points that use it (Task Scheduler tick, Synapse slots) —
the [GUI (folder)](../gui/___gui.md) is just an editor for `config.json`.

## Files

| File | Tier | One line |
|------|------|----------|
| `__init__.py` | Trivial | empty — makes `core/` a package |
| `settings.py` | Standard | load + validate `config.json` (schema v3) — [about](__about/settings.md) |
| `solar.py` | Standard | five sun events of a local day via `astral` — [about](__about/solar.md) |
| `schedule.py` | Algorithmic | `(Settings, now) -> color name \| None` for all five preset types — [about](__about/schedule.md) · [flow](__flow/schedule.md) |
| `apply.py` | Algorithmic | connects to the OpenRGB SDK, waits for device readiness, applies colors — [about](__about/apply.md) · [flow](__flow/apply.md) |
| `actions.py` | Standard | shared shortcut-binding resolution (color vs preset switch) — [about](__about/actions.md) |
| `keymap.py` | Standard | key labels + Win32 VK codes + modifier flags — [about](__about/keymap.md) |
| `chroma.py` | Standard | Razer Chroma REST client (keyboard-only lighting) — [about](__about/chroma.md) |
| `locations.py` | Algorithmic | 45k-city tree repository + search folding — [about](__about/locations.md) · [flow](__flow/locations.md) |
| `paths.py` | Standard | single source of truth for repo-vs-frozen paths — [about](__about/paths.md) |
| `tasks.py` | Standard | registers the four scheduled tasks — [about](__about/tasks.md) |
| `updates.py` | Standard | GitHub-release update check — [about](__about/updates.md) |

## Connections

### Used by
- [Resolver](../__about/resolver.md) — CLI entry point (Task Scheduler tick, Synapse slots)
- [Hotkey Daemon](../__about/hotkey_daemon.md) — global hotkeys + Chroma session
- [GUI (folder)](../gui/___gui.md) — validation, live preview, device list, location picker

## Design Decisions
- **Compute, don't generate (root Rule #19):** no `.orp` profiles, no
  per-combination VBS files — one engine computes the color for any moment
  from rules in `config.json`.
- **Pure core:** `schedule.py`/`solar.py` do no I/O, so every schedule type
  is testable without hardware (see [Tests (folder)](../tests/___tests.md)).
