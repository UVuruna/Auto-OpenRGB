"""The closed-loop apply — readback, rescan, and an honest cache.

REGRESSION (2026-08-21, "OpenRGB never loaded the RAM, so no shortcut could
color it"): the resolver wrote state.json as if the apply had succeeded even
when a selected device was missing from the OpenRGB device list. Every later
10-min tick then answered "Unchanged since last tick — skipping apply", so the
missing device kept its old color until the next reboot. Two amplifiers made
it permanent: the learned device count was lowered by that single bad boot (so
the next boot never waited), and nothing ever asked OpenRGB to RE-DETECT — and
a device the server missed never appears on its own.

Run: python -m pytest tests/test_apply_verify.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core import apply as rgb
from core import paths


class FakeColor:
    def __init__(self, red, green, blue):
        self.red, self.green, self.blue = red, green, blue


class FakeMode:
    def __init__(self, name):
        self.name = name


class FakeDevice:
    """A device whose readback can be made to lie, the way real RGB RAM does
    when it keeps running its onboard effect after a Direct write."""

    def __init__(self, device_id, name, modes=("Direct", "Static"),
                 obedient=True):
        self.id = device_id
        self.name = name
        self.modes = [FakeMode(m) for m in modes]
        self.active_mode = 0
        self.colors = [FakeColor(0, 0, 0)]
        self.obedient = obedient
        self.writes = 0

    def set_mode(self, mode):
        if self.obedient:
            self.active_mode = self.modes.index(mode)

    def set_color(self, color):
        self.writes += 1
        if self.obedient:
            self.colors = [FakeColor(color.red, color.green, color.blue)]


class FakeClient:
    def __init__(self, devices):
        self.devices = devices
        self.updates = 0

    def update(self):
        self.updates += 1


# ── ApplyResult: what may be cached ────────────────────────────────────────

def test_only_a_complete_and_verified_apply_is_trustworthy():
    assert rgb.ApplyResult(complete=True).trustworthy
    assert not rgb.ApplyResult(complete=False).trustworthy
    assert not rgb.ApplyResult(complete=True, unverified=["RAM"]).trustworthy


def test_reason_names_what_went_wrong():
    reason = rgb.ApplyResult(complete=False, unverified=["RAM"]).reason()
    assert "incomplete" in reason and "RAM" in reason


# ── verify_applied: is OUR color the one showing? ──────────────────────────

def test_verify_passes_when_the_hardware_shows_what_we_sent():
    device = FakeDevice(0, "HyperX Predator RGB")
    device.colors = [FakeColor(255, 32, 32)]
    client = FakeClient([device])
    assert rgb.verify_applied(client, {0: FakeColor(255, 32, 32)}) == []
    assert client.updates == 1          # the readback is a real re-read


def test_verify_catches_a_device_still_showing_the_old_color():
    device = FakeDevice(0, "HyperX Predator RGB")
    device.colors = [FakeColor(0, 255, 0)]
    assert rgb.verify_applied(FakeClient([device]), {0: FakeColor(255, 32, 32)}) == [0]


def test_verify_catches_a_device_left_on_an_effect_mode():
    device = FakeDevice(0, "HyperX Predator RGB", modes=("Direct", "Rainbow"))
    device.active_mode = 1              # onboard effect still running
    device.colors = [FakeColor(255, 32, 32)]
    assert rgb.verify_applied(FakeClient([device]), {0: FakeColor(255, 32, 32)}) == [0]


def test_verify_ignores_devices_we_did_not_target():
    ours, theirs = FakeDevice(0, "ASRock"), FakeDevice(1, "Razer Blackwidow V4")
    ours.colors = [FakeColor(255, 32, 32)]
    assert rgb.verify_applied(FakeClient([ours, theirs]),
                              {0: FakeColor(255, 32, 32)}) == []


# ── the learned device count must survive one bad boot ─────────────────────

def _state(tmp_path, monkeypatch, record=None):
    path = tmp_path / "devices.json"
    if record is not None:
        path.write_text(json.dumps(record), encoding="utf-8")
    monkeypatch.setattr(paths, "DEVICE_STATE_PATH", path)
    return path


def test_a_new_device_raises_the_learned_count_immediately(tmp_path, monkeypatch):
    path = _state(tmp_path, monkeypatch, {"count": 3})
    rgb._remember_count(4, {"count": 3}, drop_confirmations=3)
    assert json.loads(path.read_text())["count"] == 4


def test_one_bad_boot_does_not_lower_the_learned_count(tmp_path, monkeypatch):
    path = _state(tmp_path, monkeypatch, {"count": 3})
    rgb._remember_count(2, {"count": 3}, drop_confirmations=3)
    written = json.loads(path.read_text())
    assert written["count"] == 3        # still waits for the third device
    assert written["lowCount"] == 2 and written["lowSeen"] == 1


def test_a_removed_device_is_learned_after_enough_confirmations(tmp_path, monkeypatch):
    path = _state(tmp_path, monkeypatch)
    state = {"count": 3}
    for _ in range(3):
        rgb._remember_count(2, state, drop_confirmations=3)
        state = json.loads(path.read_text())
    assert state["count"] == 2


def test_a_good_boot_clears_the_drop_counter(tmp_path, monkeypatch):
    path = _state(tmp_path, monkeypatch)
    rgb._remember_count(3, {"count": 3, "lowCount": 2, "lowSeen": 2},
                        drop_confirmations=3)
    written = json.loads(path.read_text())
    assert written["count"] == 3 and "lowCount" not in written


# ── the rescan packet ──────────────────────────────────────────────────────

def test_rescan_sends_the_openrgb_rescan_header():
    """The exact 16 bytes OpenRGB's own "Rescan devices" button sends."""
    sent = []

    class FakeLock:
        def acquire(self, timeout=None):
            return True

        def release(self):
            sent.append("released")

    class FakeSock:
        def send(self, data):
            sent.append(data)

    class FakeComms:
        lock, sock = FakeLock(), FakeSock()

    client = type("C", (), {"comms": FakeComms()})()
    assert rgb.rescan_devices(client) is True
    header = sent[0]
    assert header[:4] == b"ORGB" and len(header) == 16
    assert int.from_bytes(header[8:12], "little") == rgb._RESCAN_PACKET_ID
    assert "released" in sent          # the SDK lock is never left held
