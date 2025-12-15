# Setup

**Script:** [setup.ps1](setup.ps1)

## Purpose

Main entry point for configuring the OpenRGB automatic system. Runs all necessary steps to set up the automatic RGB profile system.

## Dependencies

- PowerShell 5.1+
- Administrator privileges
- [config.json](config.json) - profile configuration
- [lib/](lib/__index.md) folder with helper scripts

## Usage

```powershell
# Run as Administrator
.\setup.ps1
```

## Workflow

1. **Initialization** ([init.ps1](lib/init.md))
   - Admin privilege check
   - Load config.json
   - Create folders (generated/, cycle/, rainbow/)
   - Delete old OpenRGB tasks

2. **Generate BAT files** ([generate-bat.ps1](lib/generate-bat.md))
   - autoprofile.bat - for daily profiles (Task Scheduler)
   - autorainbow.bat - for rainbow profiles (keyboard shortcut)

3. **Generate VBS files** ([generate-vbs.ps1](lib/generate-vbs.md))
   - OpenRGB-Server.vbs in Startup folder
   - VBS files in cycle/ for daily profiles
   - VBS files in rainbow/ for rainbow profiles

4. **Create Task Scheduler tasks** ([create-tasks.ps1](lib/create-tasks.md))
   - OpenRGB autoprofile (at logon)
   - Daily tasks per schedule from config.json

## Output

```
=== COMPLETED ===
Total tasks: 9
Cycle VBS files: 10
Rainbow VBS files: 12
BAT files: generated/autoprofile.bat, generated/autorainbow.bat
OpenRGB Server: [path to Startup folder]\OpenRGB-Server.vbs

NOTE: Restart computer for OpenRGB server to start automatically.
```
