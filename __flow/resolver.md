# Resolver — Flow

**About:** [description](../__about/resolver.md)

## CLI dispatch

```mermaid
%%{init: {'flowchart': {'subGraphTitleMargin': {'top': 0, 'bottom': 35}}}}%%
flowchart TB
    A[main: parse args] --> B{--write-slots?}
    B -- yes --> C[refresh every set's folder;<br/>remove folders of deleted sets] --> END
    B -- no --> D{--list-devices?}
    D -- yes --> E[connect; print each device] --> END
    D -- no --> F{--off?}
    F -- yes --> G[apply_color None; write_state None] --> END
    F -- no --> H{--color or --shortcut?}
    H -- yes --> I{--color?}
    I -- yes --> J[color = args.color<br/>must exist in cfg.colors]
    I -- no, --shortcut --> K[binding = lookup SetName:key<br/>None = stale slot, quiet return]
    K --> L[color = actions.resolve_binding<br/>may switch activePreset]
    J --> M[apply_color color; write_state color] --> END
    L --> M
    H -- no --> N[scheduled tick:<br/>color = schedule.resolve cfg, now]
    N --> O{--dry-run?}
    O -- yes --> P[print decision only] --> END
    O -- no --> Q{--force OR<br/>color != last state?}
    Q -- no --> R[log Unchanged - skip] --> END
    Q -- yes --> S[apply_color color; write_state color] --> END
```

## `write_set_folder` (slot file generation)

```
write_set_folder(cfg, shortcut_set):
    folder = SLOTS_DIR / safe_folder_name(set.name)
    expected = {}
    FOR EACH key, binding IN set.bindings:
        file_name = key-to-filename token (e.g. "-" -> "minus.vbs")
        command = slot_command_string("SetName:key")   # re-invokes THIS
                                                         # program with --shortcut
        write file_name:  WScript.Shell.Run(command, hidden)
        expected.add(file_name)
    FOR EACH stale .vbs IN folder not in expected:
        delete it                                        # key removed from set
    RETURN folder
```

Every set gets its folder — including hypershift sets, whose files the user
links in Synapse ONCE; the file paths never change, so a link is forever
(only `config.json` changes when the user remaps a color later).
