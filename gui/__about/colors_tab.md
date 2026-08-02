# Colors Tab

**Script:** [Colors Tab (script)](../colors_tab.py)

## Purpose
The DEFINED COLORS of the app (owner terminology) — **ONE name = ONE hex**.
The palette lives in a single panel, split into hue groups
([Color Groups](color_groups.md)) stacked one below another; inside a group
the names flow across as many columns — and down as many rows — as they
need. The narrow side column shows the selected color's hex above its four
actions (New color / Rename / Edit / Remove). NOT presets — a preset is a
rule and lives in the [Presets Tab](presets_tab.md).

## Layout
- **Left panel** (scrollable): for each non-empty hue group, a header label
  then a `_ColorGrid` — a `QListWidget` in wrapping tile-flow mode that
  grows to fit exactly the rows its tiles need (`fit_height()`, recomputed
  on resize), so the surrounding `QScrollArea` does the scrolling, never the
  grid itself.
- **Right side column** (fixed width): the selected color's preview bar +
  hex value, then the four action buttons.

## Classes

### `_ColorGrid(QListWidget)`
One group's tiles. `fit_height()`: `rows = ceil(count / (width //
TILE_W))`, `height = rows * TILE_H + PAD` — recalculated in `resizeEvent`
so narrowing the window reflows the grid instead of scrolling it.

### `ColorsTab(QWidget)`
Owns the raw `colors` dict in place. `reload()` rebuilds every group from
`color_groups.grouped()`; `_add_color` / `_rename_color` / `_edit_color` /
`_remove_color` mutate the dict and emit `colors_changed` (consumed by
[Presets Tab](presets_tab.md) and [Shortcuts Tab](shortcuts_tab.md) to
refresh their color combos). `_rename_color` cascades the new name into
every preset slot and shortcut binding that referenced the old one;
`_remove_color` is blocked (with a message naming the users) while any
preset or shortcut still references the color.

## Connections

### Uses
- [Color Groups](color_groups.md), [Theme](theme.md), [Widgets](widgets.md)

### Used by
- [Main Window](main_window.md)
