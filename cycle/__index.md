# cycle/

VBS scripts for daily RGB profiles and extras.

## Purpose

Contains VBS files that users can run manually (double-click or keyboard shortcut) to change RGB profiles.

## Contents

Files are auto-generated from `config.json` when `setup.ps1` runs:

- **Daily profiles** - one VBS per `schedules.items` entry (format: `{vbsName}.vbs`)
- **Extras** - one VBS per `extras` entry (format: `{vbsName}.vbs`)

For current list of profiles, see [config.json](../config.json).

## Usage

1. **Double-click** - Runs the profile directly
2. **Keyboard shortcut** - Assign shortcut in Windows or third-party program

## File Format

All VBS files have the same structure:

```vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Program Files\OpenRGB\OpenRGB.exe"" -p ""profile-name""", 0
WScript.Quit
```

## Notes

- Files are NOT edited manually - edit `config.json` then run `setup.ps1`
- If OpenRGB server is running → instant change
- If server is not running → 2-3 sec delay (OpenRGB starts up)
