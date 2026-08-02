# World Locations

**Script:** [Locations (script)](../locations.py) ·
**Flow:** [diagram](../__flow/locations.md)

## Purpose
The DOMY Watch 45k-city database repository (`data/world_locations.json`):
a cascading tree (`Continent -> Subregion -> Country -> [Admin ->] City`,
MIXED depth) plus folded-name search. Picking a city fills latitude,
longitude and the IANA timezone automatically — the user NEVER types a
timezone by hand (a typo there would silently break every daylight
computation).

Children are classified by SHAPE, never by depth: a node with a `latitude`
key is a city leaf, anything else is a navigable group — this is what lets
"Admin" be optional (some countries have it, most don't) without special
casing.

## Classes

### `LocationRepository`
Lazy-loads `data/world_locations.json` once (`load()`), then serves:
- `children(node_path)` — the direct children of a tree node (continents
  when `node_path=()`), each wrapped as a `LocationNode`
- `all_cities()` — a cached full walk of every city leaf, as
  `(folded name, display name, path)` — the live search index
- `record_at(path)` — the `CityRecord` for one full city path

### `CityRecord` / `LocationNode`
Frozen dataclasses: `CityRecord` is a resolved city (path, name, lat, lon,
timezone); `LocationNode` is one child at some tree level — a group when
`record is None`, a selectable city otherwise (`is_city` property).

## Connections

### Uses
- [Paths](paths.md) — `WORLD_DB` (bundle vs repo resolution)

### Used by
- [Location Picker](../../gui/__about/location_picker.md)
