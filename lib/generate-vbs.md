# generate-vbs.ps1

**Script:** [generate-vbs.ps1 (script)](generate-vbs.ps1)

## Purpose

Generates all VBS files for running OpenRGB profiles.

## Dependencies

- `$config` must be loaded (init.ps1)
- `$openRGBPath`, `$cyclePath`, `$rainbowPath` must be defined (init.ps1)

## What It Does

1. **OpenRGB-Server.vbs** - Creates in Windows Startup folder
2. **Cycle VBS** - Generates VBS for schedules + extras in `cycle/` folder
3. **Rainbow VBS** - Generates VBS for rainbow profiles in `rainbow/` folder

## Generated Files

### OpenRGB-Server.vbs (Startup folder)

```vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\...\OpenRGB.exe"" --server --startminimized", 0
WScript.Quit
```

Starts OpenRGB server at Windows startup (hidden, no window).

### cycle/*.vbs

```vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\...\OpenRGB.exe"" -p ""1-blue""", 0
WScript.Quit
```

Generated for each:
- `config.schedules.items[].vbsName`
- `config.extras[].vbsName`

### rainbow/*.vbs

Same structure as cycle, generated for each `config.rainbow.items[].vbsName`.

## VBS Syntax Notes

- `"""` = escaped quote in VBS string
- `", 0` at end = run hidden (no CMD window)
- `WScript.Quit` = exits script after launching
