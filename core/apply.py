"""Apply a named color to the selected OpenRGB devices via the SDK.

Connects to the running OpenRGB server (retrying while it starts up),
filters devices by the config's include/exclude list, and sets colors
directly — no .orp profiles involved. Prefers each device's Direct mode
(no flash writes, no flicker); falls back to Static when the hardware
has no Direct mode (e.g. ASRock motherboard).

Color semantics: one hex -> every selected device gets it; N hex values
-> selected device i gets colors[i mod N] (device order = OpenRGB id).
None -> all selected devices go black (all RGB off).

The apply is CLOSED-LOOP (2026-08-21): the hardware is asked what it
actually shows, and `apply_color` returns an `ApplyResult` saying whether
the write can be trusted. A caller may cache "nothing changed" ONLY on a
trustworthy result — an unverified apply must stay retryable, or a device
that missed its color keeps it until the next reboot.
"""

import json
import logging
import struct
import time
from dataclasses import dataclass, field
from datetime import datetime

from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

from core import paths
from core.settings import Settings

logger = logging.getLogger(__name__)

_MODE_PREFERENCE = ["direct", "static"]

# OpenRGB SDK packet the server answers with a full hardware re-detection —
# exactly what the "Rescan devices" button in the OpenRGB GUI sends.
# openrgb-python has no wrapper for it, so the 16-byte header goes out raw.
# Verified against protocol_version 4: the device count drops to 1 and comes
# back complete within ~2 s.
_RESCAN_PACKET_ID = 140
_RESCAN_MAGIC = (b"O", b"R", b"G", b"B")


@dataclass(frozen=True)
class ApplyResult:
    """What the hardware actually did with the write.

    `trustworthy` is the ONLY thing a caller may cache on: it means every
    selected device was present AND read its color back correctly.
    """
    complete: bool                                       # device list was complete
    unverified: list[str] = field(default_factory=list)  # present, but read back wrong

    @property
    def trustworthy(self) -> bool:
        return self.complete and not self.unverified

    def reason(self) -> str:
        parts = []
        if not self.complete:
            parts.append("device list incomplete")
        if self.unverified:
            parts.append(f"did not take the color: {self.unverified}")
        return "; ".join(parts) or "ok"


def connect(settings: Settings) -> OpenRGBClient:
    """Connect to the SDK server, retrying while OpenRGB starts up."""
    o = settings.openrgb
    last_error: Exception | None = None
    for attempt in range(1, o.connect_retries + 1):
        try:
            return OpenRGBClient(o.host, o.port, "UltraVivid")
        except (ConnectionError, OSError, TimeoutError) as e:
            last_error = e
            logger.info("OpenRGB server not up yet (attempt %d/%d): %s",
                        attempt, o.connect_retries, e)
            time.sleep(o.retry_seconds)
    raise ConnectionError(
        f"OpenRGB SDK server unreachable at {o.host}:{o.port} "
        f"after {o.connect_retries} attempts"
    ) from last_error


def selected_devices(client: OpenRGBClient, settings: Settings) -> list:
    """Filter client.devices by the config include/exclude name list."""
    f = settings.devices
    needles = [n.lower() for n in f.names]

    def matches(device) -> bool:
        name = device.name.lower()
        return any(n in name for n in needles)

    if f.mode == "include":
        chosen = [d for d in client.devices if matches(d)]
    else:
        chosen = [d for d in client.devices if not matches(d)]
    logger.info("Devices selected: %s (of %s)",
                [d.name for d in chosen], [d.name for d in client.devices])
    return chosen


def is_razer_keyboard(device) -> bool:
    """The one rule for "this is a Razer keyboard" — the hardware behind both
    Hypershift shortcut sets and the Chroma module. Kept here so the GUI and
    the daemon never re-invent it."""
    return device.type.name == "KEYBOARD" and "razer" in device.name.lower()


def detect_hypershift_keyboard(settings: Settings) -> bool:
    """True when a Hypershift-capable keyboard (Razer) is present.
    Quick single-attempt probe; False when the server is unreachable."""
    import dataclasses
    quick = dataclasses.replace(
        settings, openrgb=dataclasses.replace(settings.openrgb, connect_retries=1))
    try:
        client = connect(quick)
    except ConnectionError:
        return False
    try:
        return any(is_razer_keyboard(d) for d in client.devices)
    finally:
        client.disconnect()


def rescan_devices(client: OpenRGBClient) -> bool:
    """Ask the SERVER to re-detect the hardware, and return True if it did.

    Polling a device list cannot find a device the server never enumerated:
    when OpenRGB starts before the SMBus is ready, the RGB RAM is simply
    absent, and it stays absent forever — until somebody clicks "Rescan
    devices" in the OpenRGB GUI. This is that click, sent over the SDK.

    False means the packet could not be sent (disconnected socket); the
    caller keeps waiting rather than treating it as fatal.
    """
    comms = client.comms
    header = struct.pack("ccccIII", *_RESCAN_MAGIC, 0, _RESCAN_PACKET_ID, 0)
    acquired = comms.lock.acquire(timeout=10)
    try:
        comms.sock.send(header)
        logger.info("Asked OpenRGB to rescan its devices.")
        return True
    except OSError as e:
        logger.warning("Rescan request failed: %s", e)
        return False
    finally:
        if acquired:
            comms.lock.release()


