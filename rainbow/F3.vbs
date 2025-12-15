Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Program Files\OpenRGB\OpenRGB.exe"" --client -p ""UC-03-0FF""", 0
WScript.Quit
