@echo off
setlocal enableextensions

:restart
cls
echo Starting JuFireX Backend and Frontend Services...
echo.

echo Starting Backend Flask Server (Port 5000)...
start "JuFireX Backend" cmd /k "cd /d f:\Code Projects\JuFireX && .venv\Scripts\activate && cd backend && python app.py"

echo Starting Frontend Dev Server (Port 5173)...
start "JuFireX Frontend" cmd /k "cd /d f:\Code Projects\JuFireX\frontend && npm run dev"

echo.
echo Services are starting...
echo Backend will be available at: http://localhost:5000
echo Frontend will be available at: http://localhost:5173
echo.
echo Press any key to restart services...
pause > nul

echo.
echo Closing existing services to restart...
rem Kill previously started windows by title
taskkill /FI "WINDOWTITLE eq JuFireX Backend" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq JuFireX Frontend" /T /F >nul 2>&1

timeout /t 1 >nul

goto :restart