# Open Questions — Ultra Vivid

Dilemmas surfaced during autonomous sessions that need an owner call.
Tracked and linked from [README.md](README.md) per root Rule #18/CLAUDE.md.

## 2026-08-02 — Docs migration to MD-First 2.0 + enforcement layer

Autonomous overnight session (root `MIGRATE-DOCS.md`). Nothing here blocked
completion — everything below is FYI / a judgment call made in the
session's favor, surfaced for the owner to overturn if wrong.

### Real drift found and FIXED (not just flagged — these are pure doc fixes, zero code change)

1. **`resolver.md` documented a `--preset NAME` flag that has never
   existed.** The actual flag is `--color NAME` (verified against
   `resolver.py`'s `argparse` block and its own module docstring). Fixed in
   the new `__about/resolver.md`.
2. **Two links were already broken before this session touched anything**
   (caught by the new `test_doc_links.py` on its first run, pre-migration):
   `core/paths.md -> locations.md` and `data/__index.md ->
   ../core/locations.md` — `core/locations.py` had NEVER had a doc at all.
   Fixed by writing `core/__about/locations.md` + `core/__flow/locations.md`
   fresh (Algorithmic tier: the tree-shape + search-folding algorithm
   genuinely earns a diagram).
3. **`core/keymap.md`'s "Used by" linked straight to a `.py` file**
   (`[Shortcuts Tab](../gui/shortcuts_tab.py)`) without the required
   "(script)" suffix — a Link Formatting Rule violation, not just a stale
   path. Fixed to link the tab's new `__about/shortcuts_tab.md`.
4. **`core/settings.md`'s schema summary listed `openrgb.path`** as if it
   were a field of the `Settings`/`OpenRGBSettings` dataclass. It is a real
   `config.json` key, but `core.settings.parse()` never reads it —
   `core/tasks.py`'s `_openrgb_path()` reads it directly from the raw JSON,
   bypassing `core.settings` entirely. The new `__about/settings.md` calls
   this out explicitly so a future reader does not go looking for a `path`
   attribute on `Settings.openrgb` that does not exist.

### Cross-cutting legacy doc DELETED, not folded (nothing survived)

`docs/plans/2026-02-22-gui-setup-wizard.md` and its companion
`-design.md` described a **tkinter** GUI (`gui/gui.py`, `profile_scanner.py`,
`config_writer.py`, `runner.py`, tabs "Setup / Raspored / Tastature /
Ekstra") for the project's earlier name ("Auto OpenRGB"). None of those
files, that framework, or that tab structure exist — the shipped `gui/` is
a complete PySide6 rewrite (`app.py`, `main_window.py`, `colors_tab.py`,
`presets_tab.py`, `devices_tab.py`, `shortcuts_tab.py`, …) with a different
config schema (v3, not the plan's `startTime`/`startHour` mix). Verified
line-by-line before deleting per Phase 2 Step 5 — nothing in either file
was still true, so nothing was folded anywhere; both were deleted along
with the now-empty `docs/` folder.

### Tier judgments made and why

| Judgment | Reasoning |
|----------|-----------|
| `gui/` tiered 5 of 12 files Algorithmic (`color_groups`, `devices_tab`, `location_picker`, `main_window`, `shortcuts_tab`) | Each has a genuine multi-step algorithm, background-thread/signal handoff, cascading multi-level state, or a real state machine that a diagram tells better than prose — the narrowed "would the diagram just restate the code?" test (root DOCS.md, 2026-08-01 decision) was applied per-file, not by GUI-file-default. `colors_tab.py` (302 lines) and `presets_tab.py` (335 lines) are the two largest GUI files but stayed Standard: both are repetitive CRUD/widget-wiring with no real branching a diagram would clarify. |
| `core/` tiered 3 of 12 files Algorithmic (`apply.py`'s `wait_until_ready` loop, `schedule.py`'s multi-branch + daylight-arc resolution, `locations.py`'s tree walk + search folding) | Same test; `settings.py` (316 lines, the largest core file) stayed Standard — it is validation bookkeeping (a schema table + per-field checks), not an algorithm a flowchart improves on. |
| `setup/build.py` is Algorithmic (the only setup/ file) | It is a literal multi-step pipeline (mirrors root CLAUDE.md's own build-pipeline Mermaid diagram) with a fail-closed verify gate worth diagramming on its own. |
| `CONFIG_FILES` in `test_config_sections.py` seeded with only `core/keymap.py` | It is the one file whose ENTIRE structure is module-level lookup tables (`VIRTUAL_KEYS`, `KEY_GROUPS`, `MODIFIER_FLAGS`) with no surrounding algorithm. `gui/theme.py` was considered and excluded: its tokens are individual scalar constants, not a dict/list table the guard's post-definition-patch check can meaningfully protect. `gui/color_groups.py` (`HUE_CENTERS`) and `core/settings.py` (`WEEKDAY_KEYS`/`MONTH_KEYS`/etc.) were excluded per root CODE.md's own scope note: "mostly algorithm with one small incidental table" stays out. |
| `assets/README.md` kept its `README.md` name rather than becoming `___assets.md` | `assets/` holds no source files — root DOCS.md's `___folder.md` convention is stated for "every CODE folder"; a pure resource bin follows the spirit (linked from the nav chain, content verified) without adopting the full tier/`__about`/`__flow` machinery a code folder needs. Reversible in one rename if the owner disagrees. |
| Root-level loose scripts (`resolver.py`, `hotkey_daemon.py`) get `__about/`/`__flow/` directly under the project root, `README.md` plays their `___folder.md` role | Matches the `3D Preview` project's precedent for its own root-level `main.py` (root DOCS.md's flat-project provision, applied per-loose-file rather than requiring the WHOLE project to be flat) — the alternative (inventing a synthetic root package folder) would be a structural change this docs-only session should not make. |

### Awaiting a decision

None. This session found no code bug, no ambiguous ownership, and no
guard-scope question it could not resolve with the reasoning above.
