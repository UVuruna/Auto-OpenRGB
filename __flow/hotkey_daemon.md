# Hotkey Daemon — Flow

**About:** [description](../__about/hotkey_daemon.md)

## Main loop

```mermaid
%%{init: {'flowchart': {'subGraphTitleMargin': {'top': 0, 'bottom': 35}}}}%%
flowchart TB
    A[start] --> B{another instance running?<br/>named mutex}
    B -- yes --> END1[log + exit]
    B -- no --> C[Daemon.__init__: load config]
    C --> D[register_hotkeys from config<br/>skip hypershift sets]
    D --> E[start chroma_thread<br/>daemon thread, heartbeat loop]
    E --> F[SetTimer RELOAD_POLL_MS = 5000]
    F --> LOOP{GetMessageW}
    LOOP -- WM_TIMER --> G[reload_if_changed:<br/>config.json mtime changed?]
    G -- yes --> H[reload config;<br/>re-register hotkeys] --> LOOP
    G -- no --> LOOP
    LOOP -- WM_HOTKEY --> I[look up binding by hotkey id]
    I --> J[worker thread: apply_binding<br/>resolve_binding -> apply_color -> push_chroma] --> LOOP
    LOOP -- WM_QUIT/error --> END2[stop_event.set; exit]
```

## Chroma thread (parallel, independent of the message loop)

```
chroma_thread():
    last_color = SENTINEL                      # forces first push
    LOOP every HEARTBEAT_SECONDS (~5s):
        IF chroma disabled:
            close session if open; continue
        TRY:
            IF no session -> open one; last_color = SENTINEL
            heartbeat()
            IF follow_schedule:
                color = schedule.resolve(cfg, now)
                IF color != last_color:
                    push_chroma(color); last_color = color
        ON ChromaError:
            log warning; drop session (retried next beat)
```

Both loops run concurrently: hotkey (un)registration and Win32 message
dispatch stay on the daemon's own thread (Win32 requirement — `RegisterHotKey`
is tied to the registering thread's message queue), while heartbeats and
schedule-following happen on the independent `chroma_thread`. A hotkey press
spawns its OWN short-lived worker thread so a slow SDK call never blocks the
message loop from picking up the next keypress.
