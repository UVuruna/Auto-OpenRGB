# init.ps1 - Load config, create folders, delete old tasks

# Check admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: Script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click Start -> Terminal (Admin)" -ForegroundColor Yellow
    exit 1
}

$script:scriptDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$script:configPath = Join-Path $scriptDir "config.json"
$script:generatedPath = Join-Path $scriptDir "generated"
$script:cyclePath = Join-Path $scriptDir "cycle"
$script:rainbowPath = Join-Path $scriptDir "rainbow"

# Create folders if they don't exist
if (-not (Test-Path $generatedPath)) {
    New-Item -ItemType Directory -Path $generatedPath | Out-Null
    Write-Host "Created folder: generated" -ForegroundColor Green
}

if (-not (Test-Path $cyclePath)) {
    New-Item -ItemType Directory -Path $cyclePath | Out-Null
    Write-Host "Created folder: cycle" -ForegroundColor Green
}

if (-not (Test-Path $rainbowPath)) {
    New-Item -ItemType Directory -Path $rainbowPath | Out-Null
    Write-Host "Created folder: rainbow" -ForegroundColor Green
}

# Load JSON config
$script:config = Get-Content $configPath -Raw | ConvertFrom-Json
$script:openRGBPath = $config.openRGBPath

Write-Host "=== OpenRGB Setup ===" -ForegroundColor Cyan
Write-Host "Loading configuration from config.json..." -ForegroundColor Yellow

# Delete existing OpenRGB tasks
Write-Host "Deleting existing OpenRGB tasks..." -ForegroundColor Yellow
Get-ScheduledTask | Where-Object { $_.TaskName -like "OpenRGB*" } | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue
