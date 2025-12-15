# generate-bat.ps1 - Generiši autoprofile.bat

Write-Host "Generisem autoprofile.bat..." -ForegroundColor Yellow

$batContent = @"
@echo off
REM Auto-generisan fajl - ne edituj rucno!
REM Edituj config.json i pokreni setup.ps1

for /f "tokens=1 delims=:" %%a in ("%time%") do set hour=%%a
if "%hour:~0,1%"==" " set hour=0%hour:~1,1%
set /a hour=%hour%

REM echo SAT JE: %hour%
REM pause


"@

# Sortiraj po hourStart za pravilnu obradu
$sorted = $config.schedules | Sort-Object hourStart

foreach ($s in $sorted) {
    $prof = $s.profile
    $start = $s.hourStart
    $end = $s.hourEnd
    $label = $prof -replace '-','_'

    if ($start -eq 0) {
        # Pocinje u ponoc (npr. 0-3) - samo manji od end
        $batContent += "if %hour% LSS $end goto $label`r`n"
    } elseif ($end -eq 0) {
        # Zavrsava u ponoc (npr. 20-0) - samo veci od start
        $batContent += "if %hour% GEQ $start goto $label`r`n"
    } elseif ($end -lt $start) {
        # Prelazi preko ponoci (npr. 23-2) - dva odvojena uslova
        $batContent += "if %hour% GEQ $start goto $label`r`n"
        $batContent += "if %hour% LSS $end goto $label`r`n"
    } else {
        # Normalan raspon (npr. 6-9)
        $batContent += "if %hour% GEQ $start if %hour% LSS $end goto $label`r`n"
    }
}

$batContent += "`r`ngoto end`r`n`r`n"

foreach ($s in $config.schedules) {
    $prof = $s.profile
    $label = $prof -replace '-','_'
    $batContent += ":$label`r`n"
    $batContent += "`"$openRGBPath`" -p `"$prof`"`r`n"
    $batContent += "goto end`r`n`r`n"
}

$batContent += ":end`r`n"

$batContent | Out-File -FilePath $autoprofilePath -Encoding ASCII
Write-Host "Kreiran: autoprofile.bat" -ForegroundColor Green
