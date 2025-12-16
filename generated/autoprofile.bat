@echo off
REM Auto-generated file - do not edit manually!
REM Edit config.json and run setup.ps1

for /f "tokens=1 delims=:" %%a in ("%time%") do set hour=%%a
if "%hour:~0,1%"==" " set hour=0%hour:~1,1%
set /a hour=%hour%

REM echo HOUR IS: %hour%
REM pause

if %hour% GEQ 3 if %hour% LSS 6 goto 1_blue
if %hour% GEQ 6 if %hour% LSS 9 goto 2_cyan
if %hour% GEQ 9 if %hour% LSS 12 goto 3_green
if %hour% GEQ 12 if %hour% LSS 15 goto 4_yellow
if %hour% GEQ 15 if %hour% LSS 18 goto 5_orange
if %hour% GEQ 18 if %hour% LSS 21 goto 6_red
if %hour% GEQ 21 goto 7_magenta
if %hour% LSS 3 goto 8_purple

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

