' Auto-generated file - do not edit manually!
' Edit config.json and run setup.ps1

Set WshShell = CreateObject("WScript.Shell")
' Get current hour
currentHour = Hour(Now)

' Determine profile based on hour
Select Case True
    Case currentHour >= 3 And currentHour < 5
        profile = "UC-01-00F"
    Case currentHour >= 5 And currentHour < 7
        profile = "UC-02-08F"
    Case currentHour >= 7 And currentHour < 9
        profile = "UC-03-0FF"
    Case currentHour >= 9 And currentHour < 11
        profile = "UC-04-0F8"
    Case currentHour >= 11 And currentHour < 13
        profile = "UC-05-0F0"
    Case currentHour >= 13 And currentHour < 15
        profile = "UC-06-8F0"
    Case currentHour >= 15 And currentHour < 17
        profile = "UC-07-FF0"
    Case currentHour >= 17 And currentHour < 19
        profile = "UC-08-F80"
    Case currentHour >= 19 And currentHour < 21
        profile = "UC-09-F00"
    Case currentHour >= 21 And currentHour < 23
        profile = "UC-10-F08"
    Case currentHour >= 23 Or currentHour < 1
        profile = "UC-11-F0F"
    Case currentHour >= 1 And currentHour < 3
        profile = "UC-12-80F"
End Select

' Run OpenRGB (hidden)
WshShell.Run """C:\Program Files\OpenRGB\OpenRGB.exe"" -p """ & profile & """", 0
WScript.Quit
