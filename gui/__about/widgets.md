# Widgets

**Script:** [Widgets (script)](../widgets.py)

## Purpose
Small shared GUI building blocks (root Rule #5 — no duplicate widget code
across tabs): color combos with swatch icons, secondary/tool buttons, and
the ordered color-sequence editor.

## Contents
- `secondary()` / `tool_button()` — style/shape helpers for buttons.
- `color_combo()` / `refresh_color_combo()` / `combo_value()` — a
  `QComboBox` of the defined colors, each item carrying its swatch icon;
  `refresh_color_combo()` rebuilds the item list from the CURRENT colors
  dict (a combo built once at construction would never see colors created
  afterward).
- `binding_combo()` / `binding_from_combo()` — a combo listing every color
  THEN (after a separator) every preset (🕑 prefix); each item carries its
  `("color"|"preset", name)` as `UserRole` data, so the selected binding
  round-trips without re-parsing display text.
- `ColorSequence` — an ordered list of color combos (the daylight day/night
  arcs) with ➕ add, 🗑 remove and ⬆⬇ reorder per row; `values()` /
  `set_values()` round-trip a plain `list[str]`.

## Connections

### Uses
- [Theme](theme.md)

### Used by
- [Colors Tab](colors_tab.md), [Presets Tab](presets_tab.md),
  [Shortcuts Tab](shortcuts_tab.md)
