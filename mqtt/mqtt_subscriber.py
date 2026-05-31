import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "vehicle/+/ota/status"


def on_connect(client, userdata, flags, rc):
    print("[MQTT CONNECTED]")
    client.subscribe(TOPIC)


def on_message(client, userdata, message):
    print(f"[MQTT RECEIVED] Topic={message.topic}")
    print(f"Payload={message.payload.decode()}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT, 60)
client.loop_forever()