import jsonpickle
from MQTT.encryption import Encryption
from model.message import Message
from MQTT.mqttClient import MQTTClient


class Sender:
    def __init__(self):
        self.acquisitions = None
        self.client = None
        self.encryption = None

    def JSONConverter(self, msg):
        aJSON = jsonpickle.encode(msg, unpicklable=False)
        #return json.dumps(aJSON)
        return(aJSON)

    def send(self, acquisitions):
        self.acquisitions = acquisitions
        if self.client is None:
            self.client = MQTTClient()
            self.client.connect_mqtt()
        if self.encryption is None:
            self.encryption = Encryption()

        for acquisition in acquisitions:
            message = Message(acquisition)
            jsonMessage = self.JSONConverter(message)
            self.client.publish(self.encryption.encrypt(jsonMessage))

