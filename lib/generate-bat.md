# generate-bat.ps1

**Script:** [generate-bat.ps1 (script)](generate-bat.ps1)

## Purpose

Generates VBS scripts that automatically select RGB profile based on current hour:
- `generated/autoprofile.vbs` - for daily profiles (with retry logic)
- `generated/autorainbow.vbs` - for rainbow profiles (no retry)

## Dependencies

- `$config` must be loaded (init.ps1)
- `$generatedPath` must be defined (init.ps1)
- `$openRGBPath` must be defined (init.ps1)

## What It Does

1. Uses `New-TimeVbs` function to generate VBS content
2. Automatically calculates time ranges from `startHour` and number of profiles
3. Generates `Select Case` conditions for each profile
4. Writes files to `generated/` folder
5. Cleans up old BAT files if they exist

## New-TimeVbs Function

Parameters:
- `$Items` - array of profile items from config
- `$StartHour` - hour when cycle begins
- `$OpenRGBPath` - path to OpenRGB.exe
- `$WithRetry` - if true, adds retry logic to wait for OpenRGB server

## Auto-Calculation Logic

Times are automatically calculated:
```
duration = 24 / number_of_profiles
start = (startHour + duration * index) % 24
end = (startHour + duration * (index + 1)) % 24
```

Example for 8 profiles with startHour=3:
- duration = 3 hours
- Profile 0: 03:00-06:00
- Profile 1: 06:00-09:00
- ...
- Profile 6: 21:00-00:00
- Profile 7: 00:00-03:00

## Midnight Crossing Logic

| Condition | Generated Case | Example |
|-----------|----------------|---------|
| `start == 0` | `Case currentHour < end` | 0-3 → `Case currentHour < 3` |
| `end == 0` | `Case currentHour >= start` | 21-0 → `Case currentHour >= 21` |
| `end < start` | `Case ... Or ...` | 23-2 → `Case currentHour >= 23 Or currentHour < 2` |
| Normal | `Case ... And ...` | 6-9 → `Case currentHour >= 6 And currentHour < 9` |

## Output

### autoprofile.vbs (with retry)

```vbs
Set WshShell = CreateObject("WScript.Shell")
Set objWMI = GetObject("winmgmts:\\.\root\cimv2")

' Wait for OpenRGB server (max 60 sec)
retries = 0
Do While retries < 30
    Set colProcesses = objWMI.ExecQuery("SELECT * FROM Win32_Process WHERE Name = 'OpenRGB.exe'")
    If colProcesses.Count > 0 Then Exit Do
    WScript.Sleep 2000
    retries = retries + 1
Loop

If retries >= 30 Then WScript.Quit

currentHour = Hour(Now)

Select Case True
    Case currentHour >= 3 And currentHour < 6
        profile = "1-blue"
    ...
End Select

WshShell.Run """...\OpenRGB.exe"" -p """ & profile & """", 0
WScript.Quit
```

### autorainbow.vbs (no retry)

Same structure but without the retry logic block.
