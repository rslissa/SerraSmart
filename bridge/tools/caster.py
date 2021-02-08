from model.acquisition import Acquisition

class Thresholds:
    # Arduino analog pin range 0-1023
    analogMax = 1023
    analogMin = 0
    # EC range 0-2000us/cm
    ECmax = 2000
    ECmin = 0
    # Water flow 0.3-6L/min
    WFmax = 6
    WFmin = 0.3
    # Ground temperature range -55-125°C
    GTmax = 125
    GTmin = -55
    # Ground humidity range 0-100%
    GHmax = 100
    GHmin = 0
    # Air temperature range -40-80°C
    ATmax = 80
    ATmin = -40
    # Air humidity range 0-100%
    AHmax = 100
    AHmin = 0


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
            _EC = (((self.s0 - Thresholds.analogMin) * (Thresholds.ECmax - Thresholds.ECmin)) /
                   (Thresholds.analogMax - Thresholds.analogMin)) + Thresholds.ECmin
        else:
            _EC = None
        if self.s1 is not None:
            _WF = (((self.s1 - Thresholds.analogMin) * (Thresholds.WFmax - Thresholds.WFmin)) /
                   (Thresholds.analogMax - Thresholds.analogMin)) + Thresholds.WFmin
        else:
            _WF = None
        if self.s2 is not None:
            _GT = (((self.s2 - Thresholds.analogMin) * (Thresholds.GTmax - Thresholds.GTmin)) /
                   (Thresholds.analogMax - Thresholds.analogMin)) + Thresholds.GTmin
        else:
            _GT = None
        if self.s3 is not None:
            _GH = (((self.s3 - Thresholds.analogMin) * (Thresholds.GHmax - Thresholds.GHmin)) /
                   (Thresholds.analogMax - Thresholds.analogMin)) + Thresholds.GHmin
        else:
            _GH = None
        if self.s4 is not None:
            _AT = (((self.s4 - Thresholds.analogMin) * (Thresholds.ATmax - Thresholds.ATmin)) /
                   (Thresholds.analogMax - Thresholds.analogMin)) + Thresholds.ATmin
        else:
            _AT = None
        if self.s5 is not None:
            _AH = (((self.s5 - Thresholds.analogMin) * (Thresholds.AHmax - Thresholds.AHmin)) /
                   (Thresholds.analogMax - Thresholds.analogMin)) + Thresholds.AHmin
        else:
            _AH = None
        return Acquisition(_EC, _WF, _GT, _GH, _AT, _AH)
