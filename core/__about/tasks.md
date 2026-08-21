# Scheduled Tasks

**Script:** [Tasks (script)](../tasks.py)

## Purpose
Register the four Ultra Vivid scheduled tasks, from the repo OR the frozen
exe — the task actions point at whatever is running (`python resolver.py`
in the repo, `UltraVivid.exe --tick` when packaged), so the same code
sets up both.

| Task | Trigger | Level | Action |
|------|---------|-------|--------|
| `OpenRGB server` | log on | **Highest (elevated)** | `OpenRGB.exe --server --startminimized` |
| `Ultra Vivid resolver` | every 10 min | normal | resolver tick (cache-respecting) |
| `Ultra Vivid wake` | log on + resume-from-sleep (**two** power events) | normal | resolver **`--force`** |
| `Ultra Vivid daemon` | log on (resident) | normal | hotkeys + optional Chroma |

**Why waking is a separate task (root cause of "no color after sleep",
fixed 2026-07-28):** a task has ONE action for all of its triggers. The resume
and log-on triggers used to sit on the resolver task, so waking ran the normal
tick — and the tick applies only when the schedule decision *changed*. After a
resume it is the same hour, same color, so the tick logged `Unchanged since
last tick — skipping apply` and wrote nothing, while the RGB RAM had come back
from sleep running its ONBOARD rainbow. A keyboard shortcut fixed it because a
shortcut always applies. Wake events therefore get their own task whose action
is `--force`: **after a power event the hardware state is unknown, so the
cache must not be trusted.** The 10-min tick keeps the cache — that is what
stops it from rewriting the devices 144 times a day. Regression-pinned by
[tests](../../tests/___tests.md) (`test_tasks.py`).

**Why TWO resume triggers (fixed 2026-08-21):** the wake task listened only
to `Microsoft-Windows-Power-Troubleshooter` EventID 1, which Windows does not
log on every wake. On the owner's machine the `Kernel-Power` EventID 107
resumes and the Power-Troubleshooter EventID 1 resumes were two DISJOINT
sets — so roughly half the wakes never ran the forced apply at all. The task
now carries both event triggers plus the log-on trigger. Two triggers firing
together is safe: Task Scheduler's default `MultipleInstances` policy ignores
the second start while the first is running, and a forced apply is
idempotent.

**Why OpenRGB runs as an elevated task (not the old Startup VBS):** the RAM
SMBus needs administrator rights. A non-elevated instance can enumerate the
RAM but not write to it, and TWO instances fight over the bus — the exact
"everything colors except the RAM" boot bug. The registration therefore also:

- **removes a conflicting auto-start `OpenRGB` *service*** — a second,
  non-`--server` instance that starts as SYSTEM, owns the SMBus, and blocks
  our server's RAM writes (this is a *service*, so earlier legacy-*task*
  cleanups never caught it);
- **deletes the old non-elevated `OpenRGB-Server.vbs`** from Startup;
- ensures exactly one live instance (kills any OpenRGB, then starts the task).

Registration runs elevated once (UAC). Only the OpenRGB server needs
elevation — the resolver/daemon are plain SDK clients (localhost), so they
stay non-elevated.

## Invoked by
- `python main.py --install-tasks` (repo) — or the GUI **Install tasks…** button
- the NSIS installer's "Run at startup" section (`UltraVivid.exe --install-tasks --elevated`)

## Connections
### Uses
- [Paths](paths.md) — repo-vs-frozen action commands

### Used by
- [Main Window](../../gui/__about/main_window.md) (Install tasks… button),
  `main.py` `--install-tasks` dispatch (Trivial tier, no separate doc)
