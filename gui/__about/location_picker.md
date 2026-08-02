# Location Picker

**Script:** [Location Picker (script)](../location_picker.py) ·
**Flow:** [diagram](../__flow/location_picker.md)

## Purpose
DOMY Watch's city system over the 45k-city database
([World Locations](../../core/__about/locations.md)). Live search (type 2+
letters, click a suggestion) plus cascading Continent / Subregion / Country
/ Region / City combos. Picking a city fills latitude, longitude and the
IANA timezone automatically — the user NEVER types a timezone (a typo there
would silently break every daylight computation). Latitude/longitude stay
fine-tunable afterward (e.g. a more precise address within the city).

Edits `raw["location"]` in place and emits `location_changed` on every
pick or fine-tune (consumed by [Presets Tab](presets_tab.md) to refresh the
daylight preview).

## Connections

### Uses
- [World Locations](../../core/__about/locations.md) — `LocationRepository`, `fold_name`
- [Theme](theme.md)

### Used by
- [Presets Tab](presets_tab.md) — the daylight editor's city picker
