# create-tasks.ps1

**Script:** [create-tasks.ps1 (script)](create-tasks.ps1)

## Purpose

Creates Task Scheduler tasks for automatic RGB profile execution.

## Dependencies

- `$config` must be loaded (init.ps1)
- `$autoprofilePath`, `$openRGBPath` must be defined (init.ps1)
- Must be run as Administrator

## What It Does

1. **OpenRGB autoprofile task** - Trigger: At Log On
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
| Trigger | At Log On (current user) |
| Action | `cmd.exe /c "generated\autoprofile.bat"` |
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

All tasks have the same settings:

```powershell
New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `      # Works on battery
    -DontStopIfGoingOnBatteries `   # Doesn't stop when switching to battery
    -StartWhenAvailable `           # Runs missed tasks
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)  # Max 5 min
```

## Notes

- Task names must start with "OpenRGB" because `init.ps1` deletes all tasks starting with "OpenRGB*"
- `-Force` flag overwrites existing tasks with same name
- BAT file is now located in `generated/` folder
