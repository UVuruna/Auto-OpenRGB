# Apply

**Script:** [Apply (script)](../apply.py) ·
**Flow:** [diagram](../__flow/apply.md)

## Purpose
Put a color on the hardware through the OpenRGB SDK server
(default `127.0.0.1:6742`) — no `.orp` profiles, no CLI spawning.

## Behavior (pseudocode)

```
CONNECT with retry (server may still be starting at log on)
WAIT until the device list is COMPLETE (wait_until_ready) — see flow diagram
devices = ALL devices, filtered by config include/exclude substrings
FOR EACH selected device i:
    color = colors[i mod N]            (one color -> everything;
                                        N colors -> round-robin by device)
    ALWAYS write mode "Direct" (fallback "Static") — even if OpenRGB already
        reports that mode: RGB RAM boots running its ONBOARD effect while
        OpenRGB's detected state already says "Direct", so only a forced mode
        write stops the effect and latches Direct (what the GUI click does)
    set color
color is None -> every selected device gets 000000 (all RGB off)
no devices left after filtering -> log a warning, apply nothing
```

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
