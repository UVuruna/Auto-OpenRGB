"""Group the defined colors by the hue centre each one is closest to.

Owner spec — nine centres: Red, Green, Blue, Cyan, Magenta, Yellow,
Orange, Azure (0,128,255) and Gray. Pure logic, no Qt: the Colors tab
uses it to lay the palette out group-by-group.

Rules (pseudocode):

```
saturation, hue = HSV of the colour
IF saturation < GRAY_MAX_SATURATION -> "Gray"      (white, black, greys)
ELSE -> the centre with the smallest CIRCULAR hue distance
        (on an exact tie the HIGHER hue centre wins)
```

The tie rule is not cosmetic: violets sit on the Blue/Magenta boundary
(#3C0078 is exactly 270 deg, #8000FF is 270.1), so "first centre wins"
would scatter two neighbouring purples into two different groups.

Brightness is deliberately ignored: a dark red and a light red belong to
the same channel. Only saturation separates the greys out.
"""

from colorsys import rgb_to_hsv

GRAY = "Gray"

# Below this saturation a colour reads as white/black/grey, not as a hue.
GRAY_MAX_SATURATION = 0.12

# (group name, hue centre in degrees). The order is the DISPLAY order
# (owner spec: R, G, B, C, M, Y, O, A, then Gray).
HUE_CENTERS: list[tuple[str, float]] = [
    ("Red", 0.0),
    ("Green", 120.0),
    ("Blue", 240.0),
    ("Cyan", 180.0),
    ("Magenta", 300.0),
    ("Yellow", 60.0),
    ("Orange", 30.0),
    ("Azure", 210.0),      # 0,128,255
]

GROUP_ORDER: list[str] = [name for name, _ in HUE_CENTERS] + [GRAY]


def hue_saturation(hex_color: str) -> tuple[float, float]:
    """(hue in degrees, saturation 0..1) of an RRGGBB string."""
    red = int(hex_color[0:2], 16) / 255.0
    green = int(hex_color[2:4], 16) / 255.0
    blue = int(hex_color[4:6], 16) / 255.0
    hue, saturation, _value = rgb_to_hsv(red, green, blue)
    return hue * 360.0, saturation


def group_of(hex_color: str) -> str:
    """The group name this colour belongs to."""
    hue, saturation = hue_saturation(hex_color)
    if saturation < GRAY_MAX_SATURATION:
        return GRAY
    best_name, best_distance, best_centre = GRAY, 360.0, -1.0
    for name, centre in HUE_CENTERS:
        distance = abs(hue - centre)
        distance = min(distance, 360.0 - distance)      # circular
        closer = distance < best_distance
        tie_to_higher_hue = distance == best_distance and centre > best_centre
        if closer or tie_to_higher_hue:
            best_name, best_distance, best_centre = name, distance, centre
    return best_name


def grouped(colors: dict[str, list[str]]) -> list[tuple[str, list[str]]]:
    """[(group name, [color names])] in display order; empty groups dropped.

    Color names keep their config order inside a group, so the palette never
    reshuffles behind the user's back.
    """
    buckets: dict[str, list[str]] = {name: [] for name in GROUP_ORDER}
    for name, values in colors.items():
        buckets[group_of(values[0])].append(name)
    return [(group, buckets[group]) for group in GROUP_ORDER if buckets[group]]
