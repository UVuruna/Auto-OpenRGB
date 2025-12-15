Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Program Files\OpenRGB\OpenRGB.exe"" --client -p ""UC-07-FF0""", 0
WScript.Quit
