@echo off
title Stop OTA Demo Services

echo Stopping OTA demo services...

echo.
echo Checking port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Found backend PID %%a
    taskkill /PID %%a /F
)

echo.
echo Checking port 8501...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501') do (
    echo Found Streamlit PID %%a
    taskkill /PID %%a /F
)

echo.
echo Checking Mosquitto service...
sc query mosquitto

echo.
echo If Mosquitto is running and Access Denied appears,
echo run this file as Administrator or stop it manually:
echo     Stop-Service Mosquitto

echo.
echo Cleanup attempt complete.
pause