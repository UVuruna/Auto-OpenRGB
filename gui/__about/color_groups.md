# Color Groups

**Script:** [Color Groups (script)](../color_groups.py) ·
**Flow:** [diagram](../__flow/color_groups.md)

## Purpose
Pure logic (no Qt): puts a hex color in one of nine groups — Red, Green,
Blue, Cyan, Magenta, Yellow, Orange, Azure (0,128,255) and Gray — so the
[Colors Tab](colors_tab.md) can lay the palette out group-by-group (owner
spec, `UV/` inbox 2026-07-24). Near-zero saturation is Gray; everything else
goes to the nearest hue center by CIRCULAR distance, brightness ignored
(dark red and light red share a channel).

## Connections

### Used by
- [Colors Tab](colors_tab.md)
