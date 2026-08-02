# tests/

Golden and regression tests for the engine's semantics. Pure `pytest`, no
Qt, no OpenRGB hardware — [Schedule](../core/__about/schedule.md) and
[Solar](../core/__about/solar.md) are testable offline by design.

## Files

- `test_color_groups.py` — [Color Groups](../gui/__about/color_groups.md)'s
  hue-classification rules: pure channels, gray threshold, brightness
  independence, the violet tie-break, group/display ordering.
- `test_imports.py` — imports EVERY project module, including ones reached
  only through lazy/dispatch imports (`core.tasks` via `--install-tasks`).
  Regression pin: a `core/tasks.py` `SyntaxError` once passed PyInstaller
  silently and broke the installed exe's `--install-tasks` — this test
  exists so an import error fails the suite, never only a frozen build.
- `test_schedule.py` — golden tests for [Schedule](../core/__about/schedule.md)
  resolution across all five preset types, including the daylight arcs
  against real Belgrade sun times (verified against `astral`) and the
  config-validation guard against an empty/invalid daylight timezone.
- `test_tasks.py` — [Tasks](../core/__about/tasks.md)' generated PowerShell
  shape: the wake task is separate and forces the apply, power-event
  triggers belong to the wake task (not the cache-respecting resolver
  tick), and the periodic tick itself never forces.

## Guard tests

The enforcement guards (`test_structure_law.py`, `test_config_sections.py`,
`test_docs_coverage.py`, `test_doc_links.py`, `run_guards.py`) live in this
same folder per root `CODE.md`'s Enforcement spec (the hook contract and
speed budget demand a root `tests/`, even though this project has no
separate `support/tests/`) — see monorepo root `CLAUDE.md` → The Laws.

## Connections

### Uses
- [Core (folder)](../core/___core.md), [GUI (folder)](../gui/___gui.md)

## Design Decisions
- **tests/ is a dedicated docs tier** (root `DOCS.md` → Tiers): individual
  test modules get NO `__about/`/`__flow/` docs of their own — this folder
  doc is the only one, by design.
