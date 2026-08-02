# gui/

The Ultra Vivid control panel — a PySide6 editor for `config.json`.
Dark-first theme per the monorepo `DESIGN.md`; opens portrait (W:H = 1:2,
min width 720, clamped to the screen). The engine itself never needs the
GUI (it reads the same config) — see [Core (folder)](../core/___core.md).

## Files

| File | Tier | One line |
|------|------|----------|
| `__init__.py` | Trivial | empty — makes `gui/` a package |
| `app.py` | Trivial | entry point, `python -m gui.app` — builds `QApplication`, applies theme, shows `MainWindow` |
| `color_groups.py` | Algorithmic | nearest-hue-center classification — [about](__about/color_groups.md) · [flow](__flow/color_groups.md) |
| `colors_tab.py` | Standard | the DEFINED COLORS panel — [about](__about/colors_tab.md) |
| `config_io.py` | Trivial | load/save `config.json` for the GUI — validates through `core.settings.parse` before writing |
| `devices_tab.py` | Algorithmic | OpenRGB device checklist, background-thread load — [about](__about/devices_tab.md) · [flow](__flow/devices_tab.md) |
| `location_picker.py` | Algorithmic | cascading city picker + live search — [about](__about/location_picker.md) · [flow](__flow/location_picker.md) |
| `main_window.py` | Algorithmic | window shell, action bar, self-update state machine — [about](__about/main_window.md) · [flow](__flow/main_window.md) |
| `presets_tab.py` | Standard | preset (rule) list + per-type editors — [about](__about/presets_tab.md) |
| `shortcuts_tab.py` | Algorithmic | shortcut-set builder, hypershift guide — [about](__about/shortcuts_tab.md) · [flow](__flow/shortcuts_tab.md) |
| `theme.py` | Standard | DESIGN.md tokens + application QSS — [about](__about/theme.md) |
| `widgets.py` | Standard | shared small widgets — [about](__about/widgets.md) |

## Connections

### Uses
- [Core (folder)](../core/___core.md) — validation, schedule preview, SDK
  device list, locations, keymap, updates
- [Resolver](../__about/resolver.md) — `write_set_folder` (Shortcuts Tab)

### Used by
- The owner. The scheduled tasks and daemon run without the GUI.

## Design Decisions
- **Tier split leans Algorithmic** for tabs with genuine background-thread
  handoff, cascading multi-level state, or a real state machine
  (`devices_tab`, `location_picker`, `main_window`, `shortcuts_tab`,
  `color_groups`); tabs that are mostly repetitive CRUD widget wiring stay
  Standard (`colors_tab`, `presets_tab`) even though they are large —
  see root DOCS.md's "would the diagram just restate the code?" test.
