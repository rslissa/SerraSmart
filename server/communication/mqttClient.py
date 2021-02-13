import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import main

broker = 'broker.mqttdashboard.com'
port = 1883
topic = "prst/test/fromweb1"
client_id = "Pasquale-receiver"


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
        main.processing_message(msg.payload.decode())

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

#
#
#
#
#
#
#
#
'''
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))


def on_message(client, userdata, message):
    #print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
    #print(message.payload)
    main.processing_message(message.payload.decode())


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, userdata, level, buf):
    print("Logging message: " + str(level) + " " + str(buf))


if __name__ == '__main__':

    client = mqtt.Client(client_id="Pasquale-receiver", clean_session=False, userdata=None, protocol=mqtt.MQTTv311,
                         transport="tcp")
    client.connect(host="broker.mqttdashboard.com", port=1883, keepalive=120, bind_address="")

    client.on_connect = on_connect
    client.on_message = on_message

    client.subscribe(topic="prst/test/fromweb1", qos=0)
    client.on_subscribe = on_subscribe

    client.loop_forever()
'''