from datetime import datetime

import threading

import serial

from MQTT.sender import Sender
from database.databaseAPI import DatabaseAPI
from model.acquisition import SensorValues
from tools.caster import Caster
from tools.staticvar import SERIAL_PORTNAME, NOTIFICATION_ERROR_DELAY, EC_ERROR_MIN, EC_ERROR_MAX, AH_ERROR_MIN, \
    AT_ERROR_MIN, GH_ERROR_MIN, GT_ERROR_MIN, WF_ERROR_MIN, WF_ERROR_MAX, GT_ERROR_MAX, GH_ERROR_MAX, AT_ERROR_MAX, \
    AH_ERROR_MAX, EC_THRESHOLD_MIN, EC_THRESHOLD_MAX, WF_THRESHOLD_MIN, WF_THRESHOLD_MAX, GT_THRESHOLD_MIN, \
    GT_THRESHOLD_MAX, GH_THRESHOLD_MIN, GH_THRESHOLD_MAX, AT_THRESHOLD_MIN, AT_THRESHOLD_MAX, AH_THRESHOLD_MIN, \
    AH_THRESHOLD_MAX, NOTIFICATION_ADVISE_DELAY, TELEGRAM_USERS
from userinterface.telegrambot import TelegramBot


class Bridge:

    def __init__(self):
        self.inbuffer = []
        self.ser = serial.Serial(SERIAL_PORTNAME, 9600, timeout=0)
        self.db = DatabaseAPI()
        self.db.connect()
        self.acquisition = None
        self.tbot = None
        self.tupdater = None
        self.start_error = None
        self.start_advise = None
        self.run_threads()

    def run_threads(self):
        t1 = threading.Thread(target=self.telegram)
        t1.start()
        t1.join()
        t2 = threading.Thread(target=self.loop())
        t2.start()
        t2.join()

    def telegram(self):
        self.tbot = TelegramBot()
        self.tupdater = self.tbot.startBot()
        # idle (blocking)
        # self.tupdater.idle()

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
                        # print("\nValue received")
                        # print(self.inbuffer)
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
        if numval is not None:
            sensorvalues = SensorValues()
            sender = Sender()
            for i in range(numval):
                if len(self.inbuffer) >= i * 2 + 5:
                    val = int.from_bytes(b"".join([self.inbuffer[i * 2 + 4], self.inbuffer[i * 2 + 5]]),
                                         byteorder='big')
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

            # sensorvalues.tostring()
            c = Caster(sensorvalues)
            self.acquisition = c.casting()
            self.error_control(self.acquisition)
            self.db.insertacquisition(self.acquisition)
            acquisitions = self.db.get_acquisitions(self.acquisition.datetime)
            sender.send(acquisitions)
            # acquisition.tostring()

    def error_control(self, acquisition):
        wrongmeasures = []
        unusualmeasures_key = []
        unusualmeasures_value = {}
        if acquisition.EC is None or acquisition.EC < EC_ERROR_MIN or acquisition.EC > EC_ERROR_MAX:
            wrongmeasures.append("EC")
        else:
            if acquisition.EC < EC_THRESHOLD_MIN or acquisition.EC > EC_THRESHOLD_MAX:
                unusualmeasures_key.append("EC")
                unusualmeasures_value["EC"] = round(acquisition.EC, 2)
        if acquisition.WF is None or acquisition.WF < WF_ERROR_MIN or acquisition.WF > WF_ERROR_MAX:
            wrongmeasures.append("WF")
        else:
            if acquisition.WF < WF_THRESHOLD_MIN or acquisition.WF > WF_THRESHOLD_MAX:
                unusualmeasures_key.append("WF")
                unusualmeasures_value["WF"] = round(acquisition.WF, 2)
        if acquisition.GT is None or acquisition.GT < GT_ERROR_MIN or acquisition.GT > GT_ERROR_MAX:
            wrongmeasures.append("GT")
        else:
            if acquisition.GT < GT_THRESHOLD_MIN or acquisition.GT > GT_THRESHOLD_MAX:
                unusualmeasures_key.append("GT")
                unusualmeasures_value["GT"] = round(acquisition.GT, 2)
        if acquisition.GH is None or acquisition.GH < GH_ERROR_MIN or acquisition.GH > GH_ERROR_MAX:
            wrongmeasures.append("GH")
        else:
            if acquisition.GH < GH_THRESHOLD_MIN or acquisition.GH > GH_THRESHOLD_MAX:
                unusualmeasures_key.append("GH")
                unusualmeasures_value["GH"] = round(acquisition.GH, 2)
        if acquisition.AT is None or acquisition.AT < AT_ERROR_MIN or acquisition.AT > AT_ERROR_MAX:
            wrongmeasures.append("AT")
        else:
            if acquisition.AT < AT_THRESHOLD_MIN or acquisition.AT > AT_THRESHOLD_MAX:
                unusualmeasures_key.append("AT")
                unusualmeasures_value["AT"] = round(acquisition.AT, 2)
        if acquisition.AH is None or acquisition.AH < AH_ERROR_MIN or acquisition.AH > AH_ERROR_MAX:
            wrongmeasures.append("AH")
        else:
            if acquisition.AH < AH_THRESHOLD_MIN or acquisition.AH > AH_THRESHOLD_MAX:
                unusualmeasures_key.append("AH")
                unusualmeasures_value["AH"] = round(acquisition.AH, 2)

        if len(wrongmeasures) > 0:
            if self.start_error is None:
                self.start_error = acquisition.datetime
                error_msg = error_msg_generator(wrongmeasures, acquisition.acquisition_point, acquisition.datetime)
                sendBotMessage(self.tupdater, error_msg)
            else:
                if isinstance(self.start_error, datetime):
                    lastNotification = acquisition.datetime - self.start_error
                    if lastNotification.total_seconds() > NOTIFICATION_ERROR_DELAY:
                        self.start_error = acquisition.datetime
                        error_msg = error_msg_generator(wrongmeasures, acquisition.acquisition_point,
                                                        acquisition.datetime)
                        sendBotMessage(self.tupdater, error_msg)
        else:
            self.start_error = None

        if len(unusualmeasures_key) > 0 and len(unusualmeasures_value) > 0:
            if self.start_advise is None:
                self.start_advise = acquisition.datetime
                advise_msg = advise_msg_generator(unusualmeasures_key, unusualmeasures_value,
                                                  acquisition.acquisition_point, acquisition.datetime)
                sendBotMessage(self.tupdater, advise_msg)
            else:
                if isinstance(self.start_advise, datetime):
                    lastNotification = acquisition.datetime - self.start_advise
                    if lastNotification.total_seconds() > NOTIFICATION_ADVISE_DELAY:
                        self.start_advise = acquisition.datetime
                        advise_msg = advise_msg_generator(unusualmeasures_key, unusualmeasures_value,
                                                          acquisition.acquisition_point,
                                                          acquisition.datetime)
                        sendBotMessage(self.tupdater, advise_msg)
        else:
            self.start_advise = None


def advise_msg_generator(unusualmeasures_key, unusualmeasures_value, acquisition_point, datetime):
    advise_msg = "----------------------------------------------------------------\n"
    advise_msg += "      AVVISO SUPERAMENTO SOGLIE           \n"
    advise_msg += "----------------------------------------------------------------\n"
    advise_msg += "Punto di raccolta   | " + str(acquisition_point) + "\n"
    advise_msg += "Data                         | " + str(datetime.date().strftime("%d/%m/%Y")) + "\n"
    advise_msg += "Ora                           | " + str(datetime.time().strftime("%H:%M:%S")) + "\n"
    advise_msg += "----------------------------------------------------------------\n"
    advise_msg += "                           SENSORI               \n"
    advise_msg += "----------------------------------------------------------------\n"
    for unusualmeasure in unusualmeasures_key:
        if unusualmeasure == "EC":
            advise_msg += "Conducibilità elettica  | " + str(unusualmeasures_value[unusualmeasure]) + " us/cm \n"
        if unusualmeasure == "WF":
            advise_msg += "Flusso Acqua di Sgrondo | " + str(unusualmeasures_value[unusualmeasure]) + " L/min \n"
        if unusualmeasure == "GT":
            advise_msg += "Temperatura del Terreno | " + str(unusualmeasures_value[unusualmeasure]) + " °C \n"
        if unusualmeasure == "GH":
            advise_msg += "Umidità del Terreno     | " + str(unusualmeasures_value[unusualmeasure]) + " % \n"
        if unusualmeasure == "AT":
            advise_msg += "Temperatura dell'Aria   | " + str(unusualmeasures_value[unusualmeasure]) + " °C \n"
        if unusualmeasure == "AH":
            advise_msg += "Umidità dell'Aria | " + str(unusualmeasures_value[unusualmeasure]) + " % \n"
    advise_msg += "----------------------------------------------------------------\n"
    return advise_msg


def error_msg_generator(wrongmeasures, acquisition_point, datetime):
    error_msg = "----------------------------------------------------------------\n"
    error_msg += "                    NOTIFICA ERRORE           \n"
    error_msg += "----------------------------------------------------------------\n"
    error_msg += "Punto di raccolta   | " + str(acquisition_point) + "\n"
    error_msg += "Data                         | " + str(datetime.date().strftime("%d/%m/%Y")) + "\n"
    error_msg += "Ora                           | " + str(datetime.time().strftime("%H:%M:%S")) + "\n"
    error_msg += "----------------------------------------------------------------\n"
    error_msg += "                           SENSORI               \n"
    error_msg += "----------------------------------------------------------------\n"
    for wrongmeasure in wrongmeasures:
        if wrongmeasure == "EC":
            error_msg += "> Conducibilità elettica \n"
        if wrongmeasure == "WF":
            error_msg += "> Flusso Acqua di Sgrondo \n"
        if wrongmeasure == "GT":
            error_msg += "> Temperatura del Terreno \n"
        if wrongmeasure == "GH":
            error_msg += "> Umidità del Terreno \n"
        if wrongmeasure == "AT":
            error_msg += "> Temperatura dell'Aria \n"
        if wrongmeasure == "AH":
            error_msg += "> Umidità dell'Aria \n"
    error_msg += "----------------------------------------------------------------\n"
    error_msg += "Controllare che i sensori funzionino correttamente. \n"

    return error_msg


def sendBotMessage(tupdater, msg):
    if tupdater is not None and msg is not None:
        for chatID in TELEGRAM_USERS:
            tupdater.bot.send_message(chat_id=chatID, text=msg)
    else:
        if tupdater is None:
            print("tupdater is none")
        if msg is None:
            print("msg is none")
