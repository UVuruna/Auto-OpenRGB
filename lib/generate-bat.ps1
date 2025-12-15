# generate-bat.ps1 - Generate autoprofile.bat and autorainbow.bat

# Function to generate BAT content
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
REM Auto-generated file - do not edit manually!
REM Edit config.json and run setup.ps1

for /f "tokens=1 delims=:" %%a in ("%time%") do set hour=%%a
if "%hour:~0,1%"==" " set hour=0%hour:~1,1%
set /a hour=%hour%

REM echo HOUR IS: %hour%
REM pause


"@

    # Calculate start/end for each item and generate conditions
    for ($i = 0; $i -lt $count; $i++) {
        $item = $Items[$i]
        $prof = $item.profile
        $label = $prof -replace '-','_'

        $start = [int](($StartHour + $duration * $i) % 24)
        $end = [int](($StartHour + $duration * ($i + 1)) % 24)

        if ($start -eq 0) {
            # Starts at midnight (e.g., 0-2) - only less than end
            $batContent += "if %hour% LSS $end goto $label`r`n"
        } elseif ($end -eq 0) {
            # Ends at midnight (e.g., 22-0) - only greater than start
            $batContent += "if %hour% GEQ $start goto $label`r`n"
        } elseif ($end -lt $start) {
            # Crosses midnight (e.g., 23-2) - two separate conditions
            $batContent += "if %hour% GEQ $start goto $label`r`n"
            $batContent += "if %hour% LSS $end goto $label`r`n"
        } else {
            # Normal range (e.g., 6-9)
            $batContent += "if %hour% GEQ $start if %hour% LSS $end goto $label`r`n"
        }
    }

    $batContent += "`r`ngoto end`r`n`r`n"

    # Generate labels
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

# Generate autoprofile.bat
Write-Host "Generating autoprofile.bat..." -ForegroundColor Yellow

$autoprofileContent = New-TimeBatContent -Items $config.schedules.items -StartHour $config.schedules.startHour -OpenRGBPath $openRGBPath
$autoprofileContent | Out-File -FilePath $autoprofilePath -Encoding ASCII
Write-Host "Created: generated/autoprofile.bat" -ForegroundColor Green

# Generate autorainbow.bat
Write-Host "Generating autorainbow.bat..." -ForegroundColor Yellow

$autorainbowContent = New-TimeBatContent -Items $config.rainbow.items -StartHour $config.rainbow.startHour -OpenRGBPath $openRGBPath
$autorainbowContent | Out-File -FilePath $autorainbowPath -Encoding ASCII
Write-Host "Created: generated/autorainbow.bat" -ForegroundColor Green
