# Schedule

**Script:** [Schedule (script)](../schedule.py) ·
**Flow:** [diagram](../__flow/schedule.md)

## Purpose
Pure resolution: given the loaded settings and the current moment, return
the color name the ACTIVE PRESET produces — or `None`, meaning ALL RGB
OFF (schedule disabled, no active preset, or uncovered time). No I/O, no
OpenRGB — [Apply](apply.md) consumes the result.

`tick_timezone(settings)` returns the configured location's `ZoneInfo` only
when the active preset is `daylight` (sun events are tz-aware); otherwise
`None` (naive local time is fine for hours/weekdays/monthdays/months).

## Connections

### Uses
- [Settings](settings.md), [Solar](solar.md)

### Used by
- [Resolver (flow)](../../__flow/resolver.md), [Hotkey Daemon (flow)](../../__flow/hotkey_daemon.md),
  [Actions](actions.md), [Main Window](../../gui/__about/main_window.md) (status line preview)
