# Chroma

**Script:** [Chroma (script)](../chroma.py)

## Purpose
Color the Razer keyboard WITHOUT touching Synapse key bindings, via the
local Chroma SDK REST endpoint (`localhost:54235/razer/chromasdk`, installed
with Synapse). Lighting and input mapping are separate subsystems at Razer —
a Chroma session claims the keyboard's lighting only.

## Why the daemon holds it
A Chroma session dies without a heartbeat every few seconds (`HEARTBEAT_SECONDS
= 5.0`), so a one-shot process cannot keep a color on the keyboard. The
[Hotkey Daemon](../../__about/hotkey_daemon.md) owns the session and heartbeats
it. When Chroma is unreachable (no Synapse installed) the daemon logs a
warning and retries — documented fallback, never a crash.

## Protocol (pseudocode)

```
POST /razer/chromasdk {app info}     -> session uri
PUT  {uri}/heartbeat                  every ~5 s
PUT  {uri}/keyboard  {CHROMA_STATIC, color: BGR-packed int}   # RGB hex is
                                       reordered to BGR and bit-packed —
                                       Chroma's own wire format
DELETE {uri}                          on shutdown
```

Standard library only (`urllib`) — no extra dependencies.

## Connections

### Used by
- [Hotkey Daemon](../../__about/hotkey_daemon.md)
