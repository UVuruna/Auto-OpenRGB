# Shortcuts Tab — Flow

**About:** [description](../__about/shortcuts_tab.md)

## The owner's flow, end to end

```mermaid
%%{init: {'flowchart': {'subGraphTitleMargin': {'top': 0, 'bottom': 35}}}}%%
flowchart TB
    A["1. Add set (name it)"] --> B["2. Pick selector<br/>(shift/ctrl/alt/combos/hypershift —<br/>hypershift only if a Razer keyboard<br/>was detected)"]
    B --> C["3. Pick ANY keys<br/>(letters, number row, numpad, F-keys)"]
    C --> D["4. Bind each key to<br/>a COLOR or a whole PRESET"]
    D --> E["5. Click 'Create shortcut files'"]
    E --> F{save config valid?}
    F -- no --> G[warn, stop]
    F -- yes --> H[write_set_folder<br/>builds shortcuts/SetName/*.vbs]
    H --> I{selector == hypershift?}
    I -- yes --> J["6a. Open the folder + Razer Synapse;<br/>show the linking guide<br/>(one-time per key, links last forever)"]
    I -- no --> K["6b. Confirm: the daemon<br/>registers the hotkeys itself<br/>within a few seconds"]
```

`_selector_choices()` only OFFERS `hypershift` when
`hypershift_available` (detected once at [Main Window](../__about/main_window.md)
construction via `core.apply.detect_hypershift_keyboard`) — or when the
CURRENT selector already is `hypershift` (so an existing hypershift set
never silently loses its selector if the keyboard is briefly unreachable).
