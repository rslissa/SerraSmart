import time

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
topic = "test"
# generate client ID with pub prefix randomly
client_id = "clientId-6L48NQ9LjJ"
username = 'test'
password = 'test'


class MQTTClient:
    def __init__(self):
        self.client = None

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client = mqtt_client.Client(client_id)
        # client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(broker, port)
        return self.client

    def publish(self, msg):
        result = self.client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        return status
