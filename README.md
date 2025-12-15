# OpenRGB Schedule - Instrukcije

## Kako radi

OpenRGB server se pokreće automatski pri startu Windows-a (u pozadini, bez prozora). Sve promene boja idu preko `--client` moda što je **instant** (bez delay-a).

## Struktura fajlova

```
U:\Coding\PC Gadgets\openRGB schedule\
├── config.json              <- JEDINI FAJL KOJI EDITIRAS
├── setup.ps1                <- Pokreni nakon promjena u config.json
├── lib\                     <- Helper skripte (ne edituj)
│   ├── init.ps1             <- Ucitavanje configa, kreiranje foldera
│   ├── generate-bat.ps1     <- Generisanje autoprofile.bat
│   ├── generate-vbs.ps1     <- Generisanje VBS fajlova
│   └── create-tasks.ps1     <- Kreiranje Task Scheduler taskova
├── autoprofile.bat          <- Auto-generisan, ne edituj
├── cycle\                   <- VBS za dnevne profile + extras
│   ├── 1-dawn.vbs
│   ├── 2-morning.vbs
│   ├── ...
│   ├── light.vbs
│   └── dark.vbs
└── rainbow\                 <- VBS za rainbow profile
    ├── F1.vbs
    ├── F2.vbs
    └── ...

Windows Startup folder:
├── OpenRGB-Server.vbs       <- Auto-generisan, pokrece server
```

## Pokretanje setup skripte

1. Desni klik na **Start** → **Terminal (Admin)**
2. Ukucaj:
   ```
   cd "U:\Coding\PC Gadgets\openRGB schedule"
   Set-ExecutionPolicy Bypass -Scope Process
   .\setup.ps1
   ```

Skripta automatski generise:
- Task Scheduler taskove (dnevni + autoprofile at logon)
- autoprofile.bat
- Sve VBS fajlove (cycle + rainbow folderi)
- OpenRGB-Server.vbs u Windows Startup folderu

## config.json format

```json
{
    "openRGBPath": "C:\\Program Files\\OpenRGB\\OpenRGB.exe",
    "schedules": [
        { "taskName": "OpenRGB zora", "vbsName": "1-dawn", "time": "05:00", "profile": "1-blue", "hourStart": 5, "hourEnd": 8 }
    ],
    "extras": [
        { "vbsName": "light", "profile": "8-white" }
    ],
    "rainbow": [
        { "vbsName": "F1", "profile": "UC-01-00F" }
    ]
}
```

### Polja:
- `taskName` - ime u Task Scheduler-u
- `vbsName` - ime VBS fajla (bez .vbs)
- `time` - kada se pokreće dnevni task (HH:MM)
- `profile` - ime profila u OpenRGB
- `hourStart` / `hourEnd` - za autoprofile.bat logiku

### hourStart / hourEnd primeri:
- `5-8` → normalno (05:00 - 08:00)
- `0-3` → počinje u ponoć (00:00 - 03:00)
- `20-0` → završava u ponoć (20:00 - 24:00)
- `23-2` → prelazi preko ponoći (23:00 - 02:00)

## Dodavanje novog profila

1. Napravi profil u OpenRGB i sačuvaj ga
2. Dodaj red u `config.json` (schedules, extras, ili rainbow)
3. Pokreni `.\setup.ps1`

## Brisanje / izmena profila

1. Edituj `config.json`
2. Pokreni `.\setup.ps1`

## Troubleshooting

### "Connection attempt failed" pri pokretanju VBS/BAT
OpenRGB server nije pokrenut. Proveri da li postoji `OpenRGB-Server.vbs` u Startup folderu (`Win+R` → `shell:startup`).

### Autoprofile daje pogrešnu boju
Odkomentariši debug linije u autoprofile.bat:
```bat
echo SAT JE: %hour%
pause
```
Proveri koji sat vraća i u koju granu ulazi.

### Server se ne pokreće pri startu
Ručno proveri da li `OpenRGB-Server.vbs` postoji u `shell:startup` i da li radi kada ga pokreneš double-click-om.
