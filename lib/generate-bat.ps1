# generate-bat.ps1 - Generiši autoprofile.bat i autorainbow.bat

# Funkcija za generisanje BAT sadrzaja
function New-TimeBatContent {
    param (
        [array]$Items,
        [int]$StartHour,
        [string]$OpenRGBPath
    )

    $count = $Items.Count
    $duration = [int][math]::Floor(24 / $count)

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

    # Izracunaj start/end za svaki item i generiši uslove
    for ($i = 0; $i -lt $count; $i++) {
        $item = $Items[$i]
        $prof = $item.profile
        $label = $prof -replace '-','_'

        $start = [int](($StartHour + $duration * $i) % 24)
        $end = [int](($StartHour + $duration * ($i + 1)) % 24)

        if ($start -eq 0) {
            # Pocinje u ponoc (npr. 0-2) - samo manji od end
            $batContent += "if %hour% LSS $end goto $label`r`n"
        } elseif ($end -eq 0) {
            # Zavrsava u ponoc (npr. 22-0) - samo veci od start
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

    # Generiši labele
    foreach ($item in $Items) {
        $prof = $item.profile
        $label = $prof -replace '-','_'
        $batContent += ":$label`r`n"
        $batContent += "`"$OpenRGBPath`" -p `"$prof`"`r`n"
        $batContent += "goto end`r`n`r`n"
    }

    $batContent += ":end`r`n"

    return $batContent
}

# Generiši autoprofile.bat
Write-Host "Generisem autoprofile.bat..." -ForegroundColor Yellow

$autoprofileContent = New-TimeBatContent -Items $config.schedules.items -StartHour $config.schedules.startHour -OpenRGBPath $openRGBPath
$autoprofileContent | Out-File -FilePath $autoprofilePath -Encoding ASCII
Write-Host "Kreiran: generated/autoprofile.bat" -ForegroundColor Green

# Generiši autorainbow.bat
Write-Host "Generisem autorainbow.bat..." -ForegroundColor Yellow

$autorainbowContent = New-TimeBatContent -Items $config.rainbow.items -StartHour $config.rainbow.startHour -OpenRGBPath $openRGBPath
$autorainbowContent | Out-File -FilePath $autorainbowPath -Encoding ASCII
Write-Host "Kreiran: generated/autorainbow.bat" -ForegroundColor Green
