class SensorValues:
    def __init__(self):
        self.s0 = None
        self.s1 = None
        self.s2 = None
        self.s3 = None
        self.s4 = None
        self.s5 = None

    def tostring(self):
        if isinstance(self.s0, int):
            print("s0: %i" % self.s0)
        else:
            if self.s0 is None:
                print("s0: is None")
        if isinstance(self.s1, int):
            print("s1: %i" % self.s1)
        else:
            if self.s1 is None:
                print("s1: is None")
        if isinstance(self.s2, int):
            print("s2: %i" % self.s2)
        else:
            if self.s2 is None:
                print("s2: is None")
        if isinstance(self.s3, int):
            print("s3: %i" % self.s3)
        else:
            if self.s3 is None:
                print("s3: is None")
        if isinstance(self.s4, int):
            print("s4: %i" % self.s4)
        else:
            if self.s4 is None:
                print("s4: is None")
        if isinstance(self.s5, int):
            print("s5: %i" % self.s5)
        else:
            if self.s5 is None:
                print("s5: is None")


class Acquisition:
    def __init__(self, ec, wf, gt, gh, at, ah):
        self.EC = ec  # Electric Conductivity
        self.WF = wf  # Water Flow
        self.GT = gt  # Ground Temperature
        self.GH = gh  # Ground Humidity
        self.AT = at  # Air Temperature
        self.AH = ah  # Air Humidity

    def tostring(self):
        if isinstance(self.EC, float):
            print("EC: %f" % self.EC)
        else:
            if self.EC is None:
                print("EC: is None")
        if isinstance(self.WF, float):
            print("WF: %f" % self.WF)
        else:
            if self.WF is None:
                print("WF: is None")
        if isinstance(self.GT, float):
            print("GT: %f" % self.GT)
        else:
            if self.GT is None:
                print("GT: is None")
        if isinstance(self.GH, float):
            print("GH: %f" % self.GH)
        else:
            if self.GH is None:
                print("GH: is None")
        if isinstance(self.AT, float):
            print("AT: %f" % self.AT)
        else:
            if self.AT is None:
                print("AT: is None")
        if isinstance(self.AH, float):
            print("AH: %f" % self.AH)
        else:
            if self.AH is None:
                print("AH: is None")
