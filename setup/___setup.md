# setup/

Builds Ultra Vivid into a distributable, signed Windows installer
(`UltraVivid_Setup.exe`) — see monorepo root `CLAUDE.md` → Build & Release
System for the 7-step pipeline every desktop project follows; this folder's
[Build](__about/build.md) is that pipeline's REFERENCE implementation.

## Files

| File | Tier | One line |
|------|------|----------|
| `build.py` | Algorithmic | the build orchestrator (ICO → PyInstaller → sign → NSIS → sign → verify) — [about](__about/build.md) · [flow](__flow/build.md) |
| `create_cert.py` | Standard | one-time self-signed code-signing certificate — [about](__about/create_cert.md) |
| `svg_to_ico.py` | Standard | supersampled SVG → multi-resolution ICO — [about](__about/svg_to_ico.md) |
| `installer.nsi` | — (NSIS, not Python) | the NSIS installer script `build.py` invokes via `makensis` |

Generated, not tracked: `version_info.txt` (PyInstaller version resource,
written by `build.py` each run), `cert/` (the `.pfx` + `password.txt` —
gitignored, back up externally).

## Usage

```powershell
python setup/create_cert.py    # once, for code signing
python setup/build.py          # full pipeline -> dist/UltraVivid_Setup.exe
```

## Connections

### Used by
- The owner, manually — this is not imported by the running app

## Design Decisions
- **`build.py` changes only with extreme care** — it is the pattern other
  monorepo projects copy their own `build.py` from; a fix here is a fix the
  owner has to manually port everywhere else (see root `CLAUDE.md`'s Step 7
  rationale for why the fail-closed verify gate exists at all).
