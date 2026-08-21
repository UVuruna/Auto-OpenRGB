"""Register the Ultra Vivid scheduled tasks — from the repo OR the exe.

Four tasks (all point at whatever is running us):
  - "OpenRGB server"        log on, ELEVATED (--server --startminimized).
                            Elevation is REQUIRED for the RAM SMBus, and this
                            single instance exposes the SDK the resolver/daemon
                            talk to.
  - "Ultra Vivid resolver"  10-min tick, cache-respecting (a tick whose
                            decision did not change applies nothing)
  - "Ultra Vivid wake"      log on + resume-from-sleep (TWO power events),
                            resolver --force
  - "Ultra Vivid daemon"    log on, resident (hotkeys + optional Chroma)

WHY the wake path is a SEPARATE task: a Task Scheduler task has ONE action for
all its triggers, so a wake trigger on the resolver task ran the same
cache-respecting tick — and the cache said "same color as before sleep, nothing
to do". But sleep/power-off RESETS the hardware: the RGB RAM comes back running
its onboard rainbow while our state file still claims the scheduled color. The
result was exactly the reported bug — color restored after a shortcut or a
power-on, never after a resume. Waking is therefore its own task whose action
FORCES the apply, because after a power event the hardware state is unknown.

Also removes two conflict sources that leave the RAM uncontrollable at boot:
  - an auto-start "OpenRGB" *service* — a SECOND, non-server instance that
    starts as SYSTEM and OWNS the SMBus, so our --server instance can enumerate
    the RAM but never write to it (everything colors except the RAM);
  - the old non-elevated Startup VBS — a non-elevated instance cannot own the
    SMBus, and two instances fight over it.

The registration itself is PowerShell (New-ScheduledTask*, the CIM event
trigger for resume-from-sleep) run elevated once — the proven approach.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from core import paths

RESOLVER_TASK = "Ultra Vivid resolver"
WAKE_TASK = "Ultra Vivid wake"
DAEMON_TASK = "Ultra Vivid daemon"
OPENRGB_TASK = "OpenRGB server"


def _action(*args: str) -> tuple[str, str]:
    """(Execute, Arguments) for a scheduled-task action that re-invokes
    this program with the given flags — windowless in both modes."""
    if paths.IS_FROZEN:
        return sys.executable, " ".join(args)
    pythonw = str(Path(sys.executable).parent / "pythonw.exe")
    script = "resolver.py" if args and args[0] != "--daemon" else "hotkey_daemon.py"
    inner = [str(paths.BUNDLE_DIR / script), *[a for a in args if a != "--daemon" and a != "--tick"]]
    return pythonw, " ".join(f'"{part}"' if " " in part else part for part in inner)


def _openrgb_path() -> str:
    """OpenRGB.exe path from config, or the default install location."""
    try:
        return json.loads(
            paths.CONFIG_PATH.read_text(encoding="utf-8"))["openrgb"]["path"]
    except (OSError, KeyError, json.JSONDecodeError):
        return r"C:\Program Files\OpenRGB\OpenRGB.exe"


def _remove_startup_vbs() -> None:
    """Delete the old non-elevated Startup launcher. OpenRGB now starts via an
    ELEVATED scheduled task — a non-elevated instance cannot own the RAM SMBus,
    and two instances fight over it (the RAM stops responding to the SDK)."""
    vbs = (Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu"
           / "Programs" / "Startup" / "OpenRGB-Server.vbs")
    if vbs.exists():
        vbs.unlink()


def _build_script() -> str:
    resolver_exe, resolver_args = _action("--tick")
    wake_exe, wake_args = _action("--force")
    daemon_exe, daemon_args = _action("--daemon")
    openrgb = _openrgb_path()

    return f"""
$ErrorActionPreference = "Stop"

# Remove a conflicting auto-start "OpenRGB" SERVICE — a second, non-server
# instance that starts as SYSTEM and owns the RAM SMBus, so our --server
# instance can see the RAM but never write to it (colors everything but RAM).
$svc = Get-Service -Name 'OpenRGB' -ErrorAction SilentlyContinue
if ($svc) {{
    Stop-Service -Name 'OpenRGB' -Force -ErrorAction SilentlyContinue
    & sc.exe delete 'OpenRGB' | Out-Null
    Write-Host "Removed conflicting OpenRGB service"
}}

# OpenRGB SDK server — ELEVATED (RAM SMBus needs admin) at log on.
$openrgbAction = New-ScheduledTaskAction -Execute '{openrgb}' -Argument '--server --startminimized'
$oLogon = New-ScheduledTaskTrigger -AtLogOn
$oLogon.UserId = "$env:USERDOMAIN\\$env:USERNAME"
$oPrincipal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\\$env:USERNAME" -LogonType Interactive -RunLevel Highest
$oSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit ([TimeSpan]::Zero)
$oTask = New-ScheduledTask -Action $openrgbAction -Trigger $oLogon -Principal $oPrincipal -Settings $oSettings
$oTask.Author = "UV"
Register-ScheduledTask -TaskName "{OPENRGB_TASK}" -InputObject $oTask -Force | Out-Null
Write-Host "Registered: {OPENRGB_TASK} (elevated)"

