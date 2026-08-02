# Keymap

**Script:** [Keymap (script)](../keymap.py)

## Purpose
Single source of truth for shortcut keys — the GUI shows the labels,
the daemon maps the same labels to Win32 virtual-key codes and
`RegisterHotKey` modifier flags. Shared so the two can never drift
(root Rule #5). Organized under section banners as a config-law file
(root CODE.md's THE CONFIG SECTION LAW — see `tests/test_config_sections.py`,
`CONFIG_FILES`).

| Table | Contents |
|-------|----------|
| `VIRTUAL_KEYS` | every supported key label → Win32 VK code (F-keys, digits, `-`/`=`, numpad, letters, punctuation) — a set may mix ANY of them |
| `KEY_GROUPS` | display grouping for the GUI key-picker menu (Function keys / Number row / Numpad / Letters) |
| `MODIFIER_FLAGS` | selector → RegisterHotKey flags (`hypershift` absent by design — Synapse territory, never registered via Win32) |
| `MOD_NOREPEAT` | RegisterHotKey flag suppressing key-repeat while held |

## Connections

### Used by
- [Shortcuts Tab](../../gui/__about/shortcuts_tab.md) (key labels for the picker menu),
  [Hotkey Daemon](../../__about/hotkey_daemon.md) (VK codes + modifier flags for `RegisterHotKey`),
  [Settings](settings.md) (validates shortcut binding keys against `VIRTUAL_KEYS`)
