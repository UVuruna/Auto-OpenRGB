# generate-bat.ps1

**Script:** [generate-bat.ps1 (script)](generate-bat.ps1)

## Purpose

Generates BAT files that automatically select RGB profile based on current hour:
- `generated/autoprofile.bat` - for daily profiles (schedules)
- `generated/autorainbow.bat` - for rainbow profiles

## Dependencies

- `$config` must be loaded (init.ps1)
- `$autoprofilePath` must be defined (init.ps1)
- `$autorainbowPath` must be defined (init.ps1)
- `$openRGBPath` must be defined (init.ps1)

## What It Does

1. Uses `New-TimeBatContent` function to generate BAT content
2. Automatically calculates time ranges from `startHour` and number of profiles
3. Generates IF conditions for each profile
4. Writes files to `generated/` folder

## Auto-Calculation Logic

Times are automatically calculated:
```
duration = 24 / number_of_profiles
start = (startHour + duration * index) % 24
end = (startHour + duration * (index + 1)) % 24
```

Example for 8 profiles with startHour=5:
- duration = 3 hours
- Profile 0: 05:00-08:00
- Profile 1: 08:00-11:00
- ...
- Profile 6: 23:00-02:00 (crosses midnight)
- Profile 7: 02:00-05:00

## Time Parsing Logic

BAT file extracts hour from `%time%` and removes leading zero:

```bat
for /f "tokens=1 delims=:" %%a in ("%time%") do set hour=%%a
if "%hour:~0,1%"==" " set hour=0%hour:~1,1%
set /a hour=%hour%
```

## Midnight Crossing Logic

| Condition | Generated IF | Example |
|-----------|--------------|---------|
| `start == 0` | `if %hour% LSS end` | 0-2 → `if %hour% LSS 2` |
| `end == 0` | `if %hour% GEQ start` | 22-0 → `if %hour% GEQ 22` |
| `end < start` | Two lines | 23-2 → `if %hour% GEQ 23` + `if %hour% LSS 2` |
| Normal | `if %hour% GEQ start if %hour% LSS end` | 6-9 → `if %hour% GEQ 6 if %hour% LSS 9` |

## Output

Generates two BAT files in `generated/` folder with same structure:

```bat
@echo off
REM Time parsing...

if %hour% GEQ 5 if %hour% LSS 8 goto 1_blue
if %hour% GEQ 8 if %hour% LSS 11 goto 2_cyan
...

goto end

:1_blue
"C:\...\OpenRGB.exe" -p "1-blue"
goto end

:2_cyan
...

:end
```
