from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv311

from tools.staticvar import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC


class MQTTClient:
    def __init__(self):
        self.client = None

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client = mqtt_client.Client("", True, None, MQTTv311)
        # client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(MQTT_BROKER, MQTT_PORT)
        return self.client

    def publish(self, msg):
        result = self.client.publish(topic=MQTT_TOPIC, payload=msg, qos=0)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{MQTT_TOPIC}`")
        else:
            print(f"Failed to send message to topic {MQTT_TOPIC}")
        return status
