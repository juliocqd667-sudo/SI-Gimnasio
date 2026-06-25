@echo off
title NovaFit - Local Development Launcher
echo ===================================================
echo   NovaFit Premium - Iniciando Entorno Local
echo ===================================================
echo.

:: 1. Iniciar el Backend Django
echo [+] Iniciando backend Django en segundo plano (puerto 8000)...
if exist "backend\venv\Scripts\python.exe" (
    start "NovaFit Backend (Django)" cmd /k "echo Iniciando Backend Django... && cd backend && venv\Scripts\activate && python manage.py runserver"
) else (
    start "NovaFit Backend (Django)" cmd /k "echo [!] Advertencia: No se encontro venv local, intentando con python global... && cd backend && python manage.py runserver"
)

:: 2. Iniciar el Frontend Vue 3 (Vite)
echo [+] Iniciando frontend Vue 3 en segundo plano (puerto 5173)...
start "NovaFit Frontend (Vite/Vue)" cmd /k "echo Iniciando Frontend Vue/Vite... && cd frontend && npm run dev"

echo.
echo ===================================================
echo   Servidores locales listos en ventanas separadas:
echo     - Backend API: http://127.0.0.1:8000/api/
echo     - Frontend Web: http://localhost:5173/
echo ===================================================
echo.
pause
