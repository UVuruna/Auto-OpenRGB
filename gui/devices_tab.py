"""Devices tab — which OpenRGB devices the schedule paints.

Lists devices live from the SDK server with checkboxes; the check state is
translated to the config's include/exclude filter.

The SDK query runs on a BACKGROUND thread and reports back through a Qt
signal (queued onto the GUI thread), so opening the window never blocks on
OpenRGB, and the last known list stays on screen while a refresh is in
flight — the page is never blank and never makes the user wait.
"""

import dataclasses
import threading

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox, QLabel, QListWidget, QListWidgetItem, QPushButton,
    QVBoxLayout, QWidget,
)

from core import apply as rgb
from core import settings as settings_mod
from core.settings import ConfigError
from gui import theme


class DevicesTab(QWidget):
    # (device names, error text). Emitted from the loader thread; Qt delivers
    # it on the GUI thread, which is the only place widgets are touched.
    _loaded = Signal(list, str)

    def __init__(self, raw: dict):
        super().__init__()
        self.raw = raw
        self._loading = False
        self._loaded.connect(self._apply_loaded)

        self.status = QLabel()
        self.status.setProperty("hint", True)
        self.device_list = QListWidget()
        self.device_list.itemChanged.connect(self._store)

        self.refresh_btn = QPushButton("🔄 Refresh from OpenRGB")
        self.refresh_btn.setProperty("secondary", True)
        self.refresh_btn.clicked.connect(self.reload)

        hint = QLabel("Checked devices follow the schedule; unchecked are left "
                      "alone (e.g. a keyboard managed by Razer Synapse).")
        hint.setProperty("hint", True)

        chroma_cfg = self.raw.setdefault(
            "chroma", {"enabled": False, "followSchedule": True})
        self.chroma_enabled = QCheckBox(
            "Color the Razer keyboard via Chroma (Synapse key bindings stay untouched)")
        self.chroma_enabled.setChecked(bool(chroma_cfg.get("enabled", False)))
        self.chroma_follow = QCheckBox(
            "…and let the keyboard follow the schedule (same color as the other devices)")
        self.chroma_follow.setChecked(bool(chroma_cfg.get("followSchedule", True)))
        self.chroma_follow.setEnabled(self.chroma_enabled.isChecked())
        self.chroma_enabled.toggled.connect(self._chroma_toggled)
        self.chroma_follow.toggled.connect(
            lambda on: self.raw["chroma"].__setitem__("followSchedule", on))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(theme.SPACE_M, theme.SPACE_M, theme.SPACE_M, theme.SPACE_M)
        layout.setSpacing(theme.SPACE_S)
        layout.addWidget(QLabel("OpenRGB devices"))
        layout.addWidget(self.device_list, 1)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.status)
        layout.addWidget(hint)
        layout.addSpacing(theme.SPACE_S)
        layout.addWidget(QLabel("Razer Chroma module"))
        layout.addWidget(self.chroma_enabled)
        layout.addWidget(self.chroma_follow)

        self.reload()

    def _selected_by_filter(self, name: str) -> bool:
        f = self.raw["devices"]
        matched = any(n.lower() in name.lower() for n in f.get("names", []))
        return not matched if f.get("mode") == "exclude" else matched

    # -- background load ---------------------------------------------------

    def reload(self) -> None:
        """Start a background read of the device list (never blocks the GUI)."""
        if self._loading:
            return
        try:
            cfg = settings_mod.parse(self.raw)
        except ConfigError as e:
            self.status.setText(f"Config is invalid, fix it first — {e}")
            return
        # One attempt only: this is a live probe, not the resolver's startup wait.
        probe = dataclasses.replace(
            cfg, openrgb=dataclasses.replace(cfg.openrgb, connect_retries=1))
        self._loading = True
        self.refresh_btn.setEnabled(False)
        self.status.setText("Reading devices from OpenRGB…")
        threading.Thread(target=self._load, args=(probe,), daemon=True).start()

    def _load(self, probe) -> None:
        """Loader thread: talks to the SDK, touches NO widgets, emits the result."""
        try:
            client = rgb.connect(probe)
            try:
                names = [d.name for d in client.devices]
            finally:
                client.disconnect()
            self._loaded.emit(names, "")
        except Exception as e:                      # noqa: BLE001 - reported in the UI
            self._loaded.emit([], str(e))

    def _apply_loaded(self, names: list, error: str) -> None:
        self._loading = False
        self.refresh_btn.setEnabled(True)
        if error:
            # Keep the list that is already on screen — a failed probe must
            # never blank the page (documented fallback, Rule #1: it is shown).
            self.status.setText(
                f"OpenRGB server unreachable ({error}). Stored filter: "
                f"{self.raw['devices']['mode']} {self.raw['devices']['names']}")
            return
        self.device_list.blockSignals(True)
        self.device_list.clear()
        for name in names:
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked if self._selected_by_filter(name)
                else Qt.CheckState.Unchecked)
            self.device_list.addItem(item)
        self.device_list.blockSignals(False)
        self.status.setText(f"Connected — {len(names)} devices.")

    # -- config writes -----------------------------------------------------

    def _chroma_toggled(self, on: bool) -> None:
        self.raw["chroma"]["enabled"] = on
        self.chroma_follow.setEnabled(on)

    def _store(self, _item) -> None:
        """Translate check states into an exclude list (unchecked names)."""
        unchecked = [
            self.device_list.item(i).text()
            for i in range(self.device_list.count())
            if self.device_list.item(i).checkState() != Qt.CheckState.Checked
        ]
        self.raw["devices"] = {"mode": "exclude", "names": unchecked}
