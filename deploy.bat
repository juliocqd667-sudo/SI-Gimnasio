@echo off
title NovaFit - Despliegue a Produccion
echo ===================================================
echo   NovaFit Premium - Publicacion en Produccion
echo ===================================================
echo.

:: Verificar si hay cambios
echo [+] Comprobando estado de Git...
git status -s

echo.
echo ===================================================
echo   Esto realizara un commit de todos tus cambios
echo   y los subira a la rama 'produccion' en GitHub.
echo ===================================================
echo.

:: Solicitar mensaje de commit
set /p commit_msg="Introduce el mensaje del commit (presiona Enter para 'Actualizacion automatica'): "
if "%commit_msg%"=="" set commit_msg=Actualizacion automatica

echo.
echo [+] Añadiendo cambios a Git...
git add .

echo [+] Creando commit...
git commit -m "Auto-deploy: %commit_msg%"

echo [+] Enviando cambios a la rama remota 'produccion'...
git push origin HEAD:produccion

echo.
echo ===================================================
echo   [ OK ] ¡Cambios subidos a la rama 'produccion'!
echo   El servidor Render.com comenzara a compilar y
echo   actualizar la aplicacion en vivo de forma automatica.
echo ===================================================
echo.
pause
