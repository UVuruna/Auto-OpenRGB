@echo off
REM Auto-generisan fajl - ne edituj rucno!
REM Edituj config.json i pokreni setup.ps1

for /f "tokens=1 delims=:" %%a in ("%time%") do set hour=%%a
if "%hour:~0,1%"==" " set hour=0%hour:~1,1%
set /a hour=%hour%

REM echo SAT JE: %hour%
REM pause

if %hour% GEQ 3 if %hour% LSS 5 goto UC_01_00F
if %hour% GEQ 5 if %hour% LSS 7 goto UC_02_08F
if %hour% GEQ 7 if %hour% LSS 9 goto UC_03_0FF
if %hour% GEQ 9 if %hour% LSS 11 goto UC_04_0F8
if %hour% GEQ 11 if %hour% LSS 13 goto UC_05_0F0
if %hour% GEQ 13 if %hour% LSS 15 goto UC_06_8F0
if %hour% GEQ 15 if %hour% LSS 17 goto UC_07_FF0
if %hour% GEQ 17 if %hour% LSS 19 goto UC_08_F80
if %hour% GEQ 19 if %hour% LSS 21 goto UC_09_F00
if %hour% GEQ 21 if %hour% LSS 23 goto UC_10_F08
if %hour% GEQ 23 goto UC_11_F0F
if %hour% LSS 1 goto UC_11_F0F
if %hour% GEQ 1 if %hour% LSS 3 goto UC_12_80F

goto end

:UC_01_00F
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-01-00F"
goto end

:UC_02_08F
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-02-08F"
goto end

:UC_03_0FF
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-03-0FF"
goto end

:UC_04_0F8
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-04-0F8"
goto end

:UC_05_0F0
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-05-0F0"
goto end

:UC_06_8F0
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-06-8F0"
goto end

:UC_07_FF0
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-07-FF0"
goto end

:UC_08_F80
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-08-F80"
goto end

:UC_09_F00
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-09-F00"
goto end

:UC_10_F08
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-10-F08"
goto end

:UC_11_F0F
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-11-F0F"
goto end

:UC_12_80F
"C:\Program Files\OpenRGB\OpenRGB.exe" -p "UC-12-80F"
goto end

:end

