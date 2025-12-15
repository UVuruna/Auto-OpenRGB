# init.ps1 - Ucitaj config, kreiraj foldere, obrisi stare taskove

# Provera admin privilegija
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "GRESKA: Skripta mora biti pokrenuta kao Administrator!" -ForegroundColor Red
    Write-Host "Desni klik na Start -> Terminal (Admin)" -ForegroundColor Yellow
    exit 1
}

$script:scriptDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$script:configPath = Join-Path $scriptDir "config.json"
$script:generatedPath = Join-Path $scriptDir "generated"
$script:autoprofilePath = Join-Path $generatedPath "autoprofile.bat"
$script:autorainbowPath = Join-Path $generatedPath "autorainbow.bat"
$script:cyclePath = Join-Path $scriptDir "cycle"
$script:rainbowPath = Join-Path $scriptDir "rainbow"

# Kreiraj foldere ako ne postoje
if (-not (Test-Path $generatedPath)) {
    New-Item -ItemType Directory -Path $generatedPath | Out-Null
    Write-Host "Kreiran folder: generated" -ForegroundColor Green
}

if (-not (Test-Path $cyclePath)) {
    New-Item -ItemType Directory -Path $cyclePath | Out-Null
    Write-Host "Kreiran folder: cycle" -ForegroundColor Green
}

if (-not (Test-Path $rainbowPath)) {
    New-Item -ItemType Directory -Path $rainbowPath | Out-Null
    Write-Host "Kreiran folder: rainbow" -ForegroundColor Green
}

# Ucitaj JSON config
$script:config = Get-Content $configPath -Raw | ConvertFrom-Json
$script:openRGBPath = $config.openRGBPath

Write-Host "=== OpenRGB Setup ===" -ForegroundColor Cyan
Write-Host "Ucitavam konfiguraciju iz config.json..." -ForegroundColor Yellow

# Obrisi postojece OpenRGB taskove
Write-Host "Brisem postojece OpenRGB taskove..." -ForegroundColor Yellow
Get-ScheduledTask | Where-Object { $_.TaskName -like "OpenRGB*" } | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue
