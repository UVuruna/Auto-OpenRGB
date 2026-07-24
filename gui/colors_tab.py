"""Colors tab — the DEFINED COLORS of the app (owner terminology).

ONE name = ONE hex color. The palette lives in a single panel, split into
hue groups (`color_groups.py`) stacked one below another; inside a group the
names flow across as many columns — and down as many rows — as they need.
The narrow side column shows the selected color's hex above its four actions
(New color / Rename / Edit / Remove).

A default palette ships with the config; the user can add fully custom
colors. Presets (rules), shortcuts and Chroma all reference these by
name. NOT presets — a preset is a rule and lives in the Presets tab.
"""

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import (
    QColorDialog, QHBoxLayout, QInputDialog, QLabel, QListView, QListWidget,
    QListWidgetItem, QMessageBox, QPushButton, QScrollArea, QVBoxLayout,
    QWidget,
)

from gui import color_groups, theme
from gui.widgets import ADD, EDIT, REMOVE, secondary

NO_SELECTION = "—"


class _ColorGrid(QListWidget):
    """A group's color tiles: wraps into columns/rows and grows to fit them
    all, so the surrounding scroll area does the scrolling, not each grid."""

    def __init__(self):
        super().__init__()
        self.setFlow(QListView.Flow.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setGridSize(QSize(theme.COLOR_TILE_W, theme.COLOR_TILE_H))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def fit_height(self) -> None:
        """Height = exactly the rows the tiles need at the current width."""
        width = max(self.viewport().width(), theme.COLOR_TILE_W)
        per_row = max(1, width // theme.COLOR_TILE_W)
        rows = max(1, (self.count() + per_row - 1) // per_row)
        height = rows * theme.COLOR_TILE_H + theme.COLOR_GRID_PAD
        if self.height() != height:
            self.setFixedHeight(height)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.fit_height()


class ColorsTab(QWidget):
    colors_changed = Signal()

    def __init__(self, raw: dict):
        super().__init__()
        self.raw = raw
        self._selected: str | None = None
        self._grids: list[_ColorGrid] = []

        # -- the one panel: hue groups stacked, each a wrapping tile grid ----
        self._groups_box = QWidget()
        self._groups_layout = QVBoxLayout(self._groups_box)
        self._groups_layout.setContentsMargins(0, 0, 0, 0)
        self._groups_layout.setSpacing(theme.SPACE_S)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._groups_box)

        # -- side column: the hex of the selected color, then its actions ----
        self.preview_bar = QLabel()
        self.preview_bar.setFixedSize(theme.COLOR_SIDE_W, theme.COLOR_PREVIEW_H)
        self.preview_hex = QLabel(NO_SELECTION)
        self.preview_hex.setProperty("hexvalue", True)
        self.preview_hex.setAlignment(Qt.AlignmentFlag.AlignCenter)

        new_btn = QPushButton(f"{ADD} New color")
        new_btn.clicked.connect(self._add_color)
        rename_btn = secondary(QPushButton("✏️ Rename"))
        rename_btn.clicked.connect(self._rename_color)
        edit_btn = secondary(QPushButton(f"{EDIT} Edit"))
        edit_btn.clicked.connect(self._edit_color)
        remove_btn = secondary(QPushButton(f"{REMOVE} Remove"))
        remove_btn.clicked.connect(self._remove_color)

        side = QVBoxLayout()
        side.setSpacing(theme.SPACE_S)
        side.addWidget(QLabel("Selected color"))
        side.addWidget(self.preview_bar)
        side.addWidget(self.preview_hex)
        side.addSpacing(theme.SPACE_S)
        for button in (new_btn, rename_btn, edit_btn, remove_btn):
            button.setFixedWidth(theme.COLOR_SIDE_W)
            side.addWidget(button)
        side.addStretch(1)

        panel = QVBoxLayout()
        panel.addWidget(QLabel("Defined colors"))
        panel.addWidget(scroll, 1)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(theme.SPACE_M, theme.SPACE_M,
                                  theme.SPACE_M, theme.SPACE_M)
        layout.setSpacing(theme.SPACE_M)
        layout.addLayout(panel, 1)
        layout.addLayout(side)

        self.reload()

    # -- data helpers ------------------------------------------------------

    def _colors(self) -> dict:
        return self.raw["colors"]

    def _current_name(self) -> str | None:
        if self._selected in self._colors():
            return self._selected
        return None

    def _value(self, name: str) -> str:
        """The color's single hex. Configs store a list (the engine can
        round-robin several values across devices); one name = one color
        here, so the GUI reads and writes the first entry."""
        return self._colors()[name][0]

    def _set_value(self, name: str, hex_value: str) -> None:
        self._colors()[name] = [hex_value]

    # -- building the grouped palette --------------------------------------

    def reload(self) -> None:
        while self._groups_layout.count():
            item = self._groups_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()
        self._grids = []

        for group, names in color_groups.grouped(self._colors()):
            header = QLabel(group.upper())
            header.setProperty("grouphdr", True)
            self._groups_layout.addWidget(header)

            grid = _ColorGrid()
            for name in names:
                grid.addItem(
                    QListWidgetItem(theme.swatch_icon(self._value(name)), name))
            grid.itemSelectionChanged.connect(
                lambda g=grid: self._grid_selected(g))
            grid.itemDoubleClicked.connect(lambda *_: self._edit_color())
            grid.fit_height()
            self._groups_layout.addWidget(grid)
            self._grids.append(grid)

        self._groups_layout.addStretch(1)
        self._select(self._selected)

    def _grid_selected(self, grid: _ColorGrid) -> None:
        items = grid.selectedItems()
        if not items:
            return
        for other in self._grids:
            if other is not grid:
                other.clearSelection()
        self._selected = items[0].text()
        self._load_selected()

    def _select(self, name: str | None) -> None:
        """Select `name` wherever it now lives, else the first color."""
        target = name if name in self._colors() else None
        for grid in self._grids:
            for row in range(grid.count()):
                item = grid.item(row)
                if target is None:
                    grid.setCurrentItem(item)   # first color of the first grid
                    return
                if item.text() == target:
                    grid.setCurrentItem(item)
                    return
        self._selected = None
        self._load_selected()

    def _load_selected(self) -> None:
        name = self._current_name()
        if name is None:
            self.preview_bar.setPixmap(QPixmap())
            self.preview_hex.setText(NO_SELECTION)
            return
        value = self._value(name)
        self.preview_bar.setPixmap(
            theme.swatch_bar(value, theme.COLOR_SIDE_W, theme.COLOR_PREVIEW_H))
        self.preview_hex.setText(f"#{value.upper()}")

    # -- color actions -----------------------------------------------------

    def _add_color(self) -> None:
        name, ok = QInputDialog.getText(self, "New color", "Color name:")
        name = name.strip()
        if not ok or not name:
            return
        if name in self._colors():
            QMessageBox.warning(self, "Ultra Vivid", f"Color {name!r} already exists.")
            return
        picked = QColorDialog.getColor(QColor(theme.ACCENT), self, f"Value for {name}")
        if not picked.isValid():
            return
        self._set_value(name, picked.name()[1:].upper())
        self._selected = name
        self.reload()
        self.colors_changed.emit()

    def _rename_color(self) -> None:
        old = self._current_name()
        if old is None:
            return
        new, ok = QInputDialog.getText(self, "Rename color", "New name:", text=old)
        new = new.strip()
        if not ok or not new or new == old:
            return
        if new in self._colors():
            QMessageBox.warning(self, "Ultra Vivid", f"Color {new!r} already exists.")
            return
        colors = self._colors()
        colors[new] = colors.pop(old)
        self._rename_references(old, new)
        self._selected = new
        self.reload()
        self.colors_changed.emit()

    def _edit_color(self) -> None:
        """Pick a new hex for the selected color (it may change group)."""
        name = self._current_name()
        if name is None:
            return
        picked = QColorDialog.getColor(
            QColor(f"#{self._value(name)}"), self, f"Value for {name}")
        if not picked.isValid():
            return
        self._set_value(name, picked.name()[1:].upper())
        self._selected = name
        self.reload()
        self.colors_changed.emit()

    def _remove_color(self) -> None:
        name = self._current_name()
        if name is None:
            return
        used = self._where_used(name)
        if used:
            QMessageBox.warning(
                self, "Ultra Vivid",
                f"Color {name!r} is still used by: {', '.join(used)}.\n"
                "Re-map those first.")
            return
        del self._colors()[name]
        self._selected = None
        self.reload()
        self.colors_changed.emit()

    def _where_used(self, name: str) -> list[str]:
        used = []
        for preset in self.raw.get("presets", []):
            hits = (
                any(s.get("color") == name for s in preset.get("hours", []))
                or name in preset.get("weekdays", {}).values()
                or any(s.get("color") == name for s in preset.get("monthdays", []))
                or name in preset.get("months", {}).values()
                or name in preset.get("daylight", {}).get("day", [])
                or name == preset.get("daylight", {}).get("twilightMorning")
                or name == preset.get("daylight", {}).get("twilightEvening")
                or name in preset.get("daylight", {}).get("night", [])
            )
            if hits:
                used.append(f"preset {preset['name']!r}")
        for st in self.raw.get("shortcuts", {}).get("sets", []):
            if any(b.get("color") == name for b in st.get("bindings", {}).values()):
                used.append(f"shortcut set {st['name']!r}")
        return used

    def _rename_references(self, old: str, new: str) -> None:
        for preset in self.raw.get("presets", []):
            for slot in preset.get("hours", []) + preset.get("monthdays", []):
                if slot.get("color") == old:
                    slot["color"] = new
            for section in (preset.get("weekdays", {}), preset.get("months", {})):
                for k, v in section.items():
                    if v == old:
                        section[k] = new
            d = preset.get("daylight", {})
            if d:
                d["day"] = [new if c == old else c for c in d.get("day", [])]
                for tk in ("twilightMorning", "twilightEvening"):
                    if d.get(tk) == old:
                        d[tk] = new
                d["night"] = [new if c == old else c for c in d.get("night", [])]
        for st in self.raw.get("shortcuts", {}).get("sets", []):
            for binding in st.get("bindings", {}).values():
                if binding.get("color") == old:
                    binding["color"] = new
