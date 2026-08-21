"""Scheduled-task registration — the shape of the generated PowerShell.

REGRESSION (2026-07-28, "no color after resume from sleep"): the resume and
log-on triggers used to sit on the resolver task, whose single action is the
cache-respecting tick. After a resume the schedule decision is unchanged, so
the tick logged "Unchanged since last tick — skipping apply" and wrote nothing
— while the RGB RAM had come back from sleep running its ONBOARD rainbow. The
power-event path must therefore live on its own task that FORCES the apply.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core import tasks


def _action_argument(script: str, variable: str) -> str:
    """The -Argument value of the New-ScheduledTaskAction assigned to $variable."""
    line = next(l for l in script.splitlines() if l.startswith(f"${variable} ="))
    return re.search(r"-Argument '(.*)'", line).group(1)


def _task_block(script: str, task_name: str) -> str:
    """The script text from the previous Register-ScheduledTask up to the one
    that registers `task_name` — i.e. everything that defines that task."""
    end = script.index(f'Register-ScheduledTask -TaskName "{task_name}"')
    previous = script.rfind("Register-ScheduledTask", 0, end)
    return script[previous:end]


def test_wake_is_its_own_task_and_forces_the_apply():
    script = tasks._build_script()
    assert f'-TaskName "{tasks.WAKE_TASK}"' in script
    assert "--force" in _action_argument(script, "wakeAction")


def test_power_triggers_belong_to_the_wake_task_not_the_cached_tick():
    script = tasks._build_script()
    resolver_block = _task_block(script, tasks.RESOLVER_TASK)
    wake_block = _task_block(script, tasks.WAKE_TASK)

    # The resolver task is the periodic tick only — no log-on, no resume.
    assert "-Trigger $tick" in resolver_block
    assert "AtLogOn" not in resolver_block
    assert "Power-Troubleshooter" not in resolver_block

    # Both power events drive the forced task.
    assert "AtLogOn" in wake_block
    assert "Power-Troubleshooter" in wake_block


def test_tick_action_keeps_the_cache():
    """The 10-min tick must NOT force — otherwise every tick rewrites the
    devices, which is what the state cache exists to avoid."""
    script = tasks._build_script()
    assert "--force" not in _action_argument(script, "resolverAction")


def test_both_resume_events_drive_the_wake_task():
    """REGRESSION (2026-08-21): the wake task listened ONLY to
    Power-Troubleshooter/1. On his machine the Kernel-Power/107 resumes and
    the Power-Troubleshooter/1 resumes were two DISJOINT sets — half the
    wakes never ran the forced apply at all."""
    wake_block = _task_block(tasks._build_script(), tasks.WAKE_TASK)
    assert "Microsoft-Windows-Power-Troubleshooter" in wake_block
    assert "Microsoft-Windows-Kernel-Power" in wake_block
    assert "EventID=107" in wake_block
    assert "-Trigger @($logon, $resume, $resumeKernel)" in wake_block
