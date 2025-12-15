# generate-bat.ps1

**Script:** [generate-bat.ps1 (script)](generate-bat.ps1)

## Purpose

Generiše `autoprofile.bat` koji automatski bira RGB profil na osnovu trenutnog sata.

## Dependencies

- `$config` mora biti učitan (init.ps1)
- `$autoprofilePath` mora biti definisan (init.ps1)
- `$openRGBPath` mora biti definisan (init.ps1)

## What It Does

1. Kreira BAT header sa time parsing logikom
2. Za svaki schedule iz config.json generiše IF uslov
3. Generiše label sekcije za svaki profil
4. Upisuje fajl u `$autoprofilePath`

## Time Parsing Logic

BAT fajl izvlači sat iz `%time%` i uklanja vodeću nulu:

```bat
for /f "tokens=1 delims=:" %%a in ("%time%") do set hour=%%a
if "%hour:~0,1%"==" " set hour=0%hour:~1,1%
set /a hour=%hour%
```

## hourStart / hourEnd Logic

| Uslov | Generisani IF | Primer |
|-------|---------------|--------|
| `start == 0` | `if %hour% LSS end` | 0-3 → `if %hour% LSS 3` |
| `end == 0` | `if %hour% GEQ start` | 20-0 → `if %hour% GEQ 20` |
| `end < start` | Dva reda | 23-2 → `if %hour% GEQ 23` + `if %hour% LSS 2` |
| Normalno | `if %hour% GEQ start if %hour% LSS end` | 6-9 → `if %hour% GEQ 6 if %hour% LSS 9` |

## Output

Generiše `autoprofile.bat` sa strukturom:

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
