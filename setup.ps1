# OpenRGB Task Scheduler Auto-Setup
# Author: UV
# Run as Administrator

$libPath = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "lib"

# 1. Initialization - load config, create folders, delete old tasks
. (Join-Path $libPath "init.ps1")

# 2. Generate BAT files (autoprofile.bat, autorainbow.bat)
. (Join-Path $libPath "generate-bat.ps1")

# 3. Generate all VBS files (server, cycle, rainbow)
. (Join-Path $libPath "generate-vbs.ps1")

# 4. Create Task Scheduler tasks
. (Join-Path $libPath "create-tasks.ps1")

# Final message
Write-Host "`n=== COMPLETED ===" -ForegroundColor Cyan
Write-Host "Total tasks: $($config.schedules.items.Count + 1)" -ForegroundColor Cyan
Write-Host "Cycle VBS files: $($config.schedules.items.Count + $config.extras.Count)" -ForegroundColor Cyan
Write-Host "Rainbow VBS files: $($config.rainbow.items.Count)" -ForegroundColor Cyan
Write-Host "BAT files: generated/autoprofile.bat, generated/autorainbow.bat" -ForegroundColor Cyan
Write-Host "OpenRGB Server: $serverVbsPath" -ForegroundColor Cyan
Write-Host "`nNOTE: Restart computer for OpenRGB server to start automatically." -ForegroundColor Yellow
