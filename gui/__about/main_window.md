# Main Window

**Script:** [Main Window (script)](../main_window.py) ·
**Flow:** [diagram](../__flow/main_window.md)

## Purpose
Window shell: the four tabs ([Colors](colors_tab.md), [Presets](presets_tab.md),
[Devices](devices_tab.md), [Shortcuts](shortcuts_tab.md)), the Save / Apply
now / Install tasks… action bar, and a live status line (active preset +
what it resolves to right now, refreshed every `STATUS_REFRESH_MS` = 30s).
Also owns the self-update flow (root Rule #23).

The tabs edit the raw config dict in place; **Save** validates and writes
(an invalid edit never reaches disk — root Rule #1), **Apply now** saves
then runs the resolver detached with `--force`.

## Window sizing (owner spec)
Opens portrait: width = `min(OPEN_WIDTH=900, screen width)`, height =
`max(MIN_HEIGHT=540, screen height // HEIGHT_SCREEN_FRACTION=2)` — i.e.
**half the screen height**, never full height. The minimum size
(`MIN_WIDTH=720 × MIN_HEIGHT=540`) is the point where content would
actually start to clip on a 720p screen — not the opening size — so the
user can drag the window much narrower than it opens.

## Connections

### Uses
- [Apply](../../core/__about/apply.md), [Paths](../../core/__about/paths.md),
  [Schedule](../../core/__about/schedule.md), [Settings](../../core/__about/settings.md),
  [Updates](../../core/__about/updates.md), `config_io.py` (Trivial tier,
  no separate doc), [Theme](theme.md)
- [Colors Tab](colors_tab.md), [Devices Tab](devices_tab.md),
  [Presets Tab](presets_tab.md), [Shortcuts Tab](shortcuts_tab.md)

### Used by
- `app.py` (Trivial tier, no separate doc — the whole entry point)
