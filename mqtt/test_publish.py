from mqtt_publisher import publish_ota_status

publish_ota_status(
    "VIN001",
    {
        "state": "DOWNLOADING",
        "progress": 50
    }
)