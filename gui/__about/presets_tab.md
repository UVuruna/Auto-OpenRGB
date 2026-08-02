# Presets Tab

**Script:** [Presets Tab (script)](../presets_tab.py)

## Purpose
A PRESET is a RULE (owner terminology): a trigger grouping (hours /
weekdays / monthdays / months / daylight) whose slots reference [defined
colors](colors_tab.md). Several presets can exist; exactly ONE is active —
the resolver follows the active one.

## Layout
Left: the preset list (⭐ marks the active one) + Add/Remove/Set active.
Right: a trigger-type combo above a `QStackedWidget` holding one editor per
`PRESET_TYPES`, swapped by `_type_changed`. All five editors share the same
`load()`/`store()` contract driven by `PresetsTab.current_preset()`.

## Classes

### `_SlotRowsEditor`
Shared editor for **hours** and **monthdays** — a grid of (from, to, color)
rows with add/remove, bounded to the tab's `(lo, hi)` range (0–23 or 1–31).

### `_MappingEditor`
Shared editor for **weekdays** and **months** — one fixed color combo per
entry (all 7 days / all 12 months always present, laid out in up to 2
columns once there are more than 7 entries).

### `_DaylightEditor`
Day arc + night arc (`ColorSequence`, [Widgets](widgets.md)) + separate
MORNING/EVENING civil-twilight color combos + the
[Location Picker](location_picker.md) (timezone never typed).

### `PresetsTab`
Owns `raw["presets"]` and `raw["activePreset"]`; add/remove/rename/activate
a preset, and dispatch `load()`/`store()` to whichever editor matches the
current preset's type.

## Connections

### Uses
- [Settings](../../core/__about/settings.md) — `MONTH_KEYS`, `PRESET_TYPES`, `WEEKDAY_KEYS`
- [Location Picker](location_picker.md), [Widgets](widgets.md), [Theme](theme.md)

### Used by
- [Main Window](main_window.md)
