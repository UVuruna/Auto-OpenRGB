# Settings

**Script:** [Settings (script)](../settings.py)

## Purpose
Load `config.json` (schema v3) into typed, frozen dataclasses and validate
every field loudly. The resolver refuses to run on an old-schema or broken
config — no silent fallbacks (root Rule #1).

Terminology (owner spec): a COLOR is a named, defined color; a PRESET is
a RULE — a trigger grouping whose slots reference colors. Several presets
can exist; `activePreset` names the one the resolver follows.

## Schema v3 (summary)

```
version: 3
openrgb:         host, port, connectRetries, retrySeconds,
                 readyPollSeconds, readyStableChecks, readyTimeoutSeconds
                 (device-readiness wait — see Apply.wait_until_ready);
                 config.json ALSO carries "path" here, but it is read
                 directly by core.tasks (_openrgb_path), never through
                 this module — OpenRGBSettings has no `path` field
location:        name, latitude, longitude, timezone (picked via the
                 city picker — validated as a real IANA zone)
devices:         mode ("exclude"|"include"), names [substrings]
colors:          { name: [RRGGBB, ...] }         (defaults + custom)
presets:         [ { name, type, + the matching trigger section } ]
activePreset:    name of the preset the resolver follows
scheduleEnabled: global on/off
chroma:          enabled, followSchedule
update:          repo, check (auto-update — see Updates)
shortcuts:       enabled, sets: [ { name, selector, bindings {key: {color|preset}} } ]
```

## Validation rules (pseudocode)

```
IF version != 3            -> error (migrate first)
FOR EACH color value       -> must be RRGGBB hex
FOR EACH preset (rule):
    weekdays  -> all 7 days present
    months    -> all 12 months present
    monthdays -> 1 <= from <= to <= 31 per slot
    hours     -> 0 <= from,to <= 23 per slot
    daylight  -> day list non-empty AND location with a VALID IANA zone
EVERY referenced color     -> must exist in colors
activePreset               -> must name an existing preset (or be absent)
shortcut sets               -> unique names (case-insensitive), known keys
                               (core.keymap.VIRTUAL_KEYS), known colors/presets
```

## Connections

### Uses
- [Keymap](keymap.md) — validates shortcut binding keys against `VIRTUAL_KEYS`

### Used by
- [Schedule](schedule.md), [Apply](apply.md), [Actions](actions.md),
  [Resolver](../../__about/resolver.md), [Hotkey Daemon](../../__about/hotkey_daemon.md),
  [GUI (folder)](../../gui/___gui.md) — every tab edits the raw config dict;
  saving always goes back through `parse()`
