# data/

Bundled databases.

## Files

### `world_locations.json`
The 45k-city world database (Continent → Subregion → Country →
[Admin →] City with lat/lon/IANA timezone) — copied verbatim from the
DOMY Watch project (its 2026-07 curation). Read by
[World Locations](../core/__about/locations.md) for the GUI city picker
([Location Picker](../gui/__about/location_picker.md)).

## Connections

### Used by
- [Core (folder)](../core/___core.md) — `core/locations.py`
