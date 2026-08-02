# Hotkey Daemon

**Script:** [Hotkey Daemon (script)](../hotkey_daemon.py) ·
**Flow:** [diagram](../__flow/hotkey_daemon.md)

## Purpose
Resident process (Task Scheduler: `Ultra Vivid daemon`, at log on,
windowless) serving the two features that need a resident process:

1. **Global hotkeys** — one `RegisterHotKey` per binding in every
   non-hypershift shortcut set; a press applies the bound color/preset.
   Hypershift is Synapse's job via the stable slot files.
2. **Chroma keyboard** (optional) — holds the Razer Chroma session
   (sessions die without heartbeat) and colors the keyboard: following
   the schedule and/or on hotkey presses. See [Chroma](../core/__about/chroma.md).

Single-instance via a named mutex (`UltraVivid-Daemon`); a second launch
logs and exits immediately.

## Connections

### Uses
- [Core (folder)](../core/___core.md) — settings, keymap, apply, schedule, actions, chroma

### Used by
- Task Scheduler task `Ultra Vivid daemon` — see [Tasks](../core/__about/tasks.md)
- `main.py` — single-exe `--daemon` dispatch (Trivial tier, no separate
  doc — see [README](../README.md#file-structure))
