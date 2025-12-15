# rainbow/

VBS scripts for rainbow (unicolor) RGB profiles.

## Purpose

Contains VBS files for rainbow profiles - single-color profiles for quick keyboard access.

## Contents

Files are auto-generated from `config.json` (`rainbow.items` section) when `setup.ps1` runs:

- One VBS per `rainbow.items` entry (format: `{vbsName}.vbs`)

For current list of profiles, see [config.json](../config.json).

## Usage

Intended for keyboard shortcuts:
- Assign each VBS to a corresponding key
- Use a program like AutoHotkey or Windows shortcuts

There is also [autorainbow.bat](../generated/__index.md) for automatic time-based profile selection.

## File Format

All VBS files have the same structure:

```vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Program Files\OpenRGB\OpenRGB.exe"" -p ""profile-name""", 0
WScript.Quit
```

## Notes

- Profiles must exist in OpenRGB before use
- Files are NOT edited manually - edit `config.json` then run `setup.ps1`
- If OpenRGB server is running → instant change
- If server is not running → 2-3 sec delay (OpenRGB starts up)
