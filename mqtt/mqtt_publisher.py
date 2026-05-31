import json
import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883


def publish_ota_status(vin, payload):
    topic = f"vehicle/{vin}/ota/status"

    client = mqtt.Client()
    client.connect(BROKER_HOST, BROKER_PORT, 60)

    client.publish(topic, json.dumps(payload))

    print(f"[MQTT PUBLISHED] Topic={topic} Payload={payload}")

    client.disconnect()