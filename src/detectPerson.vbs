Set oShell = CreateObject ("Wscript.Shell")
Dim strCMD
strCMD = "cmd cd /c D:\project_computer_vision\detectPerson\utils\detectPerson.bat"
oShell.Run strCMD, 0, false