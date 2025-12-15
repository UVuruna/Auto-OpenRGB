# cycle/

VBS skripte za dnevne RGB profile i extras.

## Purpose

Sadrži VBS fajlove koje korisnik može pokrenuti ručno (double-click ili keyboard shortcut) za promenu RGB profila.

## Contents

Fajlovi se auto-generišu iz `config.json` kada se pokrene `setup.ps1`:

### Dnevni profili (iz `schedules`)

| Fajl | Profil | Vreme |
|------|--------|-------|
| 1-dawn.vbs | 1-blue | 05:00 |
| 2-morning.vbs | 2-cyan | 08:00 |
| 3-noon.vbs | 3-green | 11:00 |
| 4-afternoon.vbs | 4-yellow | 14:00 |
| 5-evening.vbs | 5-orange | 17:00 |
| 6-dusk.vbs | 6-red | 20:00 |
| 7-midnight.vbs | 7-magenta | 23:00 |
| 8-night.vbs | 8-purple | 03:00 |

### Extras (iz `extras`)

| Fajl | Profil |
|------|--------|
| light.vbs | 9-white |
| dark.vbs | 0-black |

## Usage

1. **Double-click** - Pokreće profil direktno
2. **Keyboard shortcut** - Dodeli shortcut u Windows-u ili trećem programu

## File Format

Svi VBS fajlovi imaju istu strukturu:

```vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Program Files\OpenRGB\OpenRGB.exe"" -p ""profile-name""", 0
WScript.Quit
```

## Notes

- Fajlovi se NE edituju ručno - edituj `config.json` pa pokreni `setup.ps1`
- Ako je OpenRGB server aktivan → instant promena
- Ako server nije aktivan → 2-3 sec delay (OpenRGB se pokreće)
