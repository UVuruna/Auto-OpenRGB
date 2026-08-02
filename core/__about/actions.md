# Actions

**Script:** [Actions (script)](../actions.py)

## Purpose
The shared action behind a shortcut binding — used by BOTH the
[Resolver](../../__about/resolver.md) (Synapse slot files) and the
[Hotkey Daemon](../../__about/hotkey_daemon.md), so a keypress behaves
identically whichever path fired it (root Rule #5, no duplicate logic).

## Binding kinds

A binding is a one-key dict:

| Binding | Effect on press |
|---------|-----------------|
| `{"color": name}` | apply that color; nothing else changes |
| `{"preset": name}` | SWITCH the active preset (persisted to `config.json`, so the scheduled tick keeps following it), then apply whatever that preset resolves to at this moment |

## Behavior (pseudocode)

```
resolve_binding(config_path, binding):
    IF binding is {"color": c} -> return c
    # preset binding:
    IF config.activePreset != binding.preset:
        config.activePreset = binding.preset
        write config.json               # the tick now follows it too
    forced = config with schedule_enabled forced True
    RETURN schedule.resolve(forced, now)   # press always shows the preset,
                                           # even while the global schedule
                                           # toggle is off
```

A preset with no slot for the current moment resolves to `None` (all-off) —
the same rule the scheduled tick obeys.

## Connections

### Uses
- [Settings](settings.md), [Schedule](schedule.md)

### Used by
- [Resolver](../../__about/resolver.md), [Hotkey Daemon](../../__about/hotkey_daemon.md)
