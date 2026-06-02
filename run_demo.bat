@echo off
title OTA Validation Demo Launcher

echo Starting OTA Validation & Monitoring Demo...

cd /d C:\projects\automotive\ota-validation-monitoring

echo Activating virtual environment...
call .venv\Scripts\activate

echo Starting FastAPI Backend...
start "OTA Backend API" cmd /k "cd /d C:\projects\automotive\ota-validation-monitoring && call .venv\Scripts\activate && uvicorn backend.main:app --reload"

timeout /t 3

echo Starting Streamlit Dashboard...
start "OTA Dashboard" cmd /k "cd /d C:\projects\automotive\ota-validation-monitoring && call .venv\Scripts\activate && streamlit run dashboard/app.py"

echo Demo started.
echo Backend: http://127.0.0.1:8000/docs
echo Dashboard: http://localhost:8501

pause