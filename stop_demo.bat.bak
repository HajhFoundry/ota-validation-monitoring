@echo off
title Stop OTA Demo Services

echo Stopping OTA demo services...

echo.
echo Stopping Python processes using port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Killing PID %%a
    taskkill /PID %%a /F
)

echo.
echo Stopping Streamlit processes using port 8501...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501') do (
    echo Killing PID %%a
    taskkill /PID %%a /F
)

echo.
echo Stopping Mosquitto service...
net stop mosquitto

echo.
echo Cleanup complete.
pause