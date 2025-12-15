# OpenRGB Task Scheduler Auto-Setup
# Autor: UV
# Pokreni kao Administrator

$libPath = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "lib"

# 1. Inicijalizacija - ucitaj config, kreiraj foldere, obrisi stare taskove
. (Join-Path $libPath "init.ps1")

# 2. Generiši BAT fajlove (autoprofile.bat, autorainbow.bat)
. (Join-Path $libPath "generate-bat.ps1")

# 3. Generiši sve VBS fajlove (server, cycle, rainbow)
. (Join-Path $libPath "generate-vbs.ps1")

# 4. Kreiraj Task Scheduler taskove
. (Join-Path $libPath "create-tasks.ps1")

# Završna poruka
Write-Host "`n=== ZAVRSENO ===" -ForegroundColor Cyan
Write-Host "Ukupno taskova: $($config.schedules.items.Count + 1)" -ForegroundColor Cyan
Write-Host "Cycle VBS fajlova: $($config.schedules.items.Count + $config.extras.Count)" -ForegroundColor Cyan
Write-Host "Rainbow VBS fajlova: $($config.rainbow.items.Count)" -ForegroundColor Cyan
Write-Host "BAT fajlovi: generated/autoprofile.bat, generated/autorainbow.bat" -ForegroundColor Cyan
Write-Host "OpenRGB Server: $serverVbsPath" -ForegroundColor Cyan
Write-Host "`nNAPOMENA: Restartuj racunar da bi OpenRGB server krenuo automatski." -ForegroundColor Yellow