def _read_device_state() -> dict:
    """The learned hardware-readiness record, or {} when absent/unreadable."""
    try:
        state = json.loads(paths.DEVICE_STATE_PATH.read_text(encoding="utf-8"))
        return state if isinstance(state, dict) else {}
    except (OSError, ValueError, json.JSONDecodeError):
        return {}


def _expected_count(state: dict) -> int | None:
    """The device count seen last time the hardware was fully loaded, or None
    on first run / unreadable file."""
    try:
        return int(state["count"])
    except (KeyError, TypeError, ValueError):
        return None


def _write_device_state(count: int, low_count: int | None = None,
                        low_seen: int = 0) -> None:
    record = {"count": count, "at": datetime.now().isoformat()}
    if low_count is not None:
        record["lowCount"] = low_count
        record["lowSeen"] = low_seen
    paths.DEVICE_STATE_PATH.write_text(json.dumps(record), encoding="utf-8")


def _remember_count(count: int, state: dict, drop_confirmations: int) -> None:
    """Persist the ready device count so future boots wait for the same set.

    Raises IMMEDIATELY (a device was added), but lowers only after the same
    smaller count has been seen `drop_confirmations` runs in a row. A single
    bad boot used to rewrite the learned count downwards — after which the
    machine never waited for the slow device again, so one missed detection
    poisoned every boot that followed.
    """
    previous = _expected_count(state)
    if previous is None or count > previous:
        _write_device_state(count)
        return
    if count == previous:
        if state.get("lowCount") is not None:
            _write_device_state(count)          # clear a stale drop counter
        return

    seen = int(state.get("lowSeen", 0)) + 1 if state.get("lowCount") == count else 1
    if seen < drop_confirmations:
        _write_device_state(previous, low_count=count, low_seen=seen)
        logger.info("Only %d of %d devices (%d/%d confirmations) — keeping the "
                    "learned count at %d.",
                    count, previous, seen, drop_confirmations, previous)
        return
    logger.info("Only %d devices for %d runs in a row — learning the lower count.",
                count, seen)
    _write_device_state(count)


def wait_until_ready(client: OpenRGBClient, settings: Settings) -> bool:
    """Block until the OpenRGB device list is COMPLETE; True when it is.

    The SDK server reports the socket as ready before device detection
    finishes, so a slow device (typically RGB RAM) can be missing for a few
    seconds at log on — coloring "everything except the RAM". Worse, a device
    the server MISSED entirely never appears on its own. Generic fix, no
    hardware names: wait until as many devices are present as the last time
    everything was loaded (learned per machine, DEVICE_STATE_PATH), and when
    the wait runs out, ask the server to RESCAN and wait again.

    - Warm machine (shortcuts, ticks, resume): the count is already met, so
      this returns on the first poll — no added latency.
    - Cold boot with a slow device: polls until it appears.
    - Cold boot with a MISSED device: the rescan rounds bring it back.
    - First run ever (no learned count): waits for the count to plateau.
    - Exhausted (a device was physically removed): logs a warning and returns
      False, so the caller applies to what is present but does NOT cache it.
    """
    o = settings.openrgb
    if o.ready_timeout_seconds <= 0:
        return True
    state = _read_device_state()
    expected = _expected_count(state)

    for round_index in range(o.rescan_rounds + 1):
        if _poll_until_complete(client, o, expected):
            _remember_count(len(client.devices), state, o.count_drop_confirmations)
            return True
        if round_index < o.rescan_rounds:
            logger.warning(
                "Device list incomplete after %.0fs (%d present, expected %s)"
                " — rescan round %d/%d.", o.ready_timeout_seconds,
                len(client.devices), expected, round_index + 1, o.rescan_rounds)
            rescan_devices(client)
            time.sleep(o.ready_poll_seconds)

    logger.warning(
        "Device list still incomplete after %d rescan round(s) (%d present, "
        "expected %s) — applying to what is here, and NOT caching the result "
        "so the next tick tries again.",
        o.rescan_rounds, len(client.devices), expected)
    _remember_count(len(client.devices), state, o.count_drop_confirmations)
    return False


