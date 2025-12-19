' Auto-generated file - do not edit manually!
' Edit config.json and run setup.ps1

Set WshShell = CreateObject("WScript.Shell")
Set objWMI = GetObject("winmgmts:\\.\root\cimv2")

' Wait for OpenRGB server (max 60 sec)
retries = 0
Do While retries < 30
    Set colProcesses = objWMI.ExecQuery("SELECT * FROM Win32_Process WHERE Name = 'OpenRGB.exe'")
    If colProcesses.Count > 0 Then Exit Do
    WScript.Sleep 2000
    retries = retries + 1
Loop

If retries >= 30 Then WScript.Quit
' Get current hour
currentHour = Hour(Now)

' Determine profile based on hour
Select Case True
    Case currentHour >= 3 And currentHour < 6
        profile = "1-blue"
    Case currentHour >= 6 And currentHour < 9
        profile = "2-cyan"
    Case currentHour >= 9 And currentHour < 12
        profile = "3-green"
    Case currentHour >= 12 And currentHour < 15
        profile = "4-yellow"
    Case currentHour >= 15 And currentHour < 18
        profile = "5-orange"
    Case currentHour >= 18 And currentHour < 21
        profile = "6-red"
    Case currentHour >= 21
        profile = "7-magenta"
    Case currentHour < 3
        profile = "8-purple"
End Select

' Run OpenRGB (hidden)
WshShell.Run """C:\Program Files\OpenRGB\OpenRGB.exe"" -p """ & profile & """", 0
WScript.Quit
