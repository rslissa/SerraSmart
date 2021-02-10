import paho.mqtt.client as paho
import time
import random


def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
#rc = 0 => connessione avvenuta con successo


def on_publish(client, userdata, mid):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
    print('client', client)
    print(('userdata', userdata))


def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print('Questo è il messaggio\n', msg)
    print('topic', msg.topic)
    print('payload', msg.payload)
    print('qos', msg.qos)
    print('retain', msg.retain)



if __name__ == '__main__':
    #publishing
    '''client = paho.Client()
    client.on_publish = on_publish
    client.connect("broker.mqttdashboard.com", 1883)
    client.loop_start()

    while True:
        temperature = random.randint(0, 50)
        (rc, mid) = client.publish("serratest/temp", str(temperature), qos=1)
        time.sleep(5)'''

    #subscribing
    client = paho.Client(userdata="12345")
    client.username_pw_set("paky", "paky")
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect("broker.mqttdashboard.com", 1883)
    client.subscribe("serratest/temp", qos=1)

    client.loop_forever()
