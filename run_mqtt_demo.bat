@echo off
title OTA MQTT Demo Launcher

echo Starting OTA MQTT Telemetry Demo...

cd /d C:\projects\automotive\ota-validation-monitoring

echo Activating virtual environment...
call .venv\Scripts\activate

echo Starting Mosquitto service...
echo Make sure Mosquitto service is already running.
echo If needed, run PowerShell as Administrator and use: Start-Service Mosquitto

timeout /t 2

echo Starting MQTT Subscriber...
start "OTA MQTT Subscriber" cmd /k "cd /d C:\projects\automotive\ota-validation-monitoring && call .venv\Scripts\activate && python mqtt\mqtt_subscriber.py"

timeout /t 2

echo Running OTA Executor...
start "OTA Executor" cmd /k "cd /d C:\projects\automotive\ota-validation-monitoring && call .venv\Scripts\activate && python vehicle_client\ota_executor.py"

echo.
echo MQTT demo started.
echo Topic: vehicle/+/ota/status
echo Broker: localhost:1883
echo.
pause