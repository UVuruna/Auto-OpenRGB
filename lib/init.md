# init.ps1

**Script:** [init.ps1 (script)](init.ps1)

## Purpose

Inicijalizacija okruženja pre generisanja fajlova. Prva skripta koju `setup.ps1` poziva.

## Dependencies

- Mora biti pokrenuta kao Administrator
- `config.json` mora postojati u root folderu

## What It Does

1. **Admin Check** - Proverava da li je pokrenuto kao Administrator, izlazi ako nije
2. **Define Variables** - Definiše globalne putanje (`$scriptDir`, `$configPath`, itd.)
3. **Create Folders** - Kreira `cycle/` i `rainbow/` ako ne postoje
4. **Load Config** - Učitava `config.json` u `$config` promenljivu
5. **Cleanup** - Briše sve postojeće OpenRGB taskove iz Task Scheduler-a

## Global Variables Set

```powershell
$script:scriptDir        # Root folder projekta
$script:configPath       # config.json putanja
$script:autoprofilePath  # autoprofile.bat putanja
$script:cyclePath        # cycle/ folder
$script:rainbowPath      # rainbow/ folder
$script:config           # Učitan JSON
$script:openRGBPath      # OpenRGB.exe putanja
```

## Error Handling

- Ako nije admin → crvena poruka + exit 1
- Ako config.json ne postoji → PowerShell greška (nije eksplicitno handlovano)