# Scheduled tick — cache-respecting: applies only when the decision changed.
$resolverAction = New-ScheduledTaskAction -Execute '{resolver_exe}' -Argument '{resolver_args}'
$tick = New-ScheduledTaskTrigger -Once -At ([datetime]::Today) -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration (New-TimeSpan -Days 3650)

$rSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
$rTask = New-ScheduledTask -Action $resolverAction -Trigger $tick -Settings $rSettings
$rTask.Author = "UV"
Register-ScheduledTask -TaskName "{RESOLVER_TASK}" -InputObject $rTask -Force | Out-Null
Write-Host "Registered: {RESOLVER_TASK}"

# Wake — log on + resume-from-sleep, run with --force: a power event resets the
# hardware (RGB RAM returns to its onboard effect), so the "unchanged decision"
# cache must NOT be trusted here.
$wakeAction = New-ScheduledTaskAction -Execute '{wake_exe}' -Argument '{wake_args}'
$logon = New-ScheduledTaskTrigger -AtLogOn
$logon.UserId = "$env:USERDOMAIN\\$env:USERNAME"

$eventClass = Get-CimClass -ClassName MSFT_TaskEventTrigger -Namespace Root/Microsoft/Windows/TaskScheduler
$resume = New-CimInstance -CimClass $eventClass -ClientOnly
$resume.Subscription = '<QueryList><Query Id="0" Path="System"><Select Path="System">*[System[Provider[@Name=''Microsoft-Windows-Power-Troubleshooter''] and EventID=1]]</Select></Query></QueryList>'
$resume.Enabled = $true

# SECOND resume trigger. Power-Troubleshooter/1 is not logged on every wake:
# on this class of machine the Kernel-Power/107 resumes and the
# Power-Troubleshooter/1 resumes were two DISJOINT sets, so half the wakes
# never ran the forced apply at all. Both triggers on one task is safe —
# Task Scheduler's default MultipleInstances policy ignores the second start
# while the first is still running, and a repeated forced apply is idempotent.
$resumeKernel = New-CimInstance -CimClass $eventClass -ClientOnly
$resumeKernel.Subscription = '<QueryList><Query Id="0" Path="System"><Select Path="System">*[System[Provider[@Name=''Microsoft-Windows-Kernel-Power''] and EventID=107]]</Select></Query></QueryList>'
$resumeKernel.Enabled = $true

$wTask = New-ScheduledTask -Action $wakeAction -Trigger @($logon, $resume, $resumeKernel) -Settings $rSettings
$wTask.Author = "UV"
Register-ScheduledTask -TaskName "{WAKE_TASK}" -InputObject $wTask -Force | Out-Null
Write-Host "Registered: {WAKE_TASK}"

$daemonAction = New-ScheduledTaskAction -Execute '{daemon_exe}' -Argument '{daemon_args}'
$dLogon = New-ScheduledTaskTrigger -AtLogOn
$dLogon.UserId = "$env:USERDOMAIN\\$env:USERNAME"
$dSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit ([TimeSpan]::Zero)
$dTask = New-ScheduledTask -Action $daemonAction -Trigger $dLogon -Settings $dSettings
$dTask.Author = "UV"
Register-ScheduledTask -TaskName "{DAEMON_TASK}" -InputObject $dTask -Force | Out-Null
Write-Host "Registered: {DAEMON_TASK}"

# Ensure exactly ONE (elevated) OpenRGB instance right now — kill any current
# one (the removed service / old VBS may have started it), then start the task.
Get-Process -Name 'OpenRGB' -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 700
Start-ScheduledTask -TaskName "{OPENRGB_TASK}"
Write-Host "Started: {OPENRGB_TASK}"
"""


def install(elevated: bool = False) -> None:
    """Register the tasks. When not already elevated, relaunch this same
    step under UAC and wait for it."""
    paths.ensure_state()
    _remove_startup_vbs()
    script = _build_script()
    script_file = Path(tempfile.gettempdir()) / "ultravivid_install_tasks.ps1"
    script_file.write_text(script, encoding="utf-8")

    if elevated:
        # Already elevated (NSIS installer / re-launch): run directly, no window.
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                        "-WindowStyle", "Hidden", "-File", str(script_file)],
                       check=False, **paths.no_window())
    else:
        # Elevate via UAC; the spawned registration window stays hidden.
        subprocess.run([
            "powershell", "-NoProfile", "-Command",
            f'Start-Process powershell -ArgumentList '
            f'"-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"{script_file}`"" '
            f'-Verb RunAs -Wait -WindowStyle Hidden'
        ], check=False, **paths.no_window())
