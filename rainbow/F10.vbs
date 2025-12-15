Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Program Files\OpenRGB\OpenRGB.exe"" --client -p ""UC-10-F08""", 0
WScript.Quit
