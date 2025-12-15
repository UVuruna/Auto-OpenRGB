# rainbow/

VBS skripte za rainbow (unicolor) RGB profile.

## Purpose

Sadrži VBS fajlove za rainbow profile - jednobojni profili za brzi pristup preko tastature (F1-F12).

## Contents

Fajlovi se auto-generišu iz `config.json` (`rainbow` sekcija) kada se pokrene `setup.ps1`:

| Fajl | Profil | Boja |
|------|--------|------|
| F1.vbs | UC-01-00F | Plava |
| F2.vbs | UC-02-08F | Plavo-ljubičasta |
| F3.vbs | UC-03-0FF | Cyan |
| F4.vbs | UC-04-0F8 | Cyan-zelena |
| F5.vbs | UC-05-0F0 | Zelena |
| F6.vbs | UC-06-8F0 | Žuto-zelena |
| F7.vbs | UC-07-FF0 | Žuta |
| F8.vbs | UC-08-F80 | Narandžasta |
| F9.vbs | UC-08-F00 | Crvena |
| F10.vbs | UC-10-F08 | Crveno-ružičasta |
| F11.vbs | UC-11-F0F | Magenta |
| F12.vbs | UC-12-80F | Ljubičasta |

## Usage

Namenjeno za keyboard shortcuts:
- Dodeli svaki VBS na odgovarajući F-key
- Koristi program kao AutoHotkey ili Windows shortcut

## File Format

Svi VBS fajlovi imaju istu strukturu:

```vbs
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Program Files\OpenRGB\OpenRGB.exe"" -p ""UC-01-00F""", 0
WScript.Quit
```

## Notes

- Profili moraju postojati u OpenRGB pre korišćenja
- Imena profila (UC-XX-XXX) su hex kodovi boja
- Fajlovi se NE edituju ručno - edituj `config.json` pa pokreni `setup.ps1`
