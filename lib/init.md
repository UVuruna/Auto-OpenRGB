# init.ps1

**Script:** [init.ps1 (script)](init.ps1)

## Purpose

Environment initialization before generating files. First script that `setup.ps1` calls.

## Dependencies

- Must be run as Administrator
- `config.json` must exist in root folder

## What It Does

1. **Admin Check** - Checks if running as Administrator, exits if not
2. **Define Variables** - Defines global paths (`$scriptDir`, `$configPath`, etc.)
3. **Create Folders** - Creates `generated/`, `cycle/` and `rainbow/` if they don't exist
4. **Load Config** - Loads `config.json` into `$config` variable
5. **Cleanup** - Deletes all existing OpenRGB tasks from Task Scheduler

## Global Variables Set

```powershell
$script:scriptDir        # Project root folder
$script:configPath       # config.json path
$script:generatedPath    # generated/ folder
$script:cyclePath        # cycle/ folder
$script:rainbowPath      # rainbow/ folder
$script:config           # Loaded JSON
$script:openRGBPath      # OpenRGB.exe path
```

## Error Handling

- If not admin → red message + exit 1
- If config.json doesn't exist → PowerShell error (not explicitly handled)
