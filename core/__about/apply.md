# Apply

**Script:** [Apply (script)](../apply.py) ·
**Flow:** [diagram](../__flow/apply.md)

## Purpose
Put a color on the hardware through the OpenRGB SDK server
(default `127.0.0.1:6742`) — no `.orp` profiles, no CLI spawning.

## Behavior (pseudocode)

```
CONNECT with retry (server may still be starting at log on)
complete = WAIT until the device list is COMPLETE (wait_until_ready),
           asking the SERVER to RESCAN between waiting rounds
devices = ALL devices, filtered by config include/exclude substrings
REPEAT up to verifyRetries + 1 times:
    FOR EACH selected device i:
        color = colors[i mod N]        (one color -> everything;
                                        N colors -> round-robin by device)
        ALWAYS write mode "Direct" (fallback "Static") — even if OpenRGB
            already reports that mode: RGB RAM boots running its ONBOARD
            effect while OpenRGB's detected state already says "Direct", so
            only a forced mode write stops the effect and latches Direct
            (what the GUI click does)
        set color
    READ BACK (verify_applied): active_mode and colors[0] per device
    STOP when every selected device shows what we sent
RETURN ApplyResult(complete, unverified) — trustworthy only when BOTH hold
color is None -> every selected device gets 000000 (all RGB off)
no devices left after filtering -> log a warning, apply nothing
```

## The closed loop (2026-08-21)

The apply is no longer fire-and-forget. OpenRGB reports both `active_mode`
and the per-LED `colors`, so the module ASKS the hardware what it shows and
returns an `ApplyResult`:

| field | meaning |
|-------|---------|
| `complete` | every expected device was present in the OpenRGB list |
| `unverified` | devices that were present but read back the wrong mode/color |
| `trustworthy` | `complete` AND nothing `unverified` — the ONLY thing a caller may cache on |

[Resolver](../../__about/resolver.md) writes `state.json` only on a
trustworthy result. An untrustworthy apply leaves the state WITHOUT a
`lastColor` key, so the next 10-min tick applies again instead of answering
"unchanged" forever — the defect that left the RGB RAM uncolored for a whole
session on 2026-08-21.

## Rescan — finding a device the server never enumerated

Polling cannot find what OpenRGB never detected: when the server starts
before the SMBus is ready it simply has no RAM entry, and it never looks
again. `rescan_devices(client)` sends SDK packet `140`
(`NET_PACKET_ID_RESCAN_DEVICES`) — the wire form of the OpenRGB GUI's
"Rescan devices" button. `openrgb-python` has no wrapper, so the 16-byte
header goes out raw on the client socket under the SDK lock. Verified
against protocol version 4: the device count drops and comes back complete
within ~2 s.

## Razer keyboard detection

`is_razer_keyboard(device)` is the ONE rule for "this is a Razer keyboard"
(type `KEYBOARD` + `razer` in the name, case-insensitive). Both Razer-only
features read it, so the rule is never re-invented: the Shortcuts tab offers
the Hypershift selector, and the Devices tab shows the Chroma section, only
when it matches. `detect_hypershift_keyboard(settings)` is the standalone
single-attempt probe built on it (a single-retry connect; `False` when the
server is unreachable).

## Connections

### Uses
- [Settings](settings.md); [Paths](paths.md) — `DEVICE_STATE_PATH`;
  `openrgb-python` (SDK client)

### Used by
- [Resolver (flow)](../../__flow/resolver.md), [Hotkey Daemon (flow)](../../__flow/hotkey_daemon.md),
  [Devices Tab](../../gui/__about/devices_tab.md), [Main Window](../../gui/__about/main_window.md)
