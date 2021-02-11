import serial

from MQTT.sender import Sender
from database.databaseAPI import DatabaseAPI
from model.acquisition import SensorValues
from tools.caster import Caster

PORTNAME = 'COM3'


class Bridge:

    def __init__(self):
        self.inbuffer = []
        self.ser = serial.Serial(PORTNAME, 9600, timeout=0)
        self.db = DatabaseAPI()
        self.db.connect()
    def loop(self):
        # infinite loop
        try:
            secondlastchar = None
            while True:
                # look for a byte from serial

                if self.ser.in_waiting > 0:
                    # data available from the serial port
                    lastchar = self.ser.read(1)
                    self.inbuffer.append(lastchar)

                    if secondlastchar == b'\xff' and lastchar == b'\xfe':  # EOL
                        print("\nValue received")
                        print(self.inbuffer)
                        self.usedata()
                        self.inbuffer = []
                    else:
                        secondlastchar = lastchar
        except Exception as e:
            print("An exception occurred")
            print(e)
            self.db.closeconnection()

    def usedata(self):
        # I have received a line from the serial port. I can use it
        if len(self.inbuffer) < 6:  # at least header, size, footer
            return False
        # split parts
        if self.inbuffer[0] != b'\xff':
            return False

        numval = int.from_bytes(b"".join([self.inbuffer[2], self.inbuffer[3]]), byteorder='big')

        sensorvalues = SensorValues()
        sender = Sender()
        for i in range(numval):
            val = int.from_bytes(b"".join([self.inbuffer[i * 2 + 4], self.inbuffer[i * 2 + 5]]), byteorder='big')
            strval = "Sensor %d: %d " % (i, val)
            print(strval)
            if i == 0:
                sensorvalues.s0 = val
            if i == 1:
                sensorvalues.s1 = val
            if i == 2:
                sensorvalues.s2 = val
            if i == 3:
                sensorvalues.s3 = val
            if i == 4:
                sensorvalues.s4 = val
            if i == 5:
                sensorvalues.s5 = val

        #sensorvalues.tostring()
        c = Caster(sensorvalues)
        acquisition = c.casting()
        self.db.insertacquisition(acquisition)
        acquisitions = self.db.get_acquisitions(acquisition.datetime)
        sender.send(acquisitions)
        #acquisition.tostring()

