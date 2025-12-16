# generate-bat.ps1 - Generate autoprofile.vbs, autoprofile.bat and autorainbow.bat

# Function to generate VBS content with retry logic
function New-AutoprofileVbs {
    param (
        [array]$Items,
        [int]$StartHour,
        [string]$OpenRGBPath
    )

    $count = $Items.Count
    $duration = [int][math]::Floor(24 / $count)

    $vbsContent = @"
' Auto-generated file - do not edit manually!
' Edit config.json and run setup.ps1

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

' Get current hour
currentHour = Hour(Now)

' Determine profile based on hour
Select Case True

"@

    # Generate Case conditions
    for ($i = 0; $i -lt $count; $i++) {
        $item = $Items[$i]
        $prof = $item.profile

        $start = [int](($StartHour + $duration * $i) % 24)
        $end = [int](($StartHour + $duration * ($i + 1)) % 24)

        if ($start -eq 0) {
            # Starts at midnight (e.g., 0-3)
            $vbsContent += "    Case currentHour < $end`r`n"
        } elseif ($end -eq 0) {
            # Ends at midnight (e.g., 21-0)
            $vbsContent += "    Case currentHour >= $start`r`n"
        } elseif ($end -lt $start) {
            # Crosses midnight (e.g., 23-2)
            $vbsContent += "    Case currentHour >= $start Or currentHour < $end`r`n"
        } else {
            # Normal range (e.g., 6-9)
            $vbsContent += "    Case currentHour >= $start And currentHour < $end`r`n"
        }
        $vbsContent += "        profile = `"$prof`"`r`n"
    }

    $vbsContent += @"
End Select

' Run OpenRGB (hidden)
WshShell.Run """$OpenRGBPath"" -p """ & profile & """", 0
WScript.Quit
"@

    return $vbsContent
}

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

# Generate autoprofile.vbs (with retry logic for Task Scheduler)
Write-Host "Generating autoprofile.vbs..." -ForegroundColor Yellow

$autoprofileVbsPath = Join-Path $generatedPath "autoprofile.vbs"
$autoprofileVbsContent = New-AutoprofileVbs -Items $config.schedules.items -StartHour $config.schedules.startHour -OpenRGBPath $openRGBPath
$autoprofileVbsContent | Out-File -FilePath $autoprofileVbsPath -Encoding ASCII
Write-Host "Created: generated/autoprofile.vbs" -ForegroundColor Green

# Generate autoprofile.bat (kept for manual use)
Write-Host "Generating autoprofile.bat..." -ForegroundColor Yellow

$autoprofileContent = New-TimeBatContent -Items $config.schedules.items -StartHour $config.schedules.startHour -OpenRGBPath $openRGBPath
$autoprofileContent | Out-File -FilePath $autoprofilePath -Encoding ASCII
Write-Host "Created: generated/autoprofile.bat" -ForegroundColor Green

# Generate autorainbow.bat
Write-Host "Generating autorainbow.bat..." -ForegroundColor Yellow

$autorainbowContent = New-TimeBatContent -Items $config.rainbow.items -StartHour $config.rainbow.startHour -OpenRGBPath $openRGBPath
$autorainbowContent | Out-File -FilePath $autorainbowPath -Encoding ASCII
Write-Host "Created: generated/autorainbow.bat" -ForegroundColor Green