def _poll_until_complete(client: OpenRGBClient, o, expected: int | None) -> bool:
    """One waiting round: poll the device list until it is complete or the
    timeout runs out. True when complete."""
    deadline = time.monotonic() + o.ready_timeout_seconds
    last_count, stable = -1, 0
    waited = False

    while True:
        n = len(client.devices)
        if expected is not None:
            ready = n >= expected
        else:  # first run: no learned count — wait for the list to settle
            if n == last_count:
                stable += 1
            else:
                last_count, stable = n, 1
            ready = n > 0 and stable >= o.ready_stable_checks

        if ready:
            if waited:
                logger.info("Devices ready: %d present.", n)
            return True
        if time.monotonic() >= deadline:
            return False

        waited = True
        time.sleep(o.ready_poll_seconds)
        client.update()


def _wanted_mode(device):
    """The mode this device must be in for per-LED control, or None when the
    hardware offers neither Direct nor Static."""
    mode_names = {m.name.lower(): m for m in device.modes}
    for wanted in _MODE_PREFERENCE:
        if wanted in mode_names:
            return mode_names[wanted]
    return None


def _hex(color: RGBColor | None) -> str:
    if color is None:
        return "?"
    return f"{color.red:02X}{color.green:02X}{color.blue:02X}"


def verify_applied(client: OpenRGBClient, wanted: dict[int, RGBColor]) -> list[int]:
    """Re-read the hardware and return the ids of devices that did NOT take
    the write — wrong mode, or a first LED that is not the color we sent.

    This is the answer to "is OUR color the one actually showing": OpenRGB
    reports both `active_mode` and the per-LED `colors`, so the apply no
    longer has to assume the write landed.
    """
    client.update()
    failed = []
    for device in client.devices:
        expected = wanted.get(device.id)
        if expected is None:
            continue
        mode = device.modes[device.active_mode].name.lower() if device.modes else ""
        shown = device.colors[0] if device.colors else None
        if mode not in _MODE_PREFERENCE or shown is None or (
                shown.red, shown.green, shown.blue) != (
                expected.red, expected.green, expected.blue):
            logger.warning("%s did not take the write: mode=%s shows=#%s, wanted #%s",
                           device.name, mode or "?", _hex(shown), _hex(expected))
            failed.append(device.id)
    return failed


def apply_color(settings: Settings, color: str | None) -> ApplyResult:
    """Apply the named color (or all-off when None) to the selected devices,
    verify the hardware took it, and report whether the result can be cached."""
    colors = settings.colors[color] if color else ["000000"]
    client = connect(settings)
    try:
        complete = wait_until_ready(client, settings)
        devices = selected_devices(client, settings)
        if not devices:
            logger.warning("No devices left after filtering — nothing to apply.")
            return ApplyResult(complete=complete)

        wanted = {d.id: RGBColor.fromHEX(f"#{colors[i % len(colors)]}")
                  for i, d in enumerate(devices)}
        failed = _apply_and_verify(client, settings, wanted)
        names = {d.id: d.name for d in client.devices}
        result = ApplyResult(
            complete=complete,
            unverified=[names.get(i, str(i)) for i in failed],
        )
        if not result.trustworthy:
            logger.warning("Apply is not trustworthy — %s", result.reason())
        return result
    finally:
        client.disconnect()


def _apply_and_verify(client: OpenRGBClient, settings: Settings,
                      wanted: dict[int, RGBColor]) -> list[int]:
    """Write the colors, read them back, and re-write while the hardware
    disagrees. Returns the ids still wrong after the retries."""
    o = settings.openrgb
    targets = list(wanted)

    for attempt in range(o.verify_retries + 1):
        by_id = {d.id: d for d in client.devices}
        for device_id in targets:
            device = by_id.get(device_id)
            if device is None:
                continue        # vanished mid-apply; the readback below reports it
            _set_device_color(device, wanted[device_id])
            logger.info("Applied #%s to %s", _hex(wanted[device_id]), device.name)
        if o.verify_retries < 0:
            return []
        # verify_applied calls client.update(), which refreshes client.devices —
        # the loop above therefore re-binds its device objects every attempt.
        targets = verify_applied(client, {i: wanted[i] for i in targets})
        if not targets:
            return []
        if attempt < o.verify_retries:
            logger.warning("Re-applying to %d device(s) that did not take it.",
                           len(targets))
            time.sleep(o.ready_poll_seconds)
    return targets


def _set_device_color(device, color: RGBColor) -> None:
    mode = _wanted_mode(device)
    if mode is not None:
        # ALWAYS send the mode write (UpdateMode), even when OpenRGB already
        # reports this mode active. RGB RAM (e.g. HyperX Predator) powers up
        # running its ONBOARD effect while OpenRGB's *detected* state already
        # reads "Direct" — so the old `active_mode !=` guard skipped the
        # write, the hardware effect kept running, and the per-LED colors
        # were ignored (the RAM stayed on its rainbow until the user opened
        # the OpenRGB GUI and clicked). This forced UpdateMode IS what that
        # click does: it stops the onboard effect and latches Direct.
        device.set_mode(mode)
    device.set_color(color)
