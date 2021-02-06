import serial

## configuration
PORTNAME = 'COM3'


class Bridge():

    def setup(self):
        # open serial port
        self.ser = serial.Serial(PORTNAME, 9600, timeout=0)
        # self.ser.open()

        # internal input buffer
        self.inbuffer = []

    def loop(self):
        # infinite loop
        secondLastchar = None
        while True:
            # look for a byte from serial

            if self.ser.in_waiting > 0:
                # data available from the serial port
                lastchar = self.ser.read(1)
                self.inbuffer.append(lastchar)

                if secondLastchar == b'\xff' and lastchar == b'\xfe':  # EOL
                    print("\nValue received")
                    print(self.inbuffer)
                    self.useData()
                    self.inbuffer = []
                else:
                    secondLastchar = lastchar

    def useData(self):
        # I have received a line from the serial port. I can use it
        if len(self.inbuffer) < 6:  # at least header, size, footer
            return False
        # split parts
        if self.inbuffer[0] != b'\xff':
            return False

        numval = int.from_bytes(b"".join([self.inbuffer[2], self.inbuffer[3]]), byteorder='big')

        print(numval)
        for i in range(numval):
            val = int.from_bytes(b"".join([self.inbuffer[i*2+4], self.inbuffer[i*2+5]]), byteorder='big')
            strval = "Sensor %d: %d " % (i, val)
            print(strval)
