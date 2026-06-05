@echo off
title OTA Validation Automation Suite

echo ==========================================
echo OTA Validation Automation Test Suite
echo ==========================================
echo.

cd /d C:\projects\automotive\ota-validation-monitoring

call .venv\Scripts\activate

echo Running OTA regression suite...
echo.

python -m pytest -v

echo.
echo ==========================================
echo Test Execution Complete
echo ==========================================
pause