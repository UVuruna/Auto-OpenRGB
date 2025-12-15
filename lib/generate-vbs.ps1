# generate-vbs.ps1 - Generiši sve VBS fajlove

# OpenRGB-Server.vbs u startup folderu
Write-Host "Kreiram OpenRGB-Server.vbs u Startup folderu..." -ForegroundColor Yellow

$startupPath = [Environment]::GetFolderPath('Startup')
$script:serverVbsPath = Join-Path $startupPath "OpenRGB-Server.vbs"

$serverVbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """$openRGBPath"" --server --startminimized", 0
WScript.Quit
"@

$serverVbsContent | Out-File -FilePath $serverVbsPath -Encoding ASCII
Write-Host "Kreiran: $serverVbsPath" -ForegroundColor Green

# VBS fajlovi za cycle profile
Write-Host "Generisem VBS fajlove u cycle folderu..." -ForegroundColor Yellow

foreach ($s in $config.schedules) {
    $vbsName = $s.vbsName + ".vbs"
    $vbsPath = Join-Path $cyclePath $vbsName
    $prof = $s.profile

    $vbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """$openRGBPath"" --client -p ""$prof""", 0
WScript.Quit
"@

    $vbsContent | Out-File -FilePath $vbsPath -Encoding ASCII
    Write-Host "Kreiran: cycle\$vbsName -> $prof" -ForegroundColor Green
}

foreach ($e in $config.extras) {
    $vbsName = $e.vbsName + ".vbs"
    $vbsPath = Join-Path $cyclePath $vbsName
    $prof = $e.profile

    $vbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """$openRGBPath"" --client -p ""$prof""", 0
WScript.Quit
"@

    $vbsContent | Out-File -FilePath $vbsPath -Encoding ASCII
    Write-Host "Kreiran: cycle\$vbsName -> $prof" -ForegroundColor Green
}

# VBS fajlovi za rainbow profile
Write-Host "Generisem VBS fajlove u rainbow folderu..." -ForegroundColor Yellow

foreach ($e in $config.rainbow) {
    $vbsName = $e.vbsName + ".vbs"
    $vbsPath = Join-Path $rainbowPath $vbsName
    $prof = $e.profile

    $vbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """$openRGBPath"" --client -p ""$prof""", 0
WScript.Quit
"@

    $vbsContent | Out-File -FilePath $vbsPath -Encoding ASCII
    Write-Host "Kreiran: rainbow\$vbsName -> $prof" -ForegroundColor Green
}
