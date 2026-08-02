# Build

**Script:** [Build (script)](../build.py) ·
**Flow:** [diagram](../__flow/build.md)

## Purpose
The build orchestrator — turns the repo into a signed, distributable
`UltraVivid_Setup.exe`. **This is the monorepo's REFERENCE implementation**
of the Step-7 fail-closed verify gate (root `CLAUDE.md` → Build & Release
System) — other projects' `build.py` copy this pattern.

## Pipeline (`main()`)

1. `generate_version_info()` — writes `version_info.txt` (PyInstaller
   VERSIONINFO resource) from `version.py` + the monorepo root `company.json`
2. `generate_ico()` — calls [SVG to ICO](svg_to_ico.md), skipped gracefully
   if `assets/logo.svg` is missing
3. `build_pyinstaller()` — `--onedir --windowed`, bundles `assets/`,
   `data/world_locations.json`, `config.json` (default seed), `tzdata`
   (astral needs it); excludes `QtWebEngine*` (~500 MB, unused) and other
   dead weight; hidden-imports the single-exe dispatch targets that
   `main.py` reaches only through runtime `import` (`resolver`,
   `hotkey_daemon`, `gui.app`, `core.tasks`, `core.chroma`, `core.updates`,
   `version`) — PyInstaller's static scan cannot see those
4. `sign_exe()` — Authenticode-signs the inner exe (`sign_file`, reused for
   the installer too — see below)
5. `build_installer()` — `makensis` builds `dist/UltraVivid_Setup.exe`,
   then signs THAT file too (the file the user actually downloads and runs
   — signing only the inner exe would ship an unsigned installer)
6. `verify_build()` — **the fail-closed gate**: reads the built artifacts
   back and asserts the pipeline's promises actually hold, instead of
   trusting that every step ran silently

## Connections

### Uses
- [SVG to ICO](svg_to_ico.md); monorepo root `company.json`; `version.py`

### Used by
- The owner, manually: `python setup/build.py`
