# Theme

**Script:** [Theme (script)](../theme.py)

## Purpose
Monorepo `DESIGN.md` tokens and the application QSS. Dark-first,
one accent (vivid violet — the app is ABOUT color, so the chrome stays calm
and lets the preset swatches carry the vividness). All values are tokens
here, never literals in component code (root Rule #4).

## Sections
- **Color tokens** — surface ramp (`SURFACE_0..3`), border, text, the
  violet accent ramp, status colors (success/warning/error).
- **Geometry tokens** — corner radii, spacing scale, the Colors-tab tile/
  side-column dimensions, swatch size, font stack.
- **`app_qss()`** — the full stylesheet (tokens interpolated), covering
  every widget class the app uses: tabs, buttons (primary/secondary/
  update), inputs, lists/tables, checkboxes (with a custom SVG check
  glyph), scrollbars.
- **`swatch_bar()` / `swatch_icon()`** — small QPainter helpers that render
  a rounded color chip/bar for a given hex value (list item icons, the
  Colors-tab preview bar).

## Connections

### Uses
- [Paths](../../core/__about/paths.md) — `ASSETS_DIR` (the check-glyph SVG)

### Used by
- `app.py` (Trivial tier, no separate doc), every tab and [Widgets](widgets.md)
