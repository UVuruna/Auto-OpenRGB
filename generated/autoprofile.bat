@echo off
REM Auto-generisan fajl - ne edituj rucno!
REM Edituj config.json i pokreni setup.ps1

for /f "tokens=1 delims=:" %%a in ("%time%") do set hour=%%a
if "%hour:~0,1%"==" " set hour=0%hour:~1,1%
set /a hour=%hour%

REM echo SAT JE: %hour%
REM pause

if %hour% GEQ 5 if %hour% LSS 8 goto 1_blue
if %hour% GEQ 8 if %hour% LSS 11 goto 2_cyan
if %hour% GEQ 11 if %hour% LSS 14 goto 3_green
if %hour% GEQ 14 if %hour% LSS 17 goto 4_yellow
if %hour% GEQ 17 if %hour% LSS 20 goto 5_orange
if %hour% GEQ 20 if %hour% LSS 23 goto 6_red
if %hour% GEQ 23 goto 7_magenta
if %hour% LSS 2 goto 7_magenta
if %hour% GEQ 2 if %hour% LSS 5 goto 8_purple

goto end

:1_blue
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "1-blue"
goto end

:2_cyan
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "2-cyan"
goto end

:3_green
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "3-green"
goto end

:4_yellow
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "4-yellow"
goto end

:5_orange
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "5-orange"
goto end

:6_red
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "6-red"
goto end

:7_magenta
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "7-magenta"
goto end

:8_purple
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "8-purple"
goto end

:end

