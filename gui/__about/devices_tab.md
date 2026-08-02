# Devices Tab

**Script:** [Devices Tab (script)](../devices_tab.py) ·
**Flow:** [diagram](../__flow/devices_tab.md)

## Purpose
Which OpenRGB devices the schedule paints. Lists devices live from the SDK
server with checkboxes; the check state is translated to the config's
include/exclude filter (unchecked names become an `exclude` list — the tab
always writes `{"mode": "exclude", "names": [...]}`, regardless of the
config's previous mode). Also hosts the Razer Chroma module toggle
(`chroma.enabled` / `chroma.followSchedule`).

The SDK query runs on a BACKGROUND thread and reports back through a Qt
signal (queued onto the GUI thread), so opening the window never blocks on
OpenRGB, and the last known list stays on screen while a refresh is in
flight — the page is never blank and never makes the user wait.

The Chroma section is Razer-only: it appears once a Razer keyboard actually
shows up in the device list, or when the module is already enabled (so the
setting is never unreachable even if the keyboard briefly does not respond).
The "is this a Razer keyboard" rule lives once in
[Apply](../../core/__about/apply.md) (`is_razer_keyboard`).

## Connections

### Uses
- [Apply](../../core/__about/apply.md) — `connect()`, `is_razer_keyboard()`
- [Settings](../../core/__about/settings.md) — `parse()`, `ConfigError`
- [Theme](theme.md)

### Used by
- [Main Window](main_window.md)
