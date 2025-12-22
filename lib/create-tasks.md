# create-tasks.ps1

**Script:** [create-tasks.ps1 (script)](create-tasks.ps1)

## Purpose

Creates Task Scheduler tasks for automatic RGB profile execution.

## Dependencies

- `$config` must be loaded (init.ps1)
- `$generatedPath`, `$openRGBPath` must be defined (init.ps1)
- Must be run as Administrator

## What It Does

1. **OpenRGB autoprofile task** - Triggers: At Log On + Resume from Sleep
2. **Daily tasks** - For each schedule, trigger: Daily at auto-calculated time

## Time Auto-Calculation

Time is automatically calculated for each task:
```
duration = 24 / number_of_profiles
time = (startHour + duration * index) % 24
```

Example for 8 profiles with startHour=5:
- Profile 0: 05:00
- Profile 1: 08:00
- ...
- Profile 7: 02:00

## Created Tasks

### OpenRGB autoprofile

| Setting | Value |
|---------|-------|
| Trigger 1 | At Log On (current user) |
| Trigger 2 | Resume from Sleep (Power-Troubleshooter Event ID 1) |
| Action | `wscript.exe "generated\autoprofile.vbs"` |
| Run Level | Highest (admin) |
| Author | UV |

### OpenRGB [taskName] (daily tasks)

| Setting | Value |
|---------|-------|
| Trigger | Daily at auto-calculated time |
| Action | `OpenRGB.exe -p "profile"` |
| Run Level | Highest (admin) |
| Author | UV |

## Task Settings

### Autoprofile task

```powershell
New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `      # Works on battery
    -DontStopIfGoingOnBatteries `   # Doesn't stop when switching to battery
    -StartWhenAvailable `           # Runs after sleep/missed trigger
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)  # Max 5 min
```

### Daily tasks

```powershell
New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `      # Works on battery
    -DontStopIfGoingOnBatteries `   # Doesn't stop when switching to battery
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)  # Max 5 min
```

Note: Daily tasks do NOT have `-StartWhenAvailable` to prevent all tasks from running at once when setup.ps1 is executed.

## Notes

- Task names must start with "OpenRGB" because `init.ps1` deletes all tasks starting with "OpenRGB*"
- `-Force` flag overwrites existing tasks with same name
- VBS script has retry logic to wait for OpenRGB server (max 60 sec)
