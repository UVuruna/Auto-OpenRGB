"""Colors are grouped by the hue centre they are closest to."""

import pytest

from gui.color_groups import GROUP_ORDER, group_of, grouped


@pytest.mark.parametrize("hex_color,expected", [
    ("FF0000", "Red"),
    ("00FF00", "Green"),
    ("0000FF", "Blue"),
    ("00FFFF", "Cyan"),
    ("FF00FF", "Magenta"),
    ("FFFF00", "Yellow"),
    ("FF8000", "Orange"),
    ("0080FF", "Azure"),        # the owner's 0,128,255
])
def test_pure_channels_land_on_their_own_centre(hex_color, expected):
    assert group_of(hex_color) == expected


@pytest.mark.parametrize("hex_color", ["FFFFFF", "000000", "646464", "1A1A1A"])
def test_unsaturated_colors_are_gray(hex_color):
    assert group_of(hex_color) == "Gray"


@pytest.mark.parametrize("hex_color,expected", [
    ("800000", "Red"),          # Brown — dark, still the red channel
    ("000080", "Blue"),         # Navy
    ("962C2C", "Red"),          # desaturated red still has enough saturation
    ("3B3BC8", "Blue"),
])
def test_brightness_does_not_change_the_channel(hex_color, expected):
    assert group_of(hex_color) == expected


def test_violets_on_the_blue_magenta_boundary_stay_together():
    # 3C0078 is EXACTLY 270 deg (a tie), 8000FF is 270.1 (no tie). Both must
    # land in the same group, or two neighbouring purples would be scattered.
    assert group_of("3C0078") == "Magenta"      # tie -> higher hue centre
    assert group_of("8000FF") == "Magenta"


def test_grouped_keeps_display_order_and_drops_empty_groups():
    colors = {
        "sun": ["FFFF00"],
        "sea": ["00FFFF"],
        "blood": ["FF0000"],
        "ash": ["808080"],
    }
    result = grouped(colors)
    names = [group for group, _ in result]
    assert names == ["Red", "Cyan", "Yellow", "Gray"]
    assert names == [g for g in GROUP_ORDER if g in names]
    assert dict(result)["Red"] == ["blood"]


def test_grouped_keeps_config_order_inside_a_group():
    colors = {"r1": ["FF0000"], "r2": ["EE0000"], "r3": ["CC1111"]}
    assert grouped(colors) == [("Red", ["r1", "r2", "r3"])]
