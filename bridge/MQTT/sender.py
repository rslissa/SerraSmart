import json

import jsonpickle

from model.message import Message
from MQTT.integrity import Integrity
from MQTT.mqttClient import MQTTClient


class Sender:
    def __init__(self):
        self.acquisitions = None
        self.client = None
        self.integrity = None

    def JSONConverter(self, msg):
        aJSON = jsonpickle.encode(msg, unpicklable=False)
        #return json.dumps(aJSON)
        return(aJSON)

    def send(self, acquisitions):
        self.acquisitions = acquisitions
        if self.client is None:
            self.client = MQTTClient()
            self.client.connect_mqtt()
        if self.integrity is None:
            self.integrity = Integrity()

        for acquisition in acquisitions:
            message = Message(self.integrity.get_digest(acquisition), acquisition)
            jsonMessage = self.JSONConverter(message)
            self.client.publish(jsonMessage)

