# create-tasks.ps1

**Script:** [create-tasks.ps1 (script)](create-tasks.ps1)

## Purpose

Kreira Task Scheduler taskove za automatsko pokretanje RGB profila.

## Dependencies

- `$config` mora biti učitan (init.ps1)
- `$autoprofilePath`, `$openRGBPath` moraju biti definisani (init.ps1)
- Mora biti pokrenuto kao Administrator

## What It Does

1. **OpenRGB autoprofile task** - Trigger: At Log On
2. **Daily tasks** - Za svaki schedule, trigger: Daily at HH:MM

## Created Tasks

### OpenRGB autoprofile

| Podešavanje | Vrednost |
|-------------|----------|
| Trigger | At Log On (current user) |
| Action | `cmd.exe /c "autoprofile.bat"` |
| Run Level | Highest (admin) |
| Author | UV |

### OpenRGB [time] (daily tasks)

| Podešavanje | Vrednost |
|-------------|----------|
| Trigger | Daily at `config.schedules[].time` |
| Action | `OpenRGB.exe -p "profile"` |
| Run Level | Highest (admin) |
| Author | UV |

## Task Settings

Svi taskovi imaju ista podešavanja:

```powershell
New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `      # Radi i na bateriji
    -DontStopIfGoingOnBatteries `   # Ne prekida kad pređe na bateriju
    -StartWhenAvailable `           # Pokreće propuštene taskove
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)  # Max 5 min
```

## Notes

- Task names moraju početi sa "OpenRGB" jer `init.ps1` briše sve taskove koji počinju sa "OpenRGB*"
- `-Force` flag overwrite-uje postojeće taskove istog imena
