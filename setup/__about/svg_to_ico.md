# SVG to ICO

**Script:** [SVG to ICO (script)](../svg_to_ico.py)

## Purpose
Renders `assets/logo.svg` into a multi-resolution `assets/UltraVivid.ico`
(16/32/48/64/128/256 px) for the EXE icon, taskbar and Add/Remove Programs
entry. Small sizes (≤128 px) are supersampled (4x below 64 px, 2x below
128 px) via `QSvgRenderer` + `QPainter`, then downscaled with Pillow's
Lanczos filter for sharper edges than a direct small-size render would give.

## Connections

### Used by
- [Build](build.md) — called as a subprocess (`generate_ico()`), skipped
  gracefully if `assets/logo.svg` is missing
