# generate-vbs.ps1

**Script:** [generate-vbs.ps1 (script)](generate-vbs.ps1)

## Purpose

Generiše sve VBS fajlove za pokretanje OpenRGB profila.

## Dependencies

- `$config` mora biti učitan (init.ps1)
- `$openRGBPath`, `$cyclePath`, `$rainbowPath` moraju biti definisani (init.ps1)

## What It Does

1. **OpenRGB-Server.vbs** - Kreira u Windows Startup folderu
2. **Cycle VBS** - Generiše VBS za schedules + extras u `cycle/` folderu
3. **Rainbow VBS** - Generiše VBS za rainbow profile u `rainbow/` folderu

## Generated Files

### OpenRGB-Server.vbs (Startup folder)

```vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\...\OpenRGB.exe"" --server --startminimized", 0
WScript.Quit
```

Pokreće OpenRGB server pri startu Windows-a (skriven, bez prozora).

### cycle/*.vbs

```vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\...\OpenRGB.exe"" -p ""1-blue""", 0
WScript.Quit
```

Generiše se za svaki:
- `config.schedules[].vbsName`
- `config.extras[].vbsName`

### rainbow/*.vbs

Ista struktura kao cycle, generiše se za svaki `config.rainbow[].vbsName`.

## VBS Syntax Notes

- `"""` = escaped quote u VBS stringu
- `", 0` na kraju = pokreni skriveno (bez CMD prozora)
- `WScript.Quit` = izlazi iz skripte nakon pokretanja
