import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import config
import processing

broker = config.BROKER
port = config.PORT
topic = config.TOPIC
client_id = config.client_id


def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        #util_flusso.processing_message(msg.payload.decode())
        processing.processing_message(msg.payload.decode())

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    #client.loop_forever()  #per run senza thread


