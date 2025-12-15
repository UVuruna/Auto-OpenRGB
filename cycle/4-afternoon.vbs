Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Program Files\OpenRGB\OpenRGB.exe"" --client -p ""4-yellow""", 0
WScript.Quit
