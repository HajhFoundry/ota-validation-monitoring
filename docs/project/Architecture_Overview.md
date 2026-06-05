# OTA Validation & Monitoring Platform – Architecture Overview

## Purpose

This project demonstrates an automotive OTA validation and monitoring workflow for connected vehicle systems.

It simulates how OTA campaigns are targeted, validated, executed, monitored, and reported across vehicle inventory, backend APIs, MQTT telemetry, dashboards, and automation tests.

## Architecture Diagram

```text
+-----------------------------+
| Streamlit Dashboard         |
| - Overview KPIs             |
| - Vehicle Inventory         |
| - Campaigns                 |
| - Manual Test Console       |
| - Live OTA Operations       |
+-------------+---------------+
              |
              v
+-----------------------------+
| FastAPI Backend             |
| - Vehicle APIs              |
| - Campaign APIs             |
| - OTA Status APIs           |
| - OTA Update APIs           |
+-------------+---------------+
              |
              v
+-----------------------------+
| OTA Validation Layer        |
| - Eligibility Rules         |
| - Safety Rules              |
| - Cybersecurity Rules       |
| - Configurable Rule File    |
+-------------+---------------+
              |
              v
+-----------------------------+
| OTA Execution Simulator     |
| - State Machine             |
| - Pause / Resume            |
| - Checkpoint Recovery       |
| - Notifications             |
+-------------+---------------+
              |
              v
+-----------------------------+
| MQTT Telemetry Layer        |
| - Mosquitto Broker          |
| - Publisher                 |
| - Subscriber                |
| - vehicle/{VIN}/ota/status |
+-------------+---------------+
              |
              v
+-----------------------------+
| Test Automation Layer       |
| - Pytest                    |
| - JSON Test Data            |
| - API Tests                 |
| - Regression Tests          |
+-----------------------------+