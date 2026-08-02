# Shortcuts Tab

**Script:** [Shortcuts Tab (script)](../shortcuts_tab.py) ·
**Flow:** [diagram](../__flow/shortcuts_tab.md)

## Purpose
The owner's flow for building a shortcut set: name it → pick a selector →
pick ANY keys → bind each key to a color or a whole preset → "Create
shortcut files". A preset binding switches the active preset (still
running on the schedule afterward) and applies its current color; a color
binding just applies that color.

## Layout
Left: the set list + Add/Remove set. Right: selector combo + "Add key"
(a grouped menu from [Keymap](../../core/__about/keymap.md)'s `KEY_GROUPS`)
above a scrollable grid of `key label | binding combo | remove` rows, a
guide label, and the "Create shortcut files" button.

## Connections

### Uses
- [Settings](../../core/__about/settings.md) — `SHORTCUT_SELECTORS`
- [Keymap](../../core/__about/keymap.md) — `KEY_GROUPS`
- `config_io.py` (Trivial tier, no separate doc), [Widgets](widgets.md), [Theme](theme.md)
- [Resolver](../../__about/resolver.md) — imports `write_set_folder` directly
  to build the set's folder on "Create shortcut files"

### Used by
- [Main Window](main_window.md)
