# OTA Validation & Monitoring Simulator

## Objective

Simulate an automotive OTA update workflow including:

- OTA Campaign Management
- Vehicle Update Eligibility
- Download Validation
- Installation Monitoring
- Rollback Handling
- MQTT Telemetry
- Dashboard Monitoring
- Automated Validation Testing

## Components

### OTA Backend
FastAPI-based OTA campaign server.

### Vehicle Client
Python OTA state machine simulator.

### MQTT Broker
Vehicle telemetry communication layer.

### Monitoring Dashboard
Streamlit monitoring portal.

### Test Automation
Pytest-based OTA validation suite.

## Future Enhancements

- AWS IoT Core
- Docker deployment
- GitHub Actions CI/CD
- Multi-vehicle simulation