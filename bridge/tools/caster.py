from datetime import datetime

from model.acquisition import Acquisition
from tools.staticvar import ANALOG_MIN, ACQUISITION_POINT, AH_MAX, ANALOG_MAX, AH_MIN, AT_MIN, AT_MAX, GH_MIN, GH_MAX, \
    GT_MIN, GT_MAX, WF_MIN, WF_MAX, EC_MIN, EC_MAX


class Caster:
    # sensor0 -> EC sensor
    # sensor1 -> WaterFlow sensor
    # sensor2 -> GroundTemperature sensor
    # sensor3 -> GroundHumidity sensor
    # sensor4 -> AirTemperature sensor
    # sensor5 -> AirHumidity sensor
    def __init__(self, sensorvalues):
        self.s0 = sensorvalues.s0
        self.s1 = sensorvalues.s1
        self.s2 = sensorvalues.s2
        self.s3 = sensorvalues.s3
        self.s4 = sensorvalues.s4
        self.s5 = sensorvalues.s5

    def casting(self):
        if self.s0 is not None:
            _EC = (((self.s0 - ANALOG_MIN) * (EC_MAX - EC_MIN)) / (ANALOG_MAX - ANALOG_MIN)) + EC_MIN
        else:
            _EC = None
        if self.s1 is not None:
            _WF = (((self.s1 - ANALOG_MIN) * (WF_MAX - WF_MIN)) / (ANALOG_MAX - ANALOG_MIN)) + WF_MIN
        else:
            _WF = None
        if self.s2 is not None:
            _GT = (((self.s2 - ANALOG_MIN) * (GT_MAX - GT_MIN)) / (ANALOG_MAX - ANALOG_MIN)) + GT_MIN
        else:
            _GT = None
        if self.s3 is not None:
            _GH = (((self.s3 - ANALOG_MIN) * (GH_MAX - GH_MIN)) / (ANALOG_MAX - ANALOG_MIN)) + GH_MIN
        else:
            _GH = None
        if self.s4 is not None:
            _AT = (((self.s4 - ANALOG_MIN) * (AT_MAX - AT_MIN)) / (ANALOG_MAX - ANALOG_MIN)) + AT_MIN
        else:
            _AT = None
        if self.s5 is not None:
            _AH = (((self.s5 - ANALOG_MIN) * (AH_MAX - AH_MIN)) / (ANALOG_MAX - ANALOG_MIN)) + AH_MIN
        else:
            _AH = None
        return Acquisition(None, datetime.now(), ACQUISITION_POINT, _EC, _WF, _GT, _GH, _AT, _AH)
