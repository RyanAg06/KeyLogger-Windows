Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c inyectar.bat"
oShell.Run strArgs, 0, false